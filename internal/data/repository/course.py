from sqlalchemy.orm import Session
from internal.data.entity.course import CourseEntity
import pandas as pd

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    # Mengambil semua data untuk keperluan Training/Loading Model ke Pandas
    def get_all_courses_dataframe(self):
        query = self.db.query(CourseEntity)
        # Mengonversi hasil query SQLAlchemy langsung ke Pandas DataFrame
        df = pd.read_sql(query.statement, self.db.bind)
        return df

    # Mengambil satu kursus berdasarkan judul (untuk validasi input)
    def get_course_by_title(self, title: str):
        return self.db.query(CourseEntity).filter(CourseEntity.title == title).first()