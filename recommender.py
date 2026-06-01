# recommender.py
# Fungsi inti pencarian indeks kemiripan (Content-Based Filtering)

import os
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

MODEL_PATH = "pkg/ml-models/cosine_sim_model.joblib"
TFIDF_PATH = "pkg/ml-models/tfidf_vectorizer.joblib"

class Recommender:
    def __init__(self):
        self.cosine_sim = None
        self.tfidf = None
        self.load_models()

    def load_models(self):
        """Memuat matriks cosine similarity dan TF-IDF vectorizer dari penyimpanan joblib."""
        if os.path.exists(MODEL_PATH) and os.path.exists(TFIDF_PATH):
            self.cosine_sim = joblib.load(MODEL_PATH)
            self.tfidf = joblib.load(TFIDF_PATH)
            print("--- Recommender: Model berhasil dimuat ke memori ---")
        else:
            print("--- Recommender Warning: File model tidak ditemukan. Silakan lakukan training ---")

    def get_recommendations(self, title: str, df: pd.DataFrame) -> list:
        """
        Mencari indeks kursus yang paling mirip dengan judul target.
        Mengembalikan list tuple (index, similarity_score).
        """
        if self.cosine_sim is None or df.empty:
            return []

        # 1. Cari exact match
        target_title = title.strip().lower()
        df_search = df['title'].str.strip().str.lower()
        matches = df[df_search == target_title]

        if not matches.empty:
            idx = matches.index[0]
            if idx >= len(self.cosine_sim):
                return []
            raw_scores = self.cosine_sim[idx]
            sim_scores = sorted(enumerate(raw_scores), key=lambda x: x[1], reverse=True)
            
            # Ambil top 5 kemiripan (lewati diri sendiri)
            top_matches = []
            for i, score in sim_scores:
                if i == idx:
                    continue
                if len(top_matches) >= 5:
                    break
                top_matches.append((i, score))
            return top_matches
        else:
            # 2. Fallback: Keyword search jika exact match tidak ditemukan
            if self.tfidf is None:
                return []
            
            # Buat gabungan metadata teks sesuai skema training
            metadata = (
                df['title'].fillna('') + " " + 
                df['category'].fillna('') + " " + 
                df['description'].fillna('') + " " + 
                df['skills'].fillna('') + " " + 
                df['summary'].fillna('')
            ).str.strip().str.lower()

            course_matrix = self.tfidf.transform(metadata)
            query_vector = self.tfidf.transform([title.lower()])
            sim_scores = cosine_similarity(query_vector, course_matrix).flatten()
            top_indices = sim_scores.argsort()[::-1][:5]
            
            return [(int(i), float(sim_scores[i])) for i in top_indices if sim_scores[i] > 0]
