from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    question: str
    sourcesID: int

class ChatResponseData(BaseModel):
    question: str
    answer: str

class ChatResponse(BaseModel):
    status: str
    data: ChatResponseData