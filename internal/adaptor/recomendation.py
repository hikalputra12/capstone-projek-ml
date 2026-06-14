# internal/adaptor/recomendation.py
# Handler API untuk memproses permintaan rekomendasi course.

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional
from internal.usecase.recomendation import CourseUsecase
from internal.wire.wire import get_course_usecase
from pkg.utils.security import get_api_key
import time

router = APIRouter()

# Endpoint Baru (GET /api/v1/recommendations)
@router.get("/recommendations", dependencies=[Depends(get_api_key)])
def get_course_recommendations(
    title: str, 
    request: Request, 
    level: Optional[str] = None,
    usecase: CourseUsecase = Depends(get_course_usecase)
):
    log = request.app.state.logger
    start_time = time.time()

    log.info(f"Incoming Request | Title: {title} | Level: {level}")

    try:
        result = usecase.get_recommendations(title, level=level)
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

# Endpoint POST /api/v1/recommendations/retrain
@router.post("/recommendations/retrain", dependencies=[Depends(get_api_key)])
def retrain_recommender(
    request: Request,
    usecase: CourseUsecase = Depends(get_course_usecase)
):
    log = request.app.state.logger
    start_time = time.time()
    log.info("Incoming request to retrain recommender model...")
    
    try:
        result = usecase.retrain_and_reload()
        duration = time.time() - start_time
        
        if result.get("status") == "success":
            log.info("Retraining and reloading completed successfully.", extra={
                "latency": f"{duration:.4f}s",
                "run_id": result.get("run_id")
            })
            return result
        else:
            log.error("Retraining failed", extra={"reason": result.get("reason")})
            raise HTTPException(status_code=400, detail=result.get("reason"))
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        duration = time.time() - start_time
        log.error("Retraining failed due to internal error", extra={
            "error_message": str(e),
            "latency": f"{duration:.4f}s"
        })
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Retraining Error: {str(e)}")