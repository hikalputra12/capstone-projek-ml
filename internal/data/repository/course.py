# internal/data/repository/course.py
# Query untuk penarikan data course dari PostgreSQL secara terstruktur dan terfilter.

from sqlalchemy.orm import Session
from sqlalchemy import func
from internal.data.entity.course import CourseEntity
import pandas as pd

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_courses_dataframe(self) -> pd.DataFrame:
        """
        Mengambil semua data course yang aktif (is_published = true)
        dengan urutan konsisten ORDER BY id ASC untuk sinkronisasi
        index TF-IDF / Cosine Similarity.
        """
        query = (
            self.db.query(CourseEntity)
            .filter(CourseEntity.is_published == True)
            .order_by(CourseEntity.id.asc())
        )
        # Mengonversi hasil query secara langsung ke Pandas DataFrame
        df = pd.read_sql(query.statement, self.db.bind)
        return df

    def get_course_by_title(self, title: str) -> CourseEntity:
        """
        Mengambil data satu kursus berdasarkan judul secara case-insensitive.
        """
        return (
            self.db.query(CourseEntity)
            .filter(func.lower(CourseEntity.title) == title.strip().lower())
            .first()
        )