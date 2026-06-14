---
title: BrainPath AI - Course Recommendation & Chatbot Engine
emoji: 🧠
colorFrom: indigo
colorTo: pink
sdk: docker
pinned: false
---

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
# APP ENVIRONMENT
APP_ENV=local

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

# API Key untuk mengamankan API publik (Header: X-API-Key)
API_KEY_SECRET=8f9a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a

# MLFLOW CONFIGURATION (Opsional, default menggunakan sqlite lokal & direktori ./mlruns)
MLFLOW_TRACKING_URI=
MLFLOW_EXPERIMENT_NAME=course-recommender
MLFLOW_RUN_NAME=content-based-filtering
```

---

## 🏃 Cara Menjalankan Sistem

### Langkah Pertama: Sinkronisasi / Pelatihan Ulang Model ML
Sebelum menjalankan server, model rekomendasi perlu dilatih untuk pertama kali agar file `.joblib` terbentuk di dalam direktori `pkg/ml-models/`. Proses ini akan otomatis mencatat parameter dan metrik ke MLflow:
```bash
python train_recommender.py
```

### Langkah Kedua: Jalankan Server API FastAPI
Jalankan entrypoint server utama menggunakan server ASGI Uvicorn:
```bash
python main.py
```
Aplikasi akan aktif dan mendengarkan permintaan pada port **8001** (atau port yang diset di env `PORT`): `http://localhost:8001`

### Langkah Ketiga: Jalankan MLflow UI (Opsional)
Untuk melihat visualisasi eksperimen, parameter, metrik, dan artifact model secara grafis, jalankan server MLflow UI lokal:
```bash
mlflow ui --port 5000
```
Setelah berjalan, Anda dapat mengakses dashboard MLflow di browser melalui alamat: [http://localhost:5000](http://localhost:5000)

---

## 📊 Daftar API Endpoints Ringkas

> [!IMPORTANT]  
> Semua request ke endpoint API **wajib** menyertakan header berikut demi keamanan:  
> *   **Header Key:** `X-API-Key`  
> *   **Header Value:** *[Nilai dari API_KEY_SECRET di `.env` Anda]*

| Fitur | Endpoint | Method | Parameter | Deskripsi |
| :--- | :--- | :--- | :--- | :--- |
| **Rekomendasi Kursus** | `/api/v1/recommendations` | `GET` | `title` (Wajib), `level` (Opsional) | Rekomendasi kursus serupa berdasarkan judul, opsional difilter berdasarkan level (pemula, menengah, mahir). |
| **AI Chatbot Akademik** | `/api/v1/chatbot` | `POST` | `course_id` (Query/Opsional), `course_title` (Query/Opsional), `user_question` (Body/Wajib) | Chatbot akademik ber-guardrail ketat. |
| **Retrain Model ML** | `/api/v1/recommendations/retrain` | `POST` | None | Memicu training ulang model rekomendasi dengan data terpublikasi terbaru, reload model ke memori server secara real-time, dan track ke MLflow. |
| **Health Check (Public)** | `/healthz` | `GET` | None | Mengecek kesehatan aplikasi dan memicu query `SELECT 1` ke Neon Database agar tidak masuk mode suspend (cold start). |


> [!TIP]
> Untuk dokumentasi endpoint secara super detail beserta skema JSON, contoh request cURL, response sukses, dan error handling, silakan merujuk langsung ke file dokumentasi khusus: **[api_documentations.md](file:///c:/Users/Julianda/capstone-projek-ml-1/api_documentations.md)**.

---

## ⚡ Mencegah Cold Start (Hugging Face & Neon)

Layanan **Hugging Face Spaces** (tipe free) dan serverless **Neon Database** memiliki fitur otomatis masuk ke mode tidur (*suspend/sleep*) jika tidak menerima request dalam jangka waktu tertentu (biasanya 5–10 menit untuk Neon, dan 48 jam untuk Hugging Face). Ketika ada request baru setelah itu, sistem akan mengalami *cold start* (tertunda 5–15 detik).

Untuk mencegah *cold start*, sistem ini dilengkapi dengan solusi otomatis:

1. **Endpoint Health Check**: Tersedia endpoint publik `/healthz` yang secara aktif mengirim query `SELECT 1` ke Neon Database untuk menjaga database tetap bangun.
2. **GitHub Actions Scheduler**: Workflow [.github/workflows/keep_alive.yml](file:///.github/workflows/keep_alive.yml) dikonfigurasi untuk melakukan *ping* (curl) ke URL Hugging Face Space Anda **setiap 24 jam** secara otomatis untuk mencegah Hugging Face masuk ke mode tidur.
3. **Alternatif Pihak Ketiga (Sangat Direkomendasikan untuk Neon)**: Karena *cron job* GitHub Actions berjalan setiap 24 jam dan database Neon memiliki waktu suspend yang cepat (10 menit), Anda sangat disarankan mendaftarkan URL space Anda (`https://hero1012-brainpath-ai-engine.hf.space/healthz`) ke layanan monitoring gratis seperti **[cron-job.org](https://cron-job.org/)** atau **[UptimeRobot](https://uptimerobot.com/)** dengan interval pemeriksaan setiap **5–10 menit** jika ingin database Neon tidak mengalami cold start sama sekali.

---

## 🧠 Teknologi Utama
*   **Web API Framework**: FastAPI
*   **Machine Learning**: Scikit-Learn (TF-IDF & Cosine Similarity), Joblib, Pandas
*   **AI Integration**: LangChain Google GenAI (Gemini AI API)
*   **Database ORM**: SQLAlchemy, Psycopg2-binary, PostgreSQL
*   **Logger System**: Python JSON Logger (terstruktur di folder `logs/`)