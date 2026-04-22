import joblib
import os
from fastapi import Depends
from sqlalchemy.orm import Session
from pkg.database.postgress import get_db
from internal.data.repository.course import CourseRepository
from internal.usecase.recomendation import CourseUsecase

# Sesuaikan dengan path yang kamu punya
MODEL_PATH = "pkg/ml-models/cosine_sim_model.joblib"
TFIDF_PATH = "pkg/ml-models/tfidf_vectorizer.joblib"

_cosine_sim = None
_tfidf_vectorizer = None

def load_ml_components():
    global _cosine_sim, _tfidf_vectorizer
    if os.path.exists(MODEL_PATH) and os.path.exists(TFIDF_PATH):
        print("--- Wiring: Loading Similarity Matrix & Vectorizer ---")
        _cosine_sim = joblib.load(MODEL_PATH)
        _tfidf_vectorizer = joblib.load(TFIDF_PATH)
    else:
        print(f"--- Wiring Warning: Files not found at {MODEL_PATH} ---")

def get_course_repository(db: Session = Depends(get_db)) -> CourseRepository:
    return CourseRepository(db)

def get_course_usecase(
    repo: CourseRepository = Depends(get_course_repository)
) -> CourseUsecase:
    # Kita kirim matriks sim dan repo ke usecase
    return CourseUsecase(repo, _cosine_sim)