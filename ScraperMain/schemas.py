from pydantic import BaseModel


class CircularSummary(BaseModel):
    id: str
    title: str


class CircularDetail(CircularSummary):
    content: str