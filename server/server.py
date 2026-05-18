from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager 

# Import router untuk Rekomendasi dan Chatbot
from internal.adaptor.recomendation import router as course_handler 
from internal.adaptor.chat import router as chat_handler 

# Import wiring untuk memuat semua model (Cosine Sim & Gemini/ChromaDB)
from internal.wire.wire import load_ml_components
from pkg.utils.logger import init_logger 

# Inisialisasi logger
log = init_logger("logs/", debug=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Kode di sini dijalankan SAAT STARTUP ---
    try:
        log.info("Memulai inisialisasi komponen Machine Learning (Rekomendasi & Chatbot)...")
        # load_ml_components sekarang memuat model joblib DAN ChatUsecase Gemini
        load_ml_components()
        log.info("Semua komponen ML berhasil dimuat ke memori.")
    except Exception as e:
        log.error("Gagal memuat komponen ML", extra={"error": str(e)})
    
    yield # Server berjalan di sini
    
    # --- Kode di sini dijalankan SAAT SHUTDOWN ---
    log.info("Mematikan server AI, membersihkan resource...")

def create_app() -> FastAPI:
    app = FastAPI(
        title="BrainPath AI Engine",
        description="API untuk Sistem Rekomendasi Kursus dan Chatbot Akademik berbasis RAG",
        version="1.0.0",
        lifespan=lifespan 
    )

    # Konfigurasi CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #Daftarkan router untuk rekomendasi course
    app.include_router(course_handler, prefix="/api/v1")
    
    # Daftarkan router untuk Chatbot AI Gemini
    # Ini akan membuat endpoint: /api/v1/chat/ask
    app.include_router(chat_handler, prefix="/api/v1/chat", tags=["Chatbot"])

    @app.get("/")
    def root():
        log.debug("Root endpoint diakses")
        return {
            "message": "Welcome to BrainPath AI Engine",
            "features": ["Course Recommendation", "AI Chatbot Assistant"]
        }

    app.state.logger = log
    log.info("Aplikasi FastAPI berhasil dibuat.")
    
    return app