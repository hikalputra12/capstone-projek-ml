from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.adaptor.recomendation import router as course_handler # Pastikan kamu sudah buat handler-nya
from internal.wire.wire import load_ml_components

def create_app() -> FastAPI:
    app = FastAPI(
        title="Course Recommendation API",
        description="API untuk sistem rekomendasi kursus berbasis Content-Based Filtering",
        version="1.0.0"
    )

    # Konfigurasi CORS (Penting untuk akses dari Frontend/Postman)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Load Model ML saat Server Inisialisasi
    load_ml_components()

    # Daftarkan Router (Delivery)
    app.include_router(course_handler, prefix="/api/v1")

    @app.get("/")
    def root():
        return {"message": "Welcome to Course Recommendation API"}

    return app