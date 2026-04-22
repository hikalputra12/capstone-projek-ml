from fastapi import APIRouter, Depends, HTTPException
from internal.usecase.recomendation import CourseUsecase
from internal.wire.wire import get_course_usecase

router = APIRouter()

@router.get("/recommend")
def get_course_recommendations(title: str, usecase: CourseUsecase = Depends(get_course_usecase)):
    result = usecase.get_recommendations(title)
    if not result:
        raise HTTPException(status_code=404, detail="Course title not found in database")
    return result