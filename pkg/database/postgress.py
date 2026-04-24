import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pkg.utils.config import settings

# Setup Logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Inisialisasi Base
# Ini digunakan oleh semua file di folder 'internal/data/entity/'
Base = declarative_base()

def init_db():
    """
    Menginisialisasi koneksi ke PostgreSQL berdasarkan konfigurasi dari .env
    """
    # Mengambil DSN dari settings
    conn_str = (
        f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@"
        f"{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
        f"?sslmode={settings.DATABASE_SSL_MODE}"
    )

    try:
        # Create Engine dengan Pool Settings 
        engine = create_engine(
            conn_str,
            pool_size=int(settings.DATABASE_MAX_OPEN_CONN),      # Jumlah koneksi standby
            max_overflow=int(settings.DATABASE_MAX_CONN),        # Koneksi tambahan jika penuh
            pool_recycle=3600,                                   # Refresh koneksi setiap 1 jam
            pool_timeout=30,                                     # Timeout menunggu koneksi (detik)
            echo=False,                                          # Set True jika ingin log SQL sangat detail
            future=True
        )

        # Test Koneksi Awal
        with engine.connect() as conn:
            print("--- Database: Successfully connected to PostgreSQL ---")
        
        # SessionMaker untuk membuat session setiap ada request
        session_local = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=engine
        )
        
        return engine, session_local

    except Exception as e:
        print(f"--- Database ERROR: Could not connect! ---")
        print(f"Error Detail: {str(e)}")
        sys.exit(1)

# Eksekusi Inisialisasi secara Global
# Agar variabel 'engine' dan 'SessionLocal' bisa di-import oleh file lain
try:
    engine, SessionLocal = init_db()
except Exception:
    # Handle jika ada error saat inisialisasi di luar fungsi
    sys.exit(1)

# Generator get_db untuk FastAPI Dependency Injection
def get_db():
    """
    Fungsi ini akan dipanggil oleh wire.py untuk menyuntikkan 
    session database ke repository.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Menutup koneksi secara otomatis setelah request selesai
        db.close()