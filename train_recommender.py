# train_recommender.py
# Script sinkronisasi model baru untuk sistem rekomendasi kursus.
# Menghubungkan ke database PostgreSQL, memuat kursus yang diterbitkan,
# memproses text menggunakan TF-IDF Vectorizer dan menghitung Cosine Similarity.

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from pkg.database.postgress import engine

def load_data_from_db() -> pd.DataFrame:
    """
    Mengambil data kursus dari database PostgreSQL sesuai dengan spesifikasi ERD terbaru.
    Hanya mengambil course yang is_published = true dan diurutkan berdasarkan id ASC.
    """
    query = """
    SELECT id, title, category, description, skills, summary 
    FROM public.courses 
    WHERE is_published = true 
    ORDER BY id ASC;
    """
    print("--- [TRAIN] Menarik data dari database... ---")
    df = pd.read_sql(query, engine)
    return df

def run_retrain():
    print("--- [TRAIN] Memulai proses sinkronisasi model rekomendasi ---")
    
    # 1. Muat data dari database
    df = load_data_from_db()
    
    if df.empty:
        print("--- [TRAIN] Error: Database kosong atau tidak ada course yang di-publish! ---")
        return

    print(f"--- [TRAIN] Training menggunakan {len(df)} data dari database. ---")

    # 2. Gabungkan fitur teks untuk dihitung kemiripannya (TF-IDF)
    # Kolom Fitur Teks untuk TF-IDF: title, category, description, skills, summary
    df['metadata'] = (
        df['title'].fillna('') + " " + 
        df['category'].fillna('') + " " + 
        df['description'].fillna('') + " " + 
        df['skills'].fillna('') + " " + 
        df['summary'].fillna('')
    )
    # Pastikan case-insensitive (huruf kecil semua) dan membersihkan spasi
    df['metadata'] = df['metadata'].str.strip().str.lower()

    # 3. Ambil daftar stop words bahasa Indonesia dari Sastrawi
    factory = StopWordRemoverFactory()
    id_stop_words = factory.get_stop_words()
    
    # 4. Proses TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words=id_stop_words)
    tfidf_matrix = tfidf.fit_transform(df['metadata'])

    # 5. Hitung Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 6. Simpan Model Baru (Menimpa file lama)
    MODEL_PATH = "pkg/ml-models/cosine_sim_model.joblib"
    VECTOR_PATH = "pkg/ml-models/tfidf_vectorizer.joblib"
    
    joblib.dump(cosine_sim, MODEL_PATH)
    joblib.dump(tfidf, VECTOR_PATH)
    
    print(f"--- [TRAIN] Berhasil! Model disimpan di: {MODEL_PATH} ---")
    print("--- [TRAIN] Silakan restart server main.py Anda sekarang. ---")

if __name__ == "__main__":
    run_retrain()
