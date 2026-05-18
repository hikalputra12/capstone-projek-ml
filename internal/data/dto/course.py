#kode ini berisi data transfer object (DTO) untuk course yang akan digunakan untuk menampilkan hasil rekomendasi course yang sesuai dengan title yang diberikan. DTO ini akan digunakan oleh adaptor untuk mengirimkan data ke client dalam format yang sesuai.

from pydantic import BaseModel
from typing import List, Optional

# DTO untuk menampilkan hasil rekomendasi
class CourseRecommendationResponse(BaseModel):
    id: int
    title: str
    cosine_score: float
    category: Optional[str]
    skills: Optional[str]

    class Config:
        from_attributes = True

# DTO untuk response utama
class RecommendationBaseResponse(BaseModel):
    target_course: str
    recommendations: List[CourseRecommendationResponse]