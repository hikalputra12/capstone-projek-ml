# Import Core & Community
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from pkg.utils.config import settings
from internal.data.dto.chat import ChatRequest, ChatResponse, ChatResponseData


class ChatUsecase:
    def __init__(self):
        # Embedding Lokal
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Database Vektor ChromaDB
        db_path = "pkg/ml-models/chroma_db2"
        self.vector_db = Chroma(
            persist_directory=db_path, 
            embedding_function=self.embeddings
        )
        
        # LLM Gemini
        api_key = settings.GOOGLE_API_KEY
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0
        )
        
        # Prompt Engineering
        template = """
        Anda adalah BrainPath, seorang Asisten Akademik AI yang cerdas, interaktif, dan edukatif. Tugas Anda adalah membantu pengguna memahami materi kuliah atau kursus dengan penjelasan yang jernih.

        [DETAIL MATERI SAAT INI]
        - Judul Materi/Video: {course_title}
        - Deskripsi: {course_description}
        - Tingkat Kesulitan (Level): {course_level}
        - Kategori: {course_category}
        - Durasi Pembelajaran: {course_duration}

        [INSTRUKSI UTAMA]
        1. Analisis Detail Materi, Konteks dari dokumen materi, serta Pertanyaan Pengguna yang diberikan di bawah ini.
        2. Anda sangat dianjurkan dan diperbolehkan menjawab pertanyaan seputar identitas materi (seperti judul, deskripsi, tingkat kesulitan/seberapa susah materi tersebut, durasi, atau roadmap belajar) berdasarkan [DETAIL MATERI SAAT INI] yang disediakan di atas.
        3. Jika pengguna menanyakan tingkat kesulitan materi atau penilaian "seberapa susah materi ini 0/10", gunakan skala kesulitan 1/10 sampai 10/10 secara ramah dan edukatif berdasarkan Tingkat Kesulitan/Level yang tercantum (contoh: Level 'Pemula' = 2/10 sampai 4/10, Level 'Menengah' = 5/10 sampai 7/10, Level 'Lanjutan' = 8/10 sampai 10/10). Berikan motivasi tambahan agar mereka termotivasi!
        4. Untuk pertanyaan akademis atau konseptual mengenai isi materi, carilah jawabannya di dalam [Konteks Dokumen Materi] di bawah. Jika ada, jelaskan kembali (paraphrase) menggunakan bahasa yang kasual, mudah dimengerti, sistematis, ramah, dan mengalir alami, serta tambahkan contoh/analogi jika membantu.
        5. JANGAN hanya menyalin mentah-mentah (copy-paste) teks dari database. Gunakan pemahaman Anda sebagai AI untuk memperkaya penjelasan tersebut.
        6. PENTING: Jika jawaban dari pertanyaan akademis/konseptual sama sekali tidak dibahas di [Konteks Dokumen Materi] dan tidak dapat disimpulkan dari [DETAIL MATERI SAAT INI], jawablah dengan kalimat: "Maaf, materi terkait pertanyaan tersebut belum tersedia di BrainPath saat ini."

        [Konteks Dokumen Materi]
        {context}

        Pertanyaan: {input}
        """
        self.prompt = ChatPromptTemplate.from_template(template)

    def _format_docs(self, docs):
        """Fungsi helper untuk menggabungkan teks dari dokumen yang ditemukan"""
        return "\n\n".join(doc.page_content for doc in docs)

    def get_answer(self, req: ChatRequest) -> ChatResponse:
        # Query course metadata from PostgreSQL
        from pkg.database.postgress import SessionLocal
        from internal.data.entity.course import CourseEntity

        course_title = "Tidak diketahui"
        course_description = "Tidak ada deskripsi"
        course_level = "Pemula"
        course_category = "Umum"
        course_duration = "—"

        db = SessionLocal()
        try:
            course = db.query(CourseEntity).filter(CourseEntity.id == req.sourcesID).first()
            if course:
                course_title = course.title or course_title
                course_description = course.description or course_description
                course_level = course.level or course_level
                course_category = course.category or course_category
                course_duration = course.duration_text or (f"{course.duration_minutes} menit" if course.duration_minutes else course_duration)
        except Exception as e:
            print(f"Error querying course metadata: {str(e)}")
        finally:
            db.close()

        # Buat retriever dinamis dengan filter metadata berdasarkan course_id (sourcesID)
        retriever = self.vector_db.as_retriever(
            search_kwargs={
                "k": 3,
                "filter": {"course_id": str(req.sourcesID)}
            }
        )

        # Jalankan context retriever secara manual
        source_docs = retriever.invoke(req.question)
        context_str = self._format_docs(source_docs)
        
        # Jalankan prompt + llm secara langsung dengan metadata terisi
        prompt_value = self.prompt.invoke({
            "context": context_str,
            "input": req.question,
            "course_title": course_title,
            "course_description": course_description,
            "course_level": course_level,
            "course_category": course_category,
            "course_duration": course_duration
        })
        
        try:
            llm_response = self.llm.invoke(prompt_value)
            answer = llm_response.content
        except Exception as e:
            error_str = str(e)
            print(f"Gemini API Error: {error_str}")
            if "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower() or "429" in error_str:
                answer = (
                    "**[Informasi Sistem: Limit Kuota AI Terlampaui]**\n\n"
                    "Maaf, limit kuota gratis API Key Gemini Anda di file `.env` telah habis (Limit: 20 request/hari pada Free Tier).\n\n"
                    "Untuk melanjutkan percakapan:\n"
                    "1. Buka file `d:\\Program\\xampp\\htdocs\\capstone-projek-ml\\.env`.\n"
                    "2. Ganti nilai `GOOGLE_API_KEY` dengan API Key Gemini baru yang aktif (gratis dari [Google AI Studio](https://aistudio.google.com/)).\n"
                    "3. Simpan file, dan server Python akan memuat ulang secara otomatis."
                )
            else:
                answer = f"Maaf, terjadi kesalahan saat menghubungi layanan AI: {error_str}"
        
        sources = list(set([
            str(doc.metadata.get("course_id", "Unknown")) 
            for doc in source_docs
        ]))
        
        # Bungkus data ke dalam format ChatResponse DTO
        return ChatResponse(
            status="success",
            data=ChatResponseData(
                question=req.question,
                answer=answer
            ),
            meta={
                "filtered_course_id": req.sourcesID,
                "sources_found": sources
            }
        )