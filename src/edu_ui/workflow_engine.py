"""Lazy graph integration; the existing terminal entrypoints remain usable."""
import asyncio
import logging

class Engine:
    def __init__(self):
        self.graphs = {}
        self.lock = asyncio.Lock()
        self.llm = self.retriever = None
        self.warm_status = "idle"

    async def warmup(self):
        self.warm_status = "loading"
        try:
            async with self.lock:
                await self.graph("qa")
            self.warm_status = "ready"
        except asyncio.CancelledError:
            self.warm_status = "idle"
            raise
        except Exception:
            self.warm_status = "failed"
            logging.getLogger(__name__).exception("QA startup initialization failed; a later request may retry")

    def _build(self, mode):
        from src.configs import env_config
        from src.clients.llm import LLMClient
        if self.llm is None:
            from src.clients.embedding import embeddings_qa
            from src.modules.rag.process_toan_10.retrievers2 import VectorStoreRetriever
            llm = LLMClient(model=env_config.model, api_provider=env_config.api_provider)
            retriever = VectorStoreRetriever(
                url=env_config.qdrant_url, api_key=env_config.qdrant_api_key,
                embeddings=embeddings_qa, collection_name="doc_final", tools_collection_name="tools", top_k=10)
            self.llm, self.retriever = llm, retriever
        if mode == "qa":
            from src.edu_qa.graph import build_graph
            graph = build_graph(llm_client=self.llm, retriever=self.retriever)
        elif mode == "exam":
            from src.edu_exam.graph_exam_v2 import create_graph
            graph = create_graph(self.llm, self.retriever)
        else:
            from src.edu_planning.roadmap_graph import make_roadmap_graph
            # State is owned by the UI session; no shared student_id checkpoint.
            graph = make_roadmap_graph(self.retriever, self.llm)
        self.graphs[mode] = graph
        return graph

    async def graph(self, mode):
        if mode not in self.graphs:
            await asyncio.to_thread(self._build, mode)
        return self.graphs[mode]

    async def run(self, session, text, progress):
        from copy import deepcopy
        from langchain_core.messages import HumanMessage
        from langchain_core.callbacks import BaseCallbackHandler
        loop = asyncio.get_running_loop()

        class Progress(BaseCallbackHandler):
            def on_chain_start(self, serialized, inputs, *, run_id, metadata=None, **kwargs):
                name = (metadata or {}).get("langgraph_node")
                if name:
                    loop.call_soon_threadsafe(progress, name)

            def on_tool_start(self, serialized, input_str, **kwargs):
                loop.call_soon_threadsafe(progress, "tool")

        progress("initializing")
        graph = await self.graph(session["mode"])
        state = deepcopy(session["state"])
        if session["mode"] == "qa":
            if not state:
                from src.edu_qa.state import QAState
                state = QAState(user_query=text).model_dump()
            state.update(user_query=text, router_output=None, rag_results=[], solve_results=[], final_answer=None, suggestions=[])
        else:
            if not state and session["mode"] == "exam":
                from src.edu_exam.run_exam_v2 import build_initial_state
                state = build_initial_state()
            state.setdefault("messages", []).append(HumanMessage(content=text))
            if session["mode"] == "planning":
                state["student_id"] = session["student_id"]
                state["lp_verify"] = session["lp_verify"]
        result = await graph.ainvoke(state, {"recursion_limit": 100, "callbacks": [Progress()]})
        session["state"] = result.model_dump() if hasattr(result, "model_dump") else result

    def practice(self, session, lesson):
        from src.edu_exam.exam_for_session import run_exam_for_session
        from src.clients.llm import LLMClient
        from src.configs import env_config
        subject = (session["state"].get("lp_window") or {}).get("subject")
        if not subject:
            raise ValueError("Lộ trình chưa xác định môn học, không thể tạo đề cho buổi này.")
        heavy = LLMClient(model=env_config.model_edu_exam, api_provider=env_config.plan_provider)
        return run_exam_for_session(session["state"]["student_model"], lesson, subject,
                                    self.llm, heavy, self.retriever)


engine = Engine()
