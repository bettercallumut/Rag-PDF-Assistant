from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import PyPDF2

class RAGSystem:
    def __init__(self):
        self.vectorstore = None
        self.retriever = None
        self.embeddings = None
        self.first_page_text = ""
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        except Exception as e:
            print(f"Embedding Error: {e}")

    def process_pdf(self, pdf_path, progress_callback=None):
        text = ""
        self.first_page_text = ""
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                total_pages = len(reader.pages)
                if total_pages > 0:
                    first_page = reader.pages[0]
                    if first_page.extract_text():
                        self.first_page_text = first_page.extract_text()[:2000]

                for i, page in enumerate(reader.pages):
                    if page.extract_text():
                        text += page.extract_text() + "\n"
                    if progress_callback:
                        progress_callback(int((i + 1) / total_pages * 100))
        except Exception as e:
            raise Exception(f"PDF Error: {e}")

        doc = Document(page_content=text, metadata={"source": pdf_path})
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
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
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 12})
        return len(splits)

    def query(self, question, api_key):
        if not self.retriever:
            return "PDF yükleyin."
        
        relevant_docs = self.retriever.invoke(question)
        context_text = "\n\n---\n\n".join([d.page_content for d in relevant_docs])
        
        should_fallback = False
        if not context_text.strip():
            should_fallback = True

        try:
            chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4o-mini", temperature=0.3)
            
            if not should_fallback:
                system_prompt = f"""Sen yardımsever bir Türkçe asistansın.

BAĞLAM (PDF'den alınan bilgiler):
{context_text}

GÖREV: 
- Kullanıcının sorusunu yukarıdaki bağlamı kullanarak cevapla.
- Türkçe'de "ayar/ayarı/ayarlar/ayarları" gibi ekler aynı anlama gelir, esnek ol.
- Bağlamda soruyla ilgili herhangi bir bilgi varsa (kısmi eşleşme dahil) cevap ver.
- Sadece bağlamda hiç ilgili bilgi yoksa ###FALLBACK_NEEDED### yaz.
- Kısmi bilgi varsa bile cevap vermeye çalış."""
                
                response = chat.invoke([SystemMessage(content=system_prompt), HumanMessage(content=question)]).content
                if "###FALLBACK_NEEDED###" in response:
                    should_fallback = True
                else:
                    return response

            if should_fallback:
                return "###ASK_FALLBACK###"
        except Exception as e:
            return f"Hata: {str(e)}"

    def query_general(self, question, api_key):
        try:
            chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4o-mini", temperature=0.3)
            system_prompt = f"""Sen bir teknik destek asistanısın.

DÖKÜMAN BİLGİSİ (cihaz hakkında):
{self.first_page_text}

KURALLAR:
1. Kullanıcının sorusu bu cihazla ilgili.
2. Eğer soru cihazda OLMAYAN bir özellik hakkındaysa (örn: cihazda DisplayPort yoksa DisplayPort sorusu), 
   "Bu cihazda [özellik adı] bulunmamaktadır." şeklinde cevap ver.
3. Halüsinasyon yapma - cihazda olmayan özellikleri varmış gibi anlatma.
4. Sadece genel bilgi verebiliyorsan, cevabın başına [GENEL BİLGİ] ekle.
5. Cihazın özelliklerini bilmiyorsan, genel bilgi olduğunu belirt."""
            
            response = chat.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=question)
            ]).content
            return response
        except Exception as e:
            return f"Hata: {e}"
