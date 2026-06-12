from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pkg.utils.config import settings

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    secret_key = settings.API_KEY_SECRET
    if not secret_key:
        # Jika belum dikonfigurasi di .env, loloskan agar tidak terjadi error fatal saat belum di-setup
        print("--- WARNING: API_KEY_SECRET is not configured in .env! API is unprotected. ---")
        return None
        
    if api_key != secret_key:
        raise HTTPException(
            status_code=403,
            detail="Akses Ditolak: API Key tidak valid atau tidak disertakan di header X-API-Key."
        )
    return api_key
