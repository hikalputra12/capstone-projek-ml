from fastapi import APIRouter, Depends, HTTPException
from internal.usecase.chat import ChatUsecase
from internal.wire.wire import get_chat_usecase
from internal.data.dto.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/ask", response_model=ChatResponse)
def ask_chatbot(payload: ChatRequest, usecase: ChatUsecase = Depends(get_chat_usecase)):
    try:
        # Panggil usecase dengan mengirimkan payload objek ChatRequest langsung 
        #  atau sesuaikan dengan parameter (payload.question, payload.sourcesID) jika pakai Opsi B
        result = usecase.get_answer(payload)
        
        # LANGSUNG KEMBALIKAN objek 'result' karena tipenya sudah 'ChatResponse'
        #  FastAPI akan otomatis mengubah objek Pydantic ini menjadi JSON yang sesuai.
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))