#kode ini untuk menghandle request rekomendasi course berdasarkan title yang diberikan, dan juga untuk logging performa dari request tersebut.

from fastapi import APIRouter, Depends, HTTPException, Request
from internal.usecase.recomendation import CourseUsecase
from internal.wire.wire import get_course_usecase
import time

router = APIRouter()
@router.get("/recommend")
def get_course_recommendations(
    title: str, 
    request: Request, 
    usecase: CourseUsecase = Depends(get_course_usecase)
):
    log = request.app.state.logger
    start_time = time.time()

    log.info(f"Incoming Request | Title: {title}")

    try:
        result = usecase.get_recommendations(title)
        duration = time.time() - start_time
        
        #masih belum benar dan perlu di perbaiki
        # Mengambil jumlah item dari object response
        item_count = len(result.data) if hasattr(result, 'data') else "unknown"
        print(item_count)
        log.info("Request Success", extra={
            "latency": f"{duration:.4f}s",
            "items_found": item_count,
            "query": title
        })
        
        return result

    except Exception as e:
        duration = time.time() - start_time
        log.error("Request Failed", extra={
            "error_message": str(e),
            "latency": f"{duration:.4f}s"
        })
        raise HTTPException(status_code=500, detail=f"Model Error: {str(e)}")