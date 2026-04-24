#kode ini berisi script untuk melakukan retrain model cosine similarity berdasarkan data terbaru yang ada di database. Script ini akan mengambil data course dari database, memprosesnya menggunakan TF-IDF, menghitung cosine similarity, dan menyimpan model yang sudah di-train ke dalam file joblib yang akan digunakan oleh aplikasi rekomendasi course.

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pkg.database.postgress import engine # Mengambil koneksi DB kamu

def run_retrain():
    print("--- [RETRAIN] Memulai proses sinkronisasi model dengan Database ---")
    
    #  Ambil data asli dari Database agar urutan INDEX SAMA PERSIS
    # Pastikan ORDER BY id agar urutannya konsisten
    query = "SELECT id, title, skills, description FROM courses ORDER BY id ASC"
    df = pd.read_sql(query, engine)
    
    if df.empty:
        print("--- [RETRAIN] Error: Database kosong! ---")
        return

    print(f"--- [RETRAIN] Training menggunakan {len(df)} data dari database. ---")

    # Gabungkan fitur teks untuk dihitung kemiripannya 
    df['metadata'] = df['title'] + " " + df['skills'] + " " + df['description']
    # Pastikan tidak ada nilai NaN di kolom metadata (jika ada, ganti dengan string kosong)
    df['metadata'] = df['metadata'].fillna('')

    # Proses TF-IDF
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['metadata'])

    # Hitung Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Simpan Model Baru (Timpa file yang lama)
    MODEL_PATH = "pkg/ml-models/cosine_sim_model.joblib"
    VECTOR_PATH = "pkg/ml-models/tfidf_vectorizer.joblib"
    
    joblib.dump(cosine_sim, MODEL_PATH)
    joblib.dump(tfidf, VECTOR_PATH)
    
    print(f"--- [RETRAIN] Berhasil! Model disimpan di: {MODEL_PATH} ---")
    print("--- [RETRAIN] Silakan restart server main.py kamu sekarang. ---")

if __name__ == "__main__":
    run_retrain()