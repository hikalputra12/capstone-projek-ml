#kode berisi definisi entity untuk course yang akan digunakan untuk menyimpan data course yang diambil dari database. Entity ini akan digunakan oleh usecase untuk memproses data dan menghasilkan rekomendasi course yang sesuai dengan title yang diberikan.

from sqlalchemy import Column, Integer, Text
from pkg.database.postgress import Base

class CourseEntity(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    skills = Column(Text)
    description = Column(Text)
    modules = Column(Text)
    level = Column(Text)
    schedule = Column(Text)