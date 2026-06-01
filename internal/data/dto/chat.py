# internal/data/dto/chat.py
# DTO (Data Transfer Object) untuk request dan response Chatbot AI.

from pydantic import BaseModel

# Request Schema Baru (Hanya menerima user_question di body)
class ChatbotRequest(BaseModel):
    user_question: str

class ChatResponseData(BaseModel):
    question: str
    answer: str

# Response Schema tanpa duplikasi 'answer' di root
class ChatResponse(BaseModel):
    status: str
    data: ChatResponseData