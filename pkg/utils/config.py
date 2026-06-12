import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    
    # Tambahkan baris ini yang sebelumnya terlewat
    DATABASE_SSL_MODE = os.getenv("DATABASE_SSL_MODE", "disable") 

    # Database Pool
    DATABASE_MAX_CONN = os.getenv("DATABASE_MAX_CONN", 5)
    DATABASE_MAX_IDLE_CONN = os.getenv("DATABASE_MAX_IDLE_CONN", 5)
    DATABASE_MAX_OPEN_CONN = os.getenv("DATABASE_MAX_OPEN_CONN", 10)

    # Kunci API Google 
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # API Key untuk mengamankan API publik
    API_KEY_SECRET = os.getenv("API_KEY_SECRET")

settings = Settings()
