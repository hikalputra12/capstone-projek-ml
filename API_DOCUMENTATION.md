# 🧠 BrainPath AI Engine - API Documentation

Dokumentasi ini menjelaskan seluruh API endpoint yang tersedia pada **BrainPath AI Engine**. Proyek ini menggunakan **FastAPI** untuk menyajikan layanan Machine Learning (Sistem Rekomendasi Kursus) dan AI (Chatbot Akademik berbasis RAG).

---

## 🌐 Informasi Server Utama

*   **Base URL Lokal:** `http://localhost:8000`
*   **Format Data:** `application/json`

### 🔌 Dokumentasi Interaktif (Interactive API Docs)
FastAPI secara otomatis menyediakan dokumentasi interaktif yang memungkinkan Anda menguji API secara langsung melalui browser ketika server sedang berjalan:
*   **Swagger UI (Sangat Direkomendasikan untuk Pengujian):** [http://localhost:8000/docs](http://localhost:8000/docs)
*   **ReDoc (Dokumentasi Terstruktur & Bersih):** [http://localhost:8000/redoc](http://localhost:8000/redoc)
*   **OpenAPI Schema (Raw JSON):** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## 📊 Daftar API Endpoints

### 1. Sistem Rekomendasi Kursus (Course Recommendation API)
Memberikan daftar rekomendasi kursus terbaik berdasarkan kemiripan deskripsi dan materi dari judul kursus yang diinput oleh pengguna menggunakan teknik *Content-Based Filtering* (TF-IDF & Cosine Similarity).

*   **Endpoint:** `/api/v1/recommend`
*   **Method:** `GET`
*   **Query Parameters:**
    | Parameter | Tipe Data | Wajib | Deskripsi |
    | :--- | :--- | :--- | :--- |
    | `title` | `string` | **Ya** | Judul kursus yang ingin dicari rekomendasinya. |

#### 📥 Contoh Request (cURL)
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/recommend?title=Belajar%20Python' \
  -H 'accept: application/json'
```

#### 📤 Contoh Response Sukses (`200 OK`)
```json
{
  "target_course": "Belajar Python",
  "recommendations": [
    {
      "id": 12,
      "title": "Python untuk Analisis Data",
      "cosine_score": 0.8421,
      "category": "Data Science",
      "skills": "Python, Pandas, NumPy, Data Analysis"
    },
    {
      "id": 15,
      "title": "Dasar Pemrograman Web",
      "cosine_score": 0.312,
      "category": "Web Development",
      "skills": "HTML, CSS, JavaScript"
    }
  ]
}
```

*Keterangan Field Response:*
*   `target_course`: Judul kursus target yang dicocokkan oleh sistem.
*   `cosine_score`: Skor kemiripan antar-kursus (bernilai `0.0` s/d `1.0`). Semakin mendekati `1.0`, semakin mirip kursus tersebut dengan target.

---

### 2. Chatbot AI Academic Assistant - RAG (API BARU 🚀)
Mengajukan pertanyaan akademik ke Chatbot AI (BrainPath). Jawaban chatbot disintesis menggunakan Google Gemini AI dengan mengambil dokumen pendukung (konteks materi) dari Vector Database (ChromaDB) sesuai dengan filter ID Kursus yang diberikan (`sourcesID`).

*   **Endpoint:** `/api/v1/chat/ask`
*   **Method:** `POST`
*   **Headers:**
    ```http
    Content-Type: application/json
    ```

#### 📥 Request Body (JSON)
| Field | Tipe Data | Wajib | Deskripsi |
| :--- | :--- | :--- | :--- |
| `question` | `string` | **Ya** | Pertanyaan akademik atau materi kuliah yang ingin ditanyakan. |
| `sourcesID` | `integer` | **Ya** | ID Kursus acuan yang digunakan AI untuk mencari konteks/materi yang relevan. |

```json
{
  "question": "Jelaskan konsep dasar tentang variabel dalam Python!",
  "sourcesID": 1
}
```

#### 📥 Contoh Request (cURL)
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/chat/ask' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "Jelaskan konsep dasar tentang variabel dalam Python!",
  "sourcesID": 1
}'
```

#### 📤 Contoh Response Sukses (`200 OK`)
```json
{
  "status": "success",
  "data": {
    "question": "Jelaskan konsep dasar tentang variabel dalam Python!",
    "answer": "Dalam pemrograman Python, variabel adalah nama atau label yang digunakan untuk merujuk ke suatu lokasi memori yang menyimpan data. Anda bisa membayangkan variabel seperti sebuah wadah yang diberi label. Anda dapat memasukkan nilai (seperti angka atau teks) ke dalam wadah tersebut dan mengubah isinya kapan saja. Di Python, Anda tidak perlu mendeklarasikan tipe data variabel secara eksplisit; cukup gunakan tanda sama dengan (=) untuk mengisi nilai, contohnya: `nama = 'Budi'` atau `umur = 20`."
  }
}
```

*Catatan Perilaku AI (Constraints):*
*   Jika pertanyaan yang diajukan **sama sekali tidak dibahas** atau tidak dapat disimpulkan dari data materi kursus dengan `sourcesID` terkait di database, AI akan secara otomatis membalas dengan pesan aman:
    > *"Maaf, materi terkait pertanyaan tersebut belum tersedia di BrainPath saat ini."*

---

## ❌ Penanganan Error (Error Handling)

API menyajikan respons error yang terstandarisasi jika terjadi masalah pada request atau server:

### A. Parameter Tidak Valid (`422 Unprocessable Entity`)
Terjadi ketika payload yang dikirim tidak sesuai dengan skema DTO (misalnya kurang field wajib, atau salah tipe data).

*   **Contoh Response:**
    ```json
    {
      "detail": [
        {
          "loc": ["body", "sourcesID"],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }
    ```

### B. Kesalahan Internal Server / Model / API Key (`500 Internal Server Error`)
Terjadi ketika ada kesalahan pada model Machine Learning, koneksi database, atau `GOOGLE_API_KEY` (Gemini) belum diatur di file `.env`.

*   **Contoh Response:**
    ```json
    {
      "detail": "Model Error: [Gemini API Key is invalid or missing]"
    }
    ```

---

## 🚀 Cara Menjalankan Server untuk Pengujian API

1.  Pastikan semua dependensi sudah terinstal:
    ```bash
    pip install -r requirements.txt
    ```
2.  Pastikan file `.env` sudah dikonfigurasi dengan benar (termasuk koneksi database PostgreSQL dan API Key Gemini):
    ```env
    DATABASE_NAME=capstone_db
    DATABASE_USERNAME=postgres
    DATABASE_PASSWORD=yourpassword
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    GOOGLE_API_KEY=AIzaSy...
    ```
3.  Jalankan server:
    ```bash
    python main.py
    ```
4.  Buka browser Anda dan kunjungi `http://localhost:8000/docs` untuk mulai menguji!
