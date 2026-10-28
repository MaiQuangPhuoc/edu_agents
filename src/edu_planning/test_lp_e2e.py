import sys,types,os,tempfile,json,re,time,collections; sys.path.insert(0,".")
from types import SimpleNamespace as NS
from pathlib import Path
sys.modules["tavily"]=NS(TavilyClient=lambda **k:None)
sys.modules["googleapiclient"]=types.ModuleType("googleapiclient"); gd=types.ModuleType("googleapiclient.discovery"); gd.build=lambda *a,**k:None; sys.modules["googleapiclient.discovery"]=gd
sys.modules["isodate"]=types.ModuleType("isodate")
import src.state_plan as sp
from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_planning import lp_execute, path_store, lp_tools
from src.edu_planning.learning_path_graph import make_learning_path_graph
lp_tools.CACHE_DIR=Path(tempfile.mkdtemp()); path_store.PATH_DIR=Path(tempfile.mkdtemp())
C=get_subject_curriculum("Toán 10"); l=lambda c:list(C[c]["lessons"])
ch=lambda cid,ls:{"chapter_id":cid,"lessons":ls,"ly_do":"Yếu nên học trước"}
roadmap={"muc_tieu_tong":"m","chien_luoc":"c","gia_dinh":[],"giai_doan":[{"thu_tu":1,"ten":"N","mon_hoc":"Toán 10","muc_tieu":"m","tieu_chi_hoan_thanh":"t","chapters":[ch("I",l("I")[:2]),ch("II",l("II")[:1])]}]}
sm=sp.StudentModel(student_id="x",muc_tieu=[sp.MucTieu(mon_hoc="Toán 10",muc_tieu_diem=8,so_tuan_con_lai=3)],nang_luc=[sp.NangLucMonHoc(mon_hoc="Toán 10",chu_de=[sp.ChuDe(chapter_id="I",muc_nam=0.3)] if hasattr(sp,"ChuDe") else [])],lich_hoc=sp.LichHoc(so_buoi_tuan=3,khung_gio_ranh={"thu_2":["19:00-21:00"],"thu_4":["19:00-21:00"],"thu_7":["14:00-17:00"]}),so_thich_hoc=sp.SoThichHoc(thoi_luong_buoi_phut=60,dung_video=True,dung_tai_lieu=True)).model_dump(mode="json")
D=lambda t,**m: NS(page_content=t,metadata=m)
class R:
    def lesson_plan_search(s,*a,**k): return []
    def lesson_plan_lessons(s,sub,ch): return {}
    def search_sgk(s,q,sub,ch,k=None,sub_type=None): return [D("sgk "+q[:30],retrieve_score=.8)]*8
    def rerank(s,q,d,top_k=3): return d[:top_k]
