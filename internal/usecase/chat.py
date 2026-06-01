# internal/usecase/chat.py
# Logika bisnis untuk Chatbot AI dengan Strict Title-Based Guardrail (Tanpa ChromaDB).

from typing import Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pkg.utils.config import settings
from internal.data.dto.chat import ChatResponse, ChatResponseData
from pkg.database.postgress import SessionLocal
from internal.data.entity.course import CourseEntity
from sqlalchemy import func

class ChatUsecase:
    def __init__(self):
        # Memuat LLM Gemini dengan API Key dari .env
        api_key = settings.GOOGLE_API_KEY
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0
        )
        print("--- ChatUsecase: Gemini AI chatbot inisialisasi sukses ---")

    def get_answer(self, question: str, course_id: Optional[int] = None, course_title: Optional[str] = None) -> ChatResponse:
        """
        Memproses pertanyaan akademik user dengan strict guardrail berdasarkan metadata course
        yang tersimpan di database PostgreSQL.
        """
        # 1. Query course metadata dari PostgreSQL
        db = SessionLocal()
        course = None
        try:
            if course_id is not None:
                course = db.query(CourseEntity).filter(CourseEntity.id == course_id).first()
            elif course_title:
                course = db.query(CourseEntity).filter(
                    func.lower(CourseEntity.title) == course_title.strip().lower()
                ).first()
        except Exception as e:
            print(f"Error querying course metadata: {str(e)}")
        finally:
            db.close()

        # 2. Jika course tidak ditemukan
        if not course:
            err_msg = "Maaf, materi/kursus yang Anda pelajari tidak ditemukan di sistem."
            return ChatResponse(
                status="error",
                data=ChatResponseData(
                    question=question,
                    answer=err_msg
                )
            )

        title = course.title or "Tidak diketahui"
        description = course.description or "Tidak ada deskripsi"
        summary = course.summary or "Tidak ada ringkasan"

        # 3. Susun system prompt yang sangat ketat sesuai spesifikasi claude.md
        system_prompt = (
            "Kamu adalah asisten akademik yang ketat. User saat ini sedang mempelajari materi: \"{title}\".\n"
            "Deskripsi Materi: {description}\n"
            "Ringkasan: {summary}\n\n"
            "Tugasmu:\n"
            "1. JAWAB HANYA pertanyaan yang berkaitan langsung dengan materi \"{title}\" di atas.\n"
            "2. Jika pertanyaan user melenceng, keluar dari topik, atau membahas materi/teknologi lain di luar konteks di atas, kamu WAJIB menolak menjawab dan katakan: \"Maaf, saya didesain hanya untuk membantu Anda memahami materi {title}. Mari fokus pada topik ini!\""
        ).format(title=title, description=description, summary=summary)

        # 4. Kirimkan prompt ke API Gemini
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]

        try:
            llm_response = self.llm.invoke(messages)
            answer = llm_response.content
        except Exception as e:
            error_str = str(e)
            print(f"Gemini API Error: {error_str}")
            if "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower() or "429" in error_str:
                answer = (
                    "**[Informasi Sistem: Limit Kuota AI Terlampaui]**\n\n"
                    "Maaf, limit kuota gratis API Key Gemini Anda di file `.env` telah habis (Limit: 20 request/hari pada Free Tier).\n\n"
                    "Untuk melanjutkan percakapan, silakan perbarui nilai `GOOGLE_API_KEY` di file `.env` dengan API Key Gemini baru yang aktif."
                )
            else:
                answer = f"Maaf, terjadi kesalahan saat menghubungi layanan AI: {error_str}"

        # 5. Return ChatResponse DTO yang bersih tanpa duplikasi 'answer' di root
        return ChatResponse(
            status="success",
            data=ChatResponseData(
                question=question,
                answer=answer
            )
        )