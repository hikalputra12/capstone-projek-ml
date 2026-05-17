import os
import pandas as pd

# Import library LangChain terbaru
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Modul lokal
from pkg.database.postgress import engine

# Lokasi folder ChromaDB
DB_DIR = "pkg/ml-models/chroma_db"


def run_sync():
    print("--- [SYNC] Memulai ekstraksi materi dari PostgreSQL ke ChromaDB ---")

    # Ambil data materi menggunakan engine
    # Query disesuaikan dengan skema tabel terbaru
    query = "SELECT id, title, content FROM courses WHERE content IS NOT NULL"

    try:
        df = pd.read_sql(query, engine)
    except Exception as e:
        print(f"[ERROR] Gagal membaca database: {str(e)}")
        return

    if df.empty:
        print("[WARNING] Tidak ada materi ditemukan. Pastikan tabel 'courses' sudah terisi kolom 'content'.")
        return

    # Proses Chunking (Memotong teks panjang agar LLM tidak bingung)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    all_texts = []
    all_metadatas = []

    for _, row in df.iterrows():
        # Gabungkan judul dan konten untuk memperkaya konteks pencarian
        text_content = f"Kursus: {row['title']}\nMateri: {row['content']}"
        chunks = text_splitter.split_text(text_content)

        all_texts.extend(chunks)
        # Simpan course_id sebagai metadata agar kita tahu sumbernya
        all_metadatas.extend([{"course_id": str(row['id'])}] * len(chunks))

    # Embedding (Ubah teks jadi angka menggunakan model lokal)
    print(f"--- [SYNC] Memproses {len(all_texts)} potongan teks (Embedding) ---")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Simpan ke ChromaDB (Vector Store)
    vector_db = Chroma.from_texts(
        texts=all_texts,
        embedding=embeddings,
        metadatas=all_metadatas,
        persist_directory=DB_DIR
    )

    print(f"--- [SYNC] Selesai! Database vektor disimpan di {DB_DIR} ---")


if __name__ == "__main__":
    run_sync()