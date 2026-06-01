# internal/adaptor/chat.py
# Handler API untuk memproses permintaan Chatbot AI (FastAPI Endpoints).

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from internal.usecase.chat import ChatUsecase
from internal.wire.wire import get_chat_usecase
from internal.data.dto.chat import ChatbotRequest, ChatResponse

router = APIRouter()

# Endpoint Baru (POST /api/v1/chatbot)
# Menerima course_id dan course_title sebagai query parameter, bukan di JSON request body
@router.post("/chatbot", response_model=ChatResponse)
def chatbot_endpoint(
    payload: ChatbotRequest, 
    course_id: Optional[int] = Query(None, description="ID Kursus acuan yang sedang dipelajari"),
    course_title: Optional[str] = Query(None, description="Judul Kursus acuan yang sedang dipelajari"),
    usecase: ChatUsecase = Depends(get_chat_usecase)
):
    try:
        result = usecase.get_answer(
            question=payload.user_question, 
            course_id=course_id, 
            course_title=course_title
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))