# internal/adaptor/recomendation.py
# Handler API untuk memproses permintaan rekomendasi course.

from fastapi import APIRouter, Depends, HTTPException, Request
from internal.usecase.recomendation import CourseUsecase
from internal.wire.wire import get_course_usecase
import time

router = APIRouter()

# Endpoint Baru (GET /api/v1/recommendations)
@router.get("/recommendations")
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
        
        # Perbaikan log item_count agar merujuk ke recommendations
        item_count = len(result.recommendations) if hasattr(result, 'recommendations') else "unknown"
        
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