#kode ini berisi setup untuk server FastAPI, termasuk konfigurasi CORS, routing, dan lifecycle events untuk startup dan shutdown. Pada bagian startup, kita akan memuat komponen Machine Learning yang diperlukan ke dalam memori agar siap digunakan saat menerima request rekomendasi course. Pada bagian shutdown, kita bisa menambahkan logika untuk membersihkan resource jika diperlukan.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager 
from internal.adaptor.recomendation import router as course_handler 
from internal.wire.wire import load_ml_components
from pkg.utils.logger import init_logger 

# Inisialisasi logger di luar agar bisa diakses global di file ini
log = init_logger("logs/", debug=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Kode di sini dijalankan SAAT STARTUP ---
    try:
        log.info("Memulai inisialisasi komponen Machine Learning...")
        load_ml_components()
        log.info("Komponen ML berhasil dimuat ke memori.")
    except Exception as e:
        log.error("Gagal memuat komponen ML", extra={"error": str(e)})
    
    yield # Server berjalan di sini
    
    # --- Kode di sini dijalankan SAAT SHUTDOWN ---
    log.info("Mematikan server AI, membersihkan resource...")

def create_app() -> FastAPI:
    app = FastAPI(
        title="Course Recommendation API",
        description="API untuk sistem rekomendasi kursus berbasis Content-Based Filtering",
        version="1.0.0",
        lifespan=lifespan # mwendaftarkan lifepan untuk startup/shutdown events
    )

    # Konfigurasi CORS (Cross-Origin Resource Sharing)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Daftarkan router untuk rekomendasi course
    app.include_router(course_handler, prefix="/api/v1")

    @app.get("/")
    def root():
        log.debug("Root endpoint diakses")
        return {"message": "Welcome to Course Recommendation API"}

    app.state.logger = log
    log.info("Aplikasi FastAPI berhasil dibuat.")
    
    return app