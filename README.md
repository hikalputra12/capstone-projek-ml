# BrainPath AI - Course Recommendation System

Sistem rekomendasi kursus berbasis Machine Learning yang dikembangkan menggunakan **FastAPI** dan **PostgreSQL**. Projek ini merupakan bagian dari sistem edukasi cerdas yang memberikan rekomendasi konten pembelajaran berdasarkan kemiripan deskripsi dan kategori kursus.

## 🚀 Fitur Utama
- **Content-Based Filtering**: Menggunakan TF-IDF Vectorizer dan Cosine Similarity untuk menghitung tingkat kemiripan antar kursus.
- **Dynamic Retraining**: Skrip otomatis untuk melatih ulang model berdasarkan data terbaru dari database.
- **Clean Architecture**: Implementasi pola desain Repository dan Usecase untuk kemudahan pemeliharaan kode.
- **Logging & Monitoring**: Sistem logging terintegrasi untuk melacak aktivitas API dan error.

## 📁 Struktur Folder
```text
.
├── internal/
│   ├── adaptor/      # Handler API (Endpoint)
│   ├── usecase/      # Logika bisnis sistem rekomendasi
│   ├── data/         # Repository, DTO, dan Entity (Database)
│   └── wire/         # Dependency Injection logic
├── pkg/
│   ├── database/     # Konfigurasi koneksi PostgreSQL
│   ├── ml-models/    # Penyimpanan model .joblib
│   └── utils/        # Logger dan konfigurasi sistem
├── main.py           # Entry point aplikasi
├── retrain_model.py  # Skrip retraining model ML
└── requirements.txt  # Daftar dependensi Python
```
## 🛠️ Persiapan dan Instalasi
### 1. Prasyarat
* Python 3.10+

* PostgreSQL

### 2. Instalasi Dependensi
Clone repositori ini dan instal semua library yang diperlukan:
```
pip install -r requirements.txt
```
### 3. Konfigurasi Environment
Buat file ```.env ``` di direktori utama dan sesuaikan konfigurasinya:

```
DATABASE_NAME=nama_db_anda
DATABASE_USERNAME=user_anda
DATABASE_PASSWORD=password_anda
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_SSL_MODE=disable
```

## 🏃 Cara Menjalankan

### Melatih Model (Retrain)
Sistem memerlukan file model .joblib untuk bekerja. Jalankan perintah berikut untuk mengekstraksi data dari database dan melatih model:

```
python retrain_model.py
```

### Menjalankan Server API
Jalankan aplikasi menggunakan server Uvicorn:
```
python main.py
```

Server akan berjalan di: ```http://localhost:8000```

## 📊 API Endpoints

### Get Recommendation
Memberikan daftar rekomendasi kursus berdasarkan judul kursus yang dicari.

* Endpoint: ```/api/v1/recommend```

* Method: ```GET```

* Query Parameter: ```title (string)```

* Contoh: ```GET /api/v1/recommend?title=Belajar%20Python```

## 🧠 Teknologi yang Digunakan
* Framework: ```FastAPI```

* Machine Learning: ```Scikit-learn (TF-IDF & Cosine Similarity)```

* Database: ```PostgreSQL``` 

* Tools: ```Pandas, Joblib, Python-Dotenv```