CALLS=collections.Counter()
class L:
    def invoke_structured(s,model,msgs,max_tokens=0,**k):
        CALLS[model.__name__]+=1; u=msgs[1]["content"]
        if model is sp.OutlinePlan:
            tot=3; codes=list(dict.fromkeys(re.findall(r"\b([IVX]+\.\d+)\b",u)))     # không phụ thuộc định dạng prompt; 3 = so_tuan_con_lai của học sinh mẫu
            n=tot; w=[sp.OutlineWeek(phase=1,goal=f"g{i}",lessons=codes[i*len(codes)//n:(i+1)*len(codes)//n] or [codes[-1]],activity_types=["lecture","exercise"],difficulty_trend="dễ → vừa",has_assessment=(i==n-1)) for i in range(n)]
            return sp.OutlinePlan(weeks=w,self_check=sp.OutlineSelfCheck(all_lessons_covered=True,phases_contiguous=True,difficulty_ratio_ok=True,time_budget_ok=True))
        if model is sp.ChapterKnowledge:
            names=[x[2:] for x in u.split("CÁC BÀI CẦN PHÂN TÍCH")[1].split("TÀI LIỆU THEO")[0].split("\n") if x.startswith("- ")]
            return sp.ChapterKnowledge(chapter_id="I",lessons=[sp.LessonKnowledge(lesson=n,key_points=["ý "+n],must_know=["nắm "+n],must_understand=["hiểu "+n],problem_types=["dạng A "+n,"dạng B "+n]) for n in names])
        if model is sp.ResourceQueryPlan:
            q=[sp.ResourceQuery(purpose="theory",tool="video",query="Mệnh đề bài giảng"),sp.ResourceQuery(purpose="exam",tool="web",query="Tập hợp đề ôn tập")]
            return sp.ResourceQueryPlan(candidates=q,chosen=q)
        if model is sp.ResourceVerdict:
            return sp.ResourceVerdict(items=[])
        if model is sp.WeekDraft:
            slots=[int(m) for m in re.findall(r"^Buổi \d+: (\d+) phút",u,re.M)]; codes=re.findall(r"^(\w+\.\d+): ",u.split("BÀI CỦA TUẦN")[1],re.M)
            assess="has_assessment): true" in u; urls=re.findall(r"https?://\S+",u.split("TÀI NGUYÊN TÌM ĐƯỢC")[1].split("CÁC BUỔI")[0])
            ss=[]
            for i,m in enumerate(slots):
                last=assess and i==len(slots)-1
                ss.append(sp.SessionDraft(lesson=codes[i%len(codes)],type="assessment" if last else "lesson",activities=[sp.ActivityDraft(type="lecture",content="Học ý chính",minutes=m//2),sp.ActivityDraft(type="exercise",content="Làm bài",minutes=m-m//2,problem_type="dạng A")],
                    resources=[sp.Resource(type="video",title="V",url=urls[0])] if urls and not last else []))
            return sp.WeekDraft(goal="mục tiêu tuần",sessions=ss,self_check=sp.WeekSelfCheck(session_count_matches=True,all_lessons_covered=True,assessment_rule_ok=True,only_given_resources=True,activities_grounded=True))
        if model is sp.ReviewResult: return sp.ReviewResult(verdict="pass",issues=[])
        raise AssertionError(model)
class T:
    def __init__(s,n,f): s.name=n; s.f=f
    def invoke(s,a): time.sleep(.05); return s.f(a["query"])
lp_execute.make_planning_tools=lambda r,l:[T("search_videos",lambda q:[{"loai":"video","tieu_de":"Toán 10 Mệnh đề Tập hợp bài giảng","url":"https://youtube.com/watch?v=abc","kenh":"K","phut":30,"luot_xem":9000,"thich":300,"nguoi_dang_ky":5000,"mo_ta":"d"}]),
   T("search_web_documents",lambda q:[{"loai":"tai_lieu","tieu_de":"Đề ôn tập Tập hợp lớp 10","url":"https://x.com/de","so_trang":5,"ngay":None,"mo_ta":"d"}])]
g=make_learning_path_graph(R(),L(),plan_client=L())
st={"student_model":sm,"master_roadmap":roadmap,"vi_tri_hien_tai":1,"plan_transcript":"[Tra cứu] search_web_documents (chương I): tập hợp\n- [tài liệu] Tập hợp sườn | https://x.com/seed"}
t=time.time(); out=g.invoke(st); print("thời gian",round(time.time()-t,2),"s | trạng thái:",out.get("roadmap_status"),"|",out["messages"][-1].content[:100])
print("số lần gọi LLM:",dict(CALLS))
lp=out.get("learning_path")
if lp:
    print("tuần:",len(lp["weeks"]),"| buổi:",[len(w["sessions"]) for w in lp["weeks"]],"| ghi chú:",lp.get("assumptions"))
    s0=lp["weeks"][0]["sessions"][0]; print(s0["date"],s0["chapter_id"],s0["lesson"],s0["key_points"],[(a["type"],a["minutes"],a["problem_type"]) for a in s0["activities"]],s0["resources"])
    print("assessment cuối:",lp["weeks"][-1]["sessions"][-1]["type"], lp["weeks"][-1]["sessions"][-1].get("assessment"))
