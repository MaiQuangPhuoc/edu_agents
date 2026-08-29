from pydantic import BaseModel, Field

class RetrieverEvalItem(BaseModel):

    question: str

    gold_chunks: list[str]

    subject_id: str

    chapter_id: str

    reasoning: str = Field(
        ...,
        description=(
            "Giải thích ngắn gọn vì sao chọn các gold_chunks này."
        )
    )