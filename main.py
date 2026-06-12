#kode ini adalah entry point utama untuk menjalankan server FastAPI. Di sini kita menggunakan uvicorn sebagai ASGI server untuk menjalankan aplikasi FastAPI yang sudah kita buat di dalam server/server.py. Dengan menggunakan factory function, kita bisa memastikan bahwa setiap kali server dijalankan, aplikasi akan dibuat ulang dengan konfigurasi terbaru, termasuk logger yang sudah diatur dengan benar.

import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    # Mengambil PORT dari environment variable (default 8001 jika lokal)
    port = int(os.getenv("PORT", 8001))
    
    # Reload hanya aktif jika APP_ENV = local atau development
    app_env = os.getenv("APP_ENV", "local")
    is_development = app_env in ["local", "development"]
    
    uvicorn.run(
        "server.server:create_app", # Langsung panggil factory function-nya
        host="0.0.0.0", 
        port=port, 
        reload=is_development,
        factory=True # memberitahu uvicorn bahwa ini adalah factory function
    )