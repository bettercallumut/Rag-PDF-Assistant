# rag_system.py
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import PyPDF2
import pdfplumber

class RAGSystem:
    def __init__(self):
        self.vectorstore = None
        self.retriever = None
        self.embeddings = None
        self.first_page_text = ""
        try:
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=config.API_KEY,
                model="text-embedding-3-small"
            )
        except Exception:
            pass

    def process_pdf(self, pdf_path, progress_callback=None):
        text = ""
        self.first_page_text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                if total_pages > 0:
                    # İlk sayfa özeti için metin al
                    self.first_page_text = pdf.pages[0].extract_text()[:2000] if pdf.pages[0].extract_text() else ""

                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text(layout=True)
                    if page_text:
                        text += page_text + "\n"
                    
                    if progress_callback:
                        progress_callback(int((i + 1) / total_pages * 100))
        except Exception as e:
            raise Exception(f"PDF Error: {e}")

        doc = Document(page_content=text, metadata={"source": pdf_path})
        
        # Chunk size biraz daha optimize edildi
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""]
        )
        splits = text_splitter.split_documents([doc])
        
        if self.vectorstore:
            try:
                self.vectorstore.delete_collection()
            except:
                pass
            
        self.vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=self.embeddings,
            collection_name="pdf_rag_qt"
        )
        
        # ÖNEMLİ DÜZELTME: k=30 çok fazlaydı, 6'ya düşürüldü.
        # Bu hem hızı artırır hem maliyeti düşürür hem de "Lost in the middle" sorununu çözer.
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 6})
        return len(splits)

    def generate_search_queries(self, question, api_key):
        # Maliyet tasarrufu için sorgu varyasyonlarını kapattık.
        # Çoğu teknik PDF sorusunda direkt soru daha iyi sonuç verir.
        # Eğer çok karmaşık sorular sorulacaksa burası açılabilir ama şu an için k=6 ile tek sorgu yeterli.
        return [question]

    def query(self, question, api_key):
        if not self.retriever:
            return "Lütfen önce bir PDF dosyası yükleyin."
        
        # Retrieval (Doküman Getirme)
        try:
            docs = self.retriever.invoke(question)
        except Exception:
            return "Doküman taranırken hata oluştu."
        
        context_text = "\n\n---\n\n".join([d.page_content for d in docs])
        
        if not context_text.strip():
            return "###ASK_FALLBACK###"

        try:
            # Model gpt-4o veya gpt-3.5-turbo seçilebilir. Maliyet için 3.5, zeka için 4.
            chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4o", temperature=0.2)
            
            system_prompt = f"""Sen uzman bir teknik destek asistanısın.

BAĞLAM (PDF Bilgisi):
{context_text}

GÖREV:
Soruyu SADECE yukarıdaki bağlama göre cevapla. 
- Adım adım talimat ver.
- Tuş isimlerini tam olarak belirt (Örn: "OK tuşu", "Menü tuşu").
- Bilgi bağlamda yoksa uydurma, "Bilgi PDF'te bulunamadı" de.
"""
            response = chat.invoke([
                SystemMessage(content=system_prompt), 
                HumanMessage(content=question)
            ]).content
            
            return response

        except Exception as e:
            return f"API Hatası: {str(e)}"

    def query_general(self, question, api_key):
        try:
            # Genel sohbet için daha ucuz model
            chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo", temperature=0.5)
            system_prompt = f"""Sen yardımcı bir asistansın.
Şu an yüklü olan belge hakkında ipucu: {self.first_page_text[:500]}...
Kullanıcıya genel konularda yardımcı ol."""
            
            response = chat.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=question)
            ]).content
            return response
        except Exception as e:
            return f"Hata: {e}"

    def generate_summary(self, text, api_key):
        try:
            chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4o-mini", temperature=0.3)
            system_prompt = "Bu metni sesli okunmak üzere 1-2 cümleyle özetle. Gereksiz detayları at, direkt sonucu söyle."
            response = chat.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=text)
            ]).content
            return response
        except Exception:
            return text[:300] + "..."