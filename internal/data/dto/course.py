from pydantic import BaseModel
from typing import List, Optional

# DTO untuk menampilkan hasil rekomendasi
class CourseRecommendationResponse(BaseModel):
    title: str
    cosine_score: float
    level: Optional[str]
    skills: Optional[str]

    class Config:
        from_attributes = True

# DTO untuk response utama
class RecommendationBaseResponse(BaseModel):
    target_course: str
    recommendations: List[CourseRecommendationResponse]