import joblib
import os
from fastapi import Depends
from sqlalchemy.orm import Session

# Import koneksi DB dan Repository
from pkg.database.postgress import get_db
from internal.data.repository.course import CourseRepository

# Import Usecase (Rekomendasi & Chat)
from internal.usecase.recomendation import CourseUsecase
from internal.usecase.chat import ChatUsecase

# Path Model untuk fitur rekomendasi
MODEL_PATH = "pkg/ml-models/cosine_sim_model.joblib"
TFIDF_PATH = "pkg/ml-models/tfidf_vectorizer.joblib"

# Singleton instances (disimpan di RAM agar server cepat)
_cosine_sim = None
_tfidf_vectorizer = None
_chat_usecase = None

def load_ml_components():
    """
    Memuat semua komponen ML ke memori. 
    Dipanggil satu kali saat startup aplikasi di main.py.
    """
    global _cosine_sim, _tfidf_vectorizer, _chat_usecase
    
    # Memuat Model Rekomendasi 
    if os.path.exists(MODEL_PATH) and os.path.exists(TFIDF_PATH):
        print("--- Wiring: Loading Similarity Matrix & Vectorizer ---")
        _cosine_sim = joblib.load(MODEL_PATH)
        _tfidf_vectorizer = joblib.load(TFIDF_PATH)
    else:
        print(f"--- Wiring Warning: ML Recommendation files not found ---")

    # Inisialisasi Chatbot RAG (Fitur Baru Gemini)
    if _chat_usecase is None:
        print("--- Wiring: Initializing ChatUsecase (Gemini & ChromaDB) ---")
        _chat_usecase = ChatUsecase()

# --- Dependencies untuk REKOMENDASI COURSE ---

def get_course_repository(db: Session = Depends(get_db)) -> CourseRepository:
    """Menyediakan akses ke tabel courses di PostgreSQL."""
    return CourseRepository(db)

def get_course_usecase(
    repo: CourseRepository = Depends(get_course_repository)
) -> CourseUsecase:
    """Menghubungkan repository dengan matriks cosine similarity dan TF-IDF vectorizer."""
    return CourseUsecase(repo, _cosine_sim, _tfidf_vectorizer)

# --- Dependencies untuk CHATBOT AI ---

def get_chat_usecase() -> ChatUsecase:
    """
    Mengembalikan instance ChatUsecase.
    Komponen ini yang akan menangani pertanyaan user via Gemini.
    """
    global _chat_usecase
    if _chat_usecase is None:
        _chat_usecase = ChatUsecase()
    return _chat_usecase