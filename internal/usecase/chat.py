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
        db_path = "pkg/ml-models/chroma_db"
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

        [INSTRUKSI UTAMA]
        1. Analisis Konteks Materi dan Pertanyaan Pengguna yang diberikan di bawah ini.
        2. Jika jawaban dari pertanyaan tersebut tersedia di dalam Konteks Materi, jelaskan kembali (paraphrase) menggunakan bahasa yang kasual, mudah dimengerti, sistematis, dan mengalir secara alami.
        3. JANGAN hanya menyalin mentah-mentah (copy-paste) teks dari database. Gunakan pemahaman Anda sebagai AI untuk memperkaya penjelasan tersebut (misalnya menambahkan analogi sederhana, contoh sehari-hari, atau menstrukturkannya menjadi poin-poin/tabel jika diperlukan) agar lebih mudah dipahami mahasiswa.
        4. PENTING: Penjelasan tambahan Anda harus TETAP selaras dan berbasis pada fakta yang ada di Konteks Materi. Jangan mengada-ada informasi baru di luar materi yang disediakan.

        [BATASAN / CONSTRAINTS]
        - Jika jawaban dari pertanyaan sama sekali tidak dibahas atau tidak dapat disimpulkan dari Konteks Materi yang diberikan, jawablah dengan kalimat: "Maaf, materi terkait pertanyaan tersebut belum tersedia di BrainPath saat ini." Jangan mencoba mengarang jawaban dari pengetahuan umum Anda jika materi dasarnya tidak ada di konteks.

        Konteks: {context}

        Pertanyaan: {input}
        """
        self.prompt = ChatPromptTemplate.from_template(template)

    def _format_docs(self, docs):
        """Fungsi helper untuk menggabungkan teks dari dokumen yang ditemukan"""
        return "\n\n".join(doc.page_content for doc in docs)

    def get_answer(self, req: ChatRequest) -> ChatResponse:
        # Buat retriever dinamis dengan filter metadata berdasarkan course_id (sourcesID)
        # Pastikan tipe data filter (string/int) sama dengan tipe data saat Anda menyimpan metadata
        retriever = self.vector_db.as_retriever(
            search_kwargs={
                "k": 3,
                "filter": {"course_id": str(req.sourcesID)} # Chroma mengidentifikasi metadata berupa string di sync sebelumnya
            }
        )

        #Bangun LCEL Chain secara dinamis per request agar filter retriever bekerja secara spesifik
        qa_chain = (
            {
                "context": (lambda x: x["question"]) | retriever | self._format_docs, 
                "input": lambda x: x["question"]
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        #Eksekusi Chain menggunakan payload dict
        payload = {"question": req.question}
        answer = qa_chain.invoke(payload)
        
        #Ambil source docs yang terfilter untuk verifikasi/metadata jika dibutuhkan
        source_docs = retriever.invoke(req.question)
        sources = list(set([
            str(doc.metadata.get("course_id", "Unknown")) 
            for doc in source_docs
        ]))
        
        #Bungkus data ke dalam format ChatResponse DTO
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