# train_recommender.py
# Script sinkronisasi model baru untuk sistem rekomendasi kursus.
# Menghubungkan ke database PostgreSQL, memuat kursus yang diterbitkan,
# memproses text menggunakan TF-IDF Vectorizer dan menghitung Cosine Similarity.

import joblib
import pandas as pd
import time
import os
import mlflow
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from pkg.database.postgress import engine
from pkg.utils.config import settings

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

def run_retrain() -> dict:
    print("--- [TRAIN] Memulai proses sinkronisasi model rekomendasi ---")
    
    # 1. Inisialisasi MLflow
    if settings.MLFLOW_TRACKING_URI:
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        print(f"--- [MLFLOW] Menggunakan Tracking URI: {settings.MLFLOW_TRACKING_URI} ---")
    else:
        print("--- [MLFLOW] Menggunakan tracking lokal (folder ./mlruns) ---")
        
    mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)
    
    run_name = settings.MLFLOW_RUN_NAME or "content-based-filtering"
    
    # Menjalankan tracking dalam MLflow run block
    with mlflow.start_run(run_name=run_name) as run:
        print(f"--- [MLFLOW] Run ID: {run.info.run_id} ---")
        
        # Muat data dari database
        start_db = time.time()
        df = load_data_from_db()
        db_load_time = time.time() - start_db
        
        if df.empty:
            print("--- [TRAIN] Error: Database kosong atau tidak ada course yang di-publish! ---")
            mlflow.log_param("status", "failed_empty_db")
            return {"status": "failed", "reason": "Database kosong atau tidak ada course yang di-publish"}

        print(f"--- [TRAIN] Training menggunakan {len(df)} data dari database. ---")

        # 2. Gabungkan fitur teks untuk dihitung kemiripannya (TF-IDF)
        start_train = time.time()
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
        training_time = time.time() - start_train

        # 6. Simpan Model Baru (Menimpa file lama)
        MODEL_PATH = "pkg/ml-models/cosine_sim_model.joblib"
        VECTOR_PATH = "pkg/ml-models/tfidf_vectorizer.joblib"
        
        # Pastikan folder target ada
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        
        joblib.dump(cosine_sim, MODEL_PATH)
        joblib.dump(tfidf, VECTOR_PATH)
        
        print(f"--- [TRAIN] Berhasil! Model disimpan di: {MODEL_PATH} ---")
        
        # 7. Log Parameter ke MLflow
        mlflow.log_param("vectorizer_type", "TfidfVectorizer")
        mlflow.log_param("stop_words_provider", "Sastrawi")
        mlflow.log_param("number_of_stop_words", len(id_stop_words))
        mlflow.log_param("database_table", "public.courses")
        
        # 8. Log Metrik ke MLflow
        mlflow.log_metric("num_courses", len(df))
        mlflow.log_metric("vocabulary_size", len(tfidf.vocabulary_))
        mlflow.log_metric("db_load_time_sec", db_load_time)
        mlflow.log_metric("training_time_sec", training_time)
        
        # 9. Log Artifact ke MLflow
        mlflow.log_artifact(MODEL_PATH)
        mlflow.log_artifact(VECTOR_PATH)
        print("--- [MLFLOW] Berhasil melacak run, parameter, metrik, dan menyimpan artifact model! ---")
        print("--- [TRAIN] Silakan restart server main.py Anda sekarang. ---")
        
        return {
            "status": "success",
            "run_id": run.info.run_id,
            "num_courses": len(df),
            "vocabulary_size": len(tfidf.vocabulary_),
            "db_load_time_sec": round(db_load_time, 4),
            "training_time_sec": round(training_time, 4)
        }

if __name__ == "__main__":
    run_retrain()

