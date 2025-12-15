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
            self.embeddings = HuggingFaceEmbeddings(
                model_name="emrecan/bert-base-turkish-cased-mean-nli-stsb-tr",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        except Exception:
            try:
                self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
            except Exception:
                pass

    def process_pdf(self, pdf_path, progress_callback=None):
        import pdfplumber
        text = ""
        self.first_page_text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                if total_pages > 0:
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
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200,
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
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 30})
        return len(splits)

    def generate_search_queries(self, question, api_key):
        try:
            chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4", temperature=0.3)
            system_prompt = """Sen uzman bir araştırmacısın.
Kullanıcının sorusunu analiz et ve bu sorunun cevabını teknik bir kullanım kılavuzunda bulabilmek için 3 farklı alternatif arama ifadesi üret.
Özellikler, ayarlar ve teknik terimler arasındaki anlamsal ilişkileri kur.
Örnek: "Zoom fonksiyonu" -> "Zoom ayarı", "Yakınlaştırma", "Zoom modu"

Sadece alternatif ifadeleri listele, her satıra bir tane. Başka açıklama yapma."""
            
            response = chat.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=question)
            ]).content
            
            queries = [q.strip() for q in response.split('\n') if q.strip()]
            queries.append(question)
            return list(set(queries))
        except Exception:
            return [question]

    def query(self, question, api_key):
        if not self.retriever:
            return "PDF yükleyin."
        
        queries = self.generate_search_queries(question, api_key)

        all_docs = []
        seen_content = set()
        
        for q in queries:
            try:
                docs = self.retriever.invoke(q)
                for doc in docs:
                    content_hash = doc.page_content.strip()
                    if content_hash not in seen_content:
                        seen_content.add(content_hash)
                        all_docs.append(doc)
            except Exception:
                pass
        
        question_keywords = set(question.lower().split())
        scored_docs = []
        for doc in all_docs:
            content_lower = doc.page_content.lower()
            score = sum(1 for kw in question_keywords if kw in content_lower)
            scored_docs.append((score, doc))
        
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        relevant_docs = [doc for score, doc in scored_docs[:30]]
        
        context_text = "\n\n---\n\n".join([d.page_content for d in relevant_docs])
        
        should_fallback = False
        if not context_text.strip():
            should_fallback = True

        try:
            chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4", temperature=0.2)
            
            if not should_fallback:
                system_prompt = f"""Sen uzman bir teknik destek asistanısın. Kullanıcıya cihazının kullanım kılavuzundan detaylı bilgi veriyorsun.

BAĞLAM (PDF'den alınan bilgiler):
{context_text}

GÖREV:
1. Kullanıcının sorusunu yukarıdaki bağlamı kullanarak DETAYLI cevapla.
2. MUTLAKA şunları ekle:
   - Spesifik TUŞ ADLARI ("Yukarı ok tuşu", "Mode tuşu", "Set tuşu" vb.)
   - ADIM ADIM TALİMATLAR (1. adım, 2. adım...)
   - MENÜ YOLLARI (varsa)
   - SEMBOL/İKON AÇIKLAMALARI (varsa)
3. Genel bilgi verme, BAĞLAMDAKİ tam bilgiyi ver.
4. "kumanda" yerine "kumandanın hangi tuşu" de.
5. Sayısal değerler varsa (derece, saat vb.) belirt.
6. Sadece bağlamda HIÇ ilgili bilgi yoksa ###FALLBACK_NEEDED### yaz.

KRİTİK KURAL - BOŞ SEMBOL BIRAKMA:
- Bağlamda özel semboller (↑↓▲▼►◄ veya boş) varsa veya metinde sadece resim konulmuşsa, cümlenin gelişinden hangi tuşu olduğunu ANLA ve türkçe adını YAZ.
- Kesinlikle " " veya "" şeklinde boş tırnak kullanma.
- Örnek: "Kumandadaki [Aşağı Ok] tuşuna basın" veya "Kumandadaki 'Mode' tuşuna basın".
- Tuş ismini bulamıyorsan "ilgili fonksiyon tuşuna" de ama asla boş bırakma.
"""
                
                response = chat.invoke([SystemMessage(content=system_prompt), HumanMessage(content=question)]).content
                
                if '" "' in response or '""' in response:
                    lines = response.split('\n')
                    fixed_lines = []
                    for line in lines:
                        if '" "' in line or '""' in line:
                             lower_line = line.lower()
                             replacement = '"İLGİLİ TUŞ"'
                             
                             if "çalıştırın" in lower_line or "açmak" in lower_line or "kapatmak" in lower_line:
                                 replacement = '"GÜÇ (Açma/Kapama)"'
                             elif "mod" in lower_line or "ısıtma" in lower_line or "soğutma" in lower_line:
                                 replacement = '"MOD (Mode)"'
                             elif "sıcaklık" in lower_line or "derece" in lower_line or "artacak" in lower_line:
                                 replacement = '"YUKARI/AŞAĞI OK"'
                             elif "fan" in lower_line or "hız" in lower_line:
                                 replacement = '"FAN"'
                             elif "kanat" in lower_line or "yön" in lower_line:
                                 replacement = '"KANAT (Swing)"'
                                 
                             line = line.replace('" "', replacement).replace('""', replacement)
                        fixed_lines.append(line)
                    response = '\n'.join(fixed_lines)

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
            chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo", temperature=0.3)
            system_prompt = f"""Sen bir teknik destek asistanısın.

DÖKÜMAN BİLGİSİ (cihaz hakkında):
{self.first_page_text}

KURALLAR:
1. Kullanıcının sorusu bu cihazla ilgili.
2. Cihazın PDF'inden alınan bilgilere göre cevapla.
3. Eğer kesin bilgi yoksa, elindeki cihaz (PDF) ipuçlarını kullanarak yardımcı olmaya çalış.
4. "Bu bilgi yok" demek yerine, "PDF'te tam olarak bu yok ama şunlar var..." diyerek yönlendir."""
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
            system_prompt = """Sen bir metin özetleme uzmanısın.
Görevin: Verilen teknik metni, bir kullanıcının sesli olarak dinleyeceği şekilde, en kritik bilgileri içeren 1-2 cümlelik çok kısa bir özete dönüştürmek.
- Detayları (adım numaraları, ince ayarlar) atla, sadece ana fikri ve ne yapılması gerektiğini söyle.
- "Kullanım kılavuzuna göre..." gibi girişler yapma, direkt konuya gir.
- Örneğin: "Isı ayarını değiştirmek için Mode tuşuyla ısıtma modunu seçip aşağı yukarı ok tuşlarıyla dereceyi ayarlayabilirsiniz."
"""
            response = chat.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Özetlenecek Metin:\n{text}")
            ]).content
            return response
        except Exception:
            return text[:200] + "..."

    def query_stream(self, question, api_key, callback_handler):
        if not self.retriever:
            yield "Lütfen önce bir PDF dosyası yükleyin."
            return

        queries = self.generate_search_queries(question, api_key)
        
        all_docs = []
        seen_content = set()
        for q in queries:
            try:
                docs = self.retriever.invoke(q)
                for doc in docs:
                    content_hash = doc.page_content.strip()
                    if content_hash not in seen_content:
                        seen_content.add(content_hash)
                        all_docs.append(doc)
            except Exception:
                pass
        
        relevant_docs = all_docs[:25]
        
        context_text = "\n\n---\n\n".join([d.page_content for d in relevant_docs])
        
        if not context_text.strip():
            yield "PDF içinde bu konuyla ilgili bilgi bulamadım."
            return

        try:
            chat = ChatOpenAI(
                openai_api_key=api_key, 
                model_name="gpt-3.5-turbo", 
                temperature=0.3,
                streaming=True,
                callbacks=[callback_handler]
            )
            
            system_prompt = f"""Sen yardımsever ve zeki bir Türkçe asistansın.
            
            BAĞLAM (PDF'den alınan bilgiler):
            {context_text}
            
            GÖREV: 
            - Kullanıcının sorusunu cevaplamak için yukarıdaki bağlamı analiz et.
            - Tam ve kesin bir cevap bulamazsan, bağlamdaki **ilgili olabilecek** tüm bilgileri (örn. menü yolları, benzer ayarlar, bağlantı şemaları) birleştirerek yardımcı ol.
            - "Bilgi yok" demek yerine, "PDF'te tam olarak bu anlatılmıyor ancak şunlar var..." şeklinde elindeki ipuçlarını sun.
            - Asla genel internet bilgisini "PDF'te yazıyor" gibi sunma, ama genel bilginle PDF'teki ipuçlarını yorumlayabilirsin.
            - Cevabını net, yapıcı ve konuşma dilinde ver."""

            chat.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=question)
            ])
            
        except Exception as e:
            yield f"Hata oluştu: {e}"
