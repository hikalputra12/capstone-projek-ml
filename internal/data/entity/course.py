#kode berisi definisi entity untuk course yang akan digunakan untuk menyimpan data course yang diambil dari database. Entity ini akan digunakan oleh usecase untuk memproses data dan menghasilkan rekomendasi course yang sesuai dengan title yang diberikan.

from sqlalchemy import Column, Integer, Text, Boolean
from pkg.database.postgress import Base

class CourseEntity(Base):
    __tablename__ = "courses"

    id               = Column(Integer, primary_key=True, index=True)
    title            = Column(Text, nullable=False)
    description      = Column(Text)
    skills           = Column(Text)
    category         = Column(Text)
    tags             = Column(Text)
    order_index      = Column(Integer)
    duration_minutes = Column(Integer)
    is_published     = Column(Boolean)
    external_url     = Column(Text)
    level            = Column(Text)
    summary          = Column(Text)
    learning_points  = Column(Text)
    duration_text    = Column(Text)