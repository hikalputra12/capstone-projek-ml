# 🧠 BrainPath AI Engine - API Documentation

Dokumentasi ini menjelaskan seluruh API endpoint yang tersedia pada **BrainPath AI Engine**. Proyek ini menggunakan **FastAPI** untuk menyajikan layanan Machine Learning (Sistem Rekomendasi Kursus) dan AI (Chatbot Akademik dengan Strict Guardrails tanpa ChromaDB).

---

## 🌐 Informasi Server Utama

*   **Base URL Lokal:** `http://localhost:8001`
*   **Format Data:** `application/json`

### 🔌 Dokumentasi Interaktif (Interactive API Docs)
FastAPI secara otomatis menyediakan dokumentasi interaktif yang memungkinkan Anda menguji API secara langsung melalui browser ketika server sedang berjalan:
*   **Swagger UI (Sangat Direkomendasikan untuk Pengujian):** [http://localhost:8001/docs](http://localhost:8001/docs)
*   **ReDoc (Dokumentasi Terstruktur & Bersih):** [http://localhost:8001/redoc](http://localhost:8001/redoc)
*   **OpenAPI Schema (Raw JSON):** [http://localhost:8001/openapi.json](http://localhost:8001/openapi.json)

---

## 📊 Daftar API Endpoints

### 1. Sistem Rekomendasi Kursus (Course Recommendation API)

Memberikan daftar rekomendasi kursus terbaik berdasarkan kemiripan deskripsi dan materi dari judul kursus yang diinput oleh pengguna menggunakan teknik *Content-Based Filtering* (TF-IDF & Cosine Similarity).

Hanya menampilkan course yang berstatus dipublikasikan (`is_published = true`) secara konsisten.

*   **Endpoint:** `/api/v1/recommendations` atau `/recommendations`
*   **Method:** `GET`
*   **Headers:**
    ```http
    X-API-Key: brainpath_secret_token_change_me
    ```
*   **Query Parameters:**
    | Parameter | Tipe Data | Wajib | Deskripsi |
    | :--- | :--- | :--- | :--- |
    | `title` | `string` | **Ya** | Judul kursus yang ingin dicari rekomendasinya. |
    | `level` | `string` | Tidak | Filter rekomendasi berdasarkan level kursus (contoh: `pemula`, `menengah`, `mahir`). |

#### 📥 Contoh Request (cURL)
```bash
curl -X 'GET' \
  'http://localhost:8001/api/v1/recommendations?title=Dasar%20Pemrograman%20Python&level=pemula' \
  -H 'accept: application/json' \
  -H 'X-API-Key: brainpath_secret_token_change_me'
```

#### 📤 Contoh Response Sukses (`200 OK`)
```json
{
  "target_course": "Dasar Pemrograman Python",
  "recommendations": [
    {
      "id": 2,
      "title": "Python untuk Analisis Data",
      "cosine_score": 0.1578,
      "category": "Data Science",
      "skills": "Python, Pandas, NumPy, Data Analysis, Data Visualization",
      "level": "Pemula"
    },
    {
      "id": 3,
      "title": "Dasar Pemrograman Web",
      "cosine_score": 0.1293,
      "category": "Web Development",
      "skills": "HTML5, CSS3, JavaScript, Responsive Web Design",
      "level": "Pemula"
    }
  ]
}
```

*Keterangan Field Response:*
*   `target_course`: Judul kursus target yang dicocokkan oleh sistem.
*   `cosine_score`: Skor kemiripan antar-kursus (bernilai `0.0` s/d `1.0`). Semakin mendekati `1.0`, semakin mirip kursus tersebut dengan target.
*   `category`: Kategori kursus (misal: Programming, Data Science).
*   `skills`: Keterampilan utama yang dipelajari pada kursus tersebut.
*   `level`: Tingkat kesulitan/level kursus (contoh: Pemula, Menengah, Mahir).

*Catatan Perilaku Cold-Start (Keyword Search):*
*   Jika judul yang dimasukkan tidak cocok persis (exact match), sistem akan otomatis mengaktifkan pencarian kata kunci berbasis TF-IDF untuk mencari kursus terdekat yang mengandung kata kunci tersebut.

---

### 2. Chatbot AI Academic Assistant dengan Strict Guardrail

Mengajukan pertanyaan akademik ke Chatbot AI (BrainPath). Jawaban chatbot disintesis menggunakan Google Gemini AI (`gemini-2.5-flash`) dengan mengambil dokumen pendukung (konteks materi) langsung dari database PostgreSQL (`public.courses`) berdasarkan filter `course_id` atau `course_title` yang diberikan.

**Strict Title-Based Guardrail:** Chatbot **hanya boleh** menjawab pertanyaan yang relevan dengan ruang lingkup judul dan deskripsi course tersebut. Jika pertanyaan di luar konteks materi, AI akan secara otomatis menolak dengan sopan dan mengingatkan user untuk fokus pada materi yang sedang aktif.

*   **Endpoint:** `/api/v1/chatbot` atau `/chatbot`
*   **Method:** `POST`
*   **Headers:**
    ```http
    Content-Type: application/json
    X-API-Key: brainpath_secret_token_change_me
    ```

*Catatan Penting:* Parameter `course_id` dan `course_title` dikirim sebagai **Query Parameter** (di URL), sedangkan pertanyaan dikirim di **Request Body (JSON)**.

##### 📥 Query Parameters (URL)
| Parameter | Tipe Data | Wajib | Deskripsi |
| :--- | :--- | :--- | :--- |
| `course_id` | `integer` | Tidak | ID Kursus acuan yang sedang dipelajari (misal: `1`). |
| `course_title` | `string` | Tidak | Judul Kursus acuan jika ID tidak diketahui. |

##### 📥 Request Body (JSON)
| Field | Tipe Data | Wajib | Deskripsi |
| :--- | :--- | :--- | :--- |
| `user_question` | `string` | **Ya** | Pertanyaan akademik atau materi kuliah yang ingin ditanyakan. |

```json
{
  "user_question": "Jelaskan apa itu variabel dalam Python."
}
```

##### 📥 Contoh Request (cURL)
```bash
curl -X 'POST' \
  'http://localhost:8001/api/v1/chatbot?course_id=1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: brainpath_secret_token_change_me' \
  -d '{
  "user_question": "Jelaskan apa itu variabel dalam Python."
}'
```

##### 📤 Contoh Response Sukses (`200 OK`)
```json
{
  "status": "success",
  "data": {
    "question": "Jelaskan apa itu variabel dalam Python.",
    "answer": "Variabel dalam Python adalah nama yang diberikan untuk suatu lokasi memori yang digunakan untuk menyimpan nilai..."
  }
}
```

---

#### 🛡️ Contoh Pengujian Guardrail (Pertanyaan Melenceng/Di Luar Topik)

##### 📥 Request URL & Body
`POST http://localhost:8001/api/v1/chatbot?course_id=1`
```json
{
  "user_question": "Bagaimana cara memasak rendang?"
}
```

##### 📤 Response Penolakan Otomatis
```json
{
  "status": "success",
  "data": {
    "question": "Bagaimana cara memasak rendang?",
    "answer": "Maaf, saya didesain hanya untuk membantu Anda memahami materi Dasar Pemrograman Python. Mari fokus pada topik ini!"
  }
}
```

---

## ❌ Penanganan Error (Error Handling)

API menyajikan respons error yang terstandarisasi jika terjadi masalah pada request atau server:

### A. Parameter Tidak Valid (`422 Unprocessable Entity`)
Terjadi ketika payload yang dikirim tidak sesuai dengan skema DTO (misalnya kurang field wajib, atau salah tipe data).

```json
{
  "detail": [
    {
      "loc": ["body", "user_question"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### B. Kursus Tidak Ditemukan / Error Database
Terjadi jika ID Kursus atau Judul Kursus yang diajukan tidak ada di database `smart-education`.

```json
{
  "status": "error",
  "data": {
    "question": "Jelaskan materi ini",
    "answer": "Maaf, materi/kursus yang Anda pelajari tidak ditemukan di sistem."
  }
}
```

### C. Kesalahan Internal Server (`500 Internal Server Error`)
Terjadi ketika ada kesalahan pada model Machine Learning, koneksi database, atau `GOOGLE_API_KEY` (Gemini) belum diatur di file `.env`.

```json
{
  "detail": "Model Error: [Koneksi ke database gagal atau API Key tidak valid]"
}
```
