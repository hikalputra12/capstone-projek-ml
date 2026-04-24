#kode ini adalah entry point utama untuk menjalankan server FastAPI. Di sini kita menggunakan uvicorn sebagai ASGI server untuk menjalankan aplikasi FastAPI yang sudah kita buat di dalam server/server.py. Dengan menggunakan factory function, kita bisa memastikan bahwa setiap kali server dijalankan, aplikasi akan dibuat ulang dengan konfigurasi terbaru, termasuk logger yang sudah diatur dengan benar.

import uvicorn
import os

if __name__ == "__main__":
    
    uvicorn.run(
        "server.server:create_app", # Langsung panggil factory function-nya
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        factory=True #memberitau uvicorn bahwa ini adalah factory function
    )