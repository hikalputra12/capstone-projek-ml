import uvicorn
from server.server import create_app

# Inisialisasi aplikasi
app = create_app()

if __name__ == "__main__":
    # Menjalankan server menggunakan uvicorn
    # host 0.0.0.0 agar bisa diakses dari jaringan lokal/Fedora
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True # Otomatis restart saat ada perubahan kode
    )