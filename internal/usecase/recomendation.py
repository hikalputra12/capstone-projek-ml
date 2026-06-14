# internal/usecase/recomendation.py
# Logika bisnis untuk menghitung dan merekomendasikan course serupa berdasarkan judul.

from internal.data.repository.course import CourseRepository
from internal.data.dto.course import RecommendationBaseResponse, CourseRecommendationResponse
from sklearn.metrics.pairwise import cosine_similarity

class CourseUsecase:
    def __init__(self, repo: CourseRepository, cosine_sim, tfidf_vectorizer=None):
        """
        Inisialisasi Usecase.
        cosine_sim       : matriks hasil load joblib (numpy array)
        tfidf_vectorizer : TF-IDF vectorizer untuk keyword/cold-start search
        """
        self.repo = repo
        self.cosine_sim = cosine_sim
        self.tfidf = tfidf_vectorizer

    def _keyword_search(self, query: str, df, level: str = None) -> list:
        """
        Fallback: transform query menggunakan TF-IDF vectorizer
        dan hitung cosine similarity terhadap semua course.
        Digunakan saat query tidak cocok dengan judul course manapun (cold-start).
        """
        if self.tfidf is None:
            print("--- [DEBUG] TF-IDF vectorizer tidak tersedia untuk keyword search ---")
            return []

        # Buat metadata gabungan untuk setiap course (sama persis dengan saat training)
        df['metadata'] = (
            df['title'].fillna('') + " " + 
            df['category'].fillna('') + " " + 
            df['description'].fillna('') + " " + 
            df['skills'].fillna('') + " " + 
            df['summary'].fillna('')
        ).str.strip().str.lower()

        # Transform semua course menggunakan vectorizer yang sudah di-fit
        course_matrix = self.tfidf.transform(df['metadata'])

        # Transform query (keyword/interest dari user)
        query_vector = self.tfidf.transform([query.lower()])

        # Hitung cosine similarity antara query dan semua course
        sim_scores = cosine_similarity(query_vector, course_matrix).flatten()
        sorted_indices = sim_scores.argsort()[::-1]

        top_matches = []
        for i in sorted_indices:
            score = sim_scores[i]
            if score <= 0:
                break
            if len(top_matches) >= 5:
                break

            if level:
                row = df.iloc[i]
                row_level = str(row.get('level', '')).strip().lower()
                if row_level != level.strip().lower():
                    continue

            top_matches.append((int(i), float(score)))

        return top_matches

    def get_recommendations(self, title: str, level: str = None) -> RecommendationBaseResponse:
        # 1. Tarik data terfilter (hanya is_published = true, ORDER BY id ASC) dari DB
        df = self.repo.get_all_courses_dataframe()
        
        if df.empty:
            print("--- [DEBUG] Usecase: Database kosong atau tidak ada course yang di-publish! ---")
            return RecommendationBaseResponse(target_course=title, recommendations=[])

        if self.cosine_sim is None:
            print("--- [DEBUG] Usecase: Matriks Cosine Similarity NULL! ---")
            return RecommendationBaseResponse(target_course=title, recommendations=[])

        # 2. Cari indeks berdasarkan judul (Case-insensitive & strip)
        target_title = title.strip().lower()
        df_search = df['title'].str.strip().str.lower()
        matches = df[df_search == target_title]

        use_keyword_search = matches.empty
        top_matches = []
        display_target = title  # nama yang ditampilkan di response

        if not use_keyword_search:
            # ── Exact match: gunakan cosine_sim matrix ────────────────────────
            idx = matches.index[0]
            print(f"--- [DEBUG] Usecase: Exact match '{title}' di indeks {idx} ---")
            display_target = str(df.iloc[idx]['title'])

            try:
                if idx >= len(self.cosine_sim):
                    print(f"--- [DEBUG] ERROR: Indeks {idx} di luar jangkauan matriks ---")
                    use_keyword_search = True
                else:
                    raw_scores = self.cosine_sim[idx]
                    # Sort berdasarkan skor kemiripan tertinggi, lewati dirinya sendiri
                    sim_scores = sorted(enumerate(raw_scores), key=lambda x: x[1], reverse=True)
                    
                    # Ambil top 5 rekomendasi (indeks ke-1 sampai ke-5, skip diri sendiri di indeks 0)
                    top_matches = []
                    for i, score in sim_scores:
                        if i == idx:
                            continue
                        if len(top_matches) >= 5:
                            break

                        if level:
                            row = df.iloc[i]
                            row_level = str(row.get('level', '')).strip().lower()
                            if row_level != level.strip().lower():
                                continue

                        top_matches.append((i, score))
                        
                    print(f"--- [DEBUG] 5 Skor teratas: {top_matches} ---")
            except Exception as e:
                print(f"--- [DEBUG] ERROR saat memproses skor: {str(e)} ---")
                use_keyword_search = True

        if use_keyword_search:
            # ── Keyword/cold-start fallback: gunakan TF-IDF transform ─────────
            print(f"--- [DEBUG] Usecase: '{title}' tidak ditemukan, fallback ke keyword search ---")
            top_matches = self._keyword_search(title, df.copy(), level=level)
            if not top_matches:
                print("--- [DEBUG] Keyword search tidak menemukan hasil ---")
                return RecommendationBaseResponse(target_course=title, recommendations=[])

        # 3. Mapping ke DTO
        recommendations = []
        for i, score in top_matches:
            if i < len(df):
                row = df.iloc[i]
                rec_item = CourseRecommendationResponse(
                    id=int(row['id']),
                    title=str(row['title']),
                    cosine_score=round(float(score), 4),
                    category=str(row.get('category', 'N/A')),
                    skills=str(row.get('skills', 'N/A')),
                    level=str(row.get('level', 'N/A'))
                )
                recommendations.append(rec_item)
                print(f"--- [DEBUG] Added: {row['title']} (Score: {score:.4f}) ---")

        print(f"--- [DEBUG] Usecase: Mengembalikan {len(recommendations)} rekomendasi ---")
        return RecommendationBaseResponse(
            target_course=display_target,
            recommendations=recommendations
        )

    def retrain_and_reload(self) -> dict:
        """
        Menjalankan proses training ulang model (pembelajaran dari database terbaru)
        dan memuat ulang similarity matrix beserta vectorizer ke memori server (RAM).
        """
        from train_recommender import run_retrain
        from internal.wire.wire import reload_ml_components
        
        # 1. Jalankan training ulang model dengan MLflow tracking
        result = run_retrain()
        
        if result.get("status") == "success":
            # 2. Muat ulang model terbaru dari disk ke variabel global RAM
            reloaded = reload_ml_components()
            if reloaded:
                # 3. Sinkronkan reference model pada instance usecase saat ini
                from internal.wire.wire import _cosine_sim, _tfidf_vectorizer
                self.cosine_sim = _cosine_sim
                self.tfidf = _tfidf_vectorizer
                result["reloaded"] = True
                print("--- Usecase: Retrain dan reload model berhasil! ---")
            else:
                result["reloaded"] = False
                print("--- Usecase Warning: Model berhasil dilatih namun gagal di-reload ---")
        return result