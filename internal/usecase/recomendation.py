from internal.data.repository.course import CourseRepository
from internal.data.dto.course import RecommendationBaseResponse, CourseRecommendationResponse

class CourseUsecase:
    def __init__(self, repo: CourseRepository, cosine_sim):
        """
        Inisialisasi Usecase.
        cosine_sim: matriks hasil load joblib (numpy array)
        """
        self.repo = repo
        self.cosine_sim = cosine_sim

    def get_recommendations(self, title: str) -> RecommendationBaseResponse:
        # 1. Tarik semua data dari DB
        df = self.repo.get_all_courses_dataframe()
        
        if df.empty:
            print("--- [DEBUG] Usecase: Database kosong! ---")
            return None

        if self.cosine_sim is None:
            print("--- [DEBUG] Usecase: Matriks Cosine Similarity NULL! ---")
            return None

        # 2. Cari indeks berdasarkan judul (Case-insensitive & strip)
        target_title = title.strip().lower()
        df_search = df['title'].str.strip().str.lower()
        
        try:
            # Mencari indeks baris yang cocok
            idx = df[df_search == target_title].index[0]
            print(f"--- [DEBUG] Usecase: Target '{title}' ditemukan di indeks {idx} ---")
        except IndexError:
            print(f"--- [DEBUG] Usecase: Judul '{title}' tidak ditemukan di database ---")
            return None

        # 3. Proses Skor Similarity
        try:
            # Pastikan idx tidak melebihi ukuran matriks
            if idx >= len(self.cosine_sim):
                print(f"--- [DEBUG] ERROR: Indeks {idx} di luar jangkauan matriks (size: {len(self.cosine_sim)}) ---")
                return None

            # Ambil skor untuk baris ke-idx
            raw_scores = self.cosine_sim[idx]
            
            # Ubah ke list of tuples (index, score)
            sim_scores = list(enumerate(raw_scores))
            
            # Urutkan berdasarkan skor terbesar (descending)
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Ambil peringkat 2 sampai 6 (melewati diri sendiri)
            top_matches = sim_scores[1:6]
            print(f"--- [DEBUG] Usecase: 5 Skor teratas: {top_matches} ---")

        except Exception as e:
            print(f"--- [DEBUG] ERROR saat memproses skor: {str(e)} ---")
            return None

        # 4. Mapping ke DTO
        recommendations = []
        for i, score in top_matches:
            # Pastikan i ada di dalam dataframe
            if i < len(df):
                row = df.iloc[i]
                
                # CRITICAL: Pastikan semua data diconvert ke tipe data Python standar (str/float)
                # Pydantic/FastAPI sering gagal validasi jika tipenya numpy.float64
                rec_item = CourseRecommendationResponse(
                    title=str(row['title']),
                    cosine_score=round(float(score), 4),
                    level=str(row.get('level', 'N/A')),
                    skills=str(row.get('skills', 'N/A'))
                )
                recommendations.append(rec_item)
                print(f"--- [DEBUG] Added: {row['title']} (Score: {score}) ---")

        # 5. Return Response
        print(f"--- [DEBUG] Usecase: Berhasil mengembalikan {len(recommendations)} rekomendasi ---")
        return RecommendationBaseResponse(
            target_course=str(df.iloc[idx]['title']),
            recommendations=recommendations
        )