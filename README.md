# BrainPath AI - Course Recommendation & Chatbot Engine

Sistem rekomendasi kursus berbasis Machine Learning (**Content-Based Filtering**) dan AI Chatbot yang dikembangkan menggunakan **FastAPI** dan **PostgreSQL**. Projek ini dirancang sebagai mesin kecerdasan buatan utama untuk platform edukasi cerdas **BrainPath** guna memberikan rekomendasi konten pembelajaran presisi serta bimbingan akademik interaktif.

---

## 🚀 Fitur Utama

- **Content-Based Filtering**: Menggunakan TF-IDF Vectorizer dan Cosine Similarity untuk menghitung tingkat kemiripan antar-kursus berdasarkan fitur teks (`title`, `category`, `description`, `skills`, `summary`).
- **Dynamic Re-Training & Sync**: Skrip `train_recommender.py` otomatis menyelaraskan model ML dengan data terbaru dari database PostgreSQL secara presisi, hanya menggunakan kursus yang sudah dipublikasikan (`is_published = true`) terurut `id ASC` agar terhindar dari bias indeks (*index mismatch*).
- **Strict Guardrail AI Chatbot (Tanpa ChromaDB / RAG)**: Mengintegrasikan Google Gemini AI (`gemini-2.5-flash`) dengan pembatas ketat berdasarkan metadata kursus di database. Sistem mendeteksi materi yang sedang dipelajari dan menolak dengan sopan pertanyaan di luar materi kelas untuk menjaga fokus belajar.
- **Backward Compatibility**: Semua endpoint mendukung skema request & response baru dan lama demi kelancaran integrasi dengan klien/frontend tanpa modifikasi kode di sisi klien.
- **Clean Architecture Onion Pattern**: Implementasi pemisahan tanggung jawab yang rapi antara `adaptor` (handler API), `usecase` (logika bisnis), `data` (entity/repository/DTO), dan `wire` (dependency injection).

---

## 📁 Struktur Folder Proyek

```text
.
├── internal/
│   ├── adaptor/            # Handler API (FastAPI Router Endpoints)
│   ├── usecase/            # Logika bisnis (Rekomendasi & Chatbot Guardrails)
│   ├── data/
│   │   ├── dto/            # Data Transfer Object (Skema Request & Response)
│   │   ├── entity/         # Definisi model tabel ORM SQLAlchemy
│   │   └── repository/     # Logika penarikan database PostgreSQL (SQLAlchemy)
│   └── wire/               # Dependency injection logic (wiring)
├── pkg/
│   ├── database/           # Konfigurasi pool koneksi PostgreSQL
│   ├── ml-models/          # Penyimpanan model hasil training (.joblib)
│   └── utils/              # Logger JSON terstruktur dan konfigurasi .env
├── api_documentations.md   # Referensi endpoint API lengkap beserta contoh seeding mock data
├── train_recommender.py    # Skrip sinkronisasi / melatih ulang model rekomendasi ML
├── retrain_model.py        # Skrip pembungkus pelatihan model untuk backward-compatibility
├── main.py                 # Entry point aplikasi FastAPI
├── requirements.txt        # Daftar dependensi modul Python
└── .env                    # Variabel environment (Kredensial database & Gemini API)
```

---

## 🛠️ Persiapan dan Instalasi

### 1. Prasyarat Sistem
*   Python 3.10 ke atas
*   PostgreSQL Database Server yang berjalan secara lokal atau cloud

### 2. Instalasi Dependensi
Silakan pasang seluruh pustaka Python yang diperlukan:
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi Lingkungan (`.env`)
Buat file bernama `.env` pada direktori utama proyek dan masukkan konfigurasi kredensial database Anda beserta API Key Google Gemini:
```env
# DATABASE CONNECTION
DATABASE_NAME=smart-education
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=password_anda
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_SSL_MODE=disable

# DATABASE POOL
DATABASE_MAX_CONN=5
DATABASE_MAX_IDLE_CONN=5
DATABASE_MAX_OPEN_CONN=10

# GOOGLE AI STUDIO API KEY (GEMINI)
GOOGLE_API_KEY=AIzaSy...
```

---

## 🏃 Cara Menjalankan Sistem

### Langkah Pertama: Sinkronisasi / Pelatihan Ulang Model ML
Sebelum menjalankan server, model rekomendasi perlu dilatih untuk pertama kali agar file `.joblib` terbentuk di dalam direktori `pkg/ml-models/`:
```bash
python train_recommender.py
```

### Langkah Kedua: Jalankan Server API FastAPI
Jalankan entrypoint server utama menggunakan server ASGI Uvicorn:
```bash
python main.py
```
Aplikasi akan aktif dan mendengarkan permintaan pada port **8001**: `http://localhost:8001`

---

## 📊 Daftar API Endpoints Ringkas

| Fitur | Endpoint | Method | Parameter | Deskripsi |
| :--- | :--- | :--- | :--- | :--- |
| **Rekomendasi Kursus** | `/api/v1/recommendations` | `GET` | `title` | Rekomendasi kursus serupa berdasarkan judul. |
| **AI Chatbot Akademik** | `/api/v1/chatbot` | `POST` | `course_id` (Query), `user_question` (Body) | Chatbot akademik ber-guardrail ketat. |


> [!TIP]
> Untuk dokumentasi endpoint secara super detail beserta skema JSON, contoh request cURL, response sukses, dan error handling, silakan merujuk langsung ke file dokumentasi khusus: **[api_documentations.md](file:///home/haikal/capstone-projek-ml/api_documentations.md)**.

---

## 🧠 Teknologi Utama
*   **Web API Framework**: FastAPI
*   **Machine Learning**: Scikit-Learn (TF-IDF & Cosine Similarity), Joblib, Pandas
*   **AI Integration**: LangChain Google GenAI (Gemini AI API)
*   **Database ORM**: SQLAlchemy, Psycopg2-binary, PostgreSQL
*   **Logger System**: Python JSON Logger (terstruktur di folder `logs/`)