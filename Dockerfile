# Gunakan image Python resmi yang ringan
FROM python:3.11-slim

# Atur working directory di dalam container
WORKDIR /app

# Install dependensi sistem yang dibutuhkan oleh psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt
COPY requirements.txt .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code ke dalam container
COPY . .

# Hugging Face menggunakan port default 7860 untuk Spaces
ENV PORT=7860
EXPOSE 7860

# Jalankan retrain model terlebih dahulu untuk sinkronisasi database, lalu jalankan server utama
CMD ["sh", "-c", "python train_recommender.py && python main.py"]
