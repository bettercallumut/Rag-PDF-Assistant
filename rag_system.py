from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
import PyPDF2

class RAGSystem:
    def __init__(self):
        self.full_text = ""
        self.page_texts = []
        self.total_tokens = 0
        
    def count_tokens(self, text):
        return int(len(text) * 0.25)
    
    def process_pdf(self, pdf_path, progress_callback=None):
        self.full_text = ""
        self.page_texts = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                for i, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    
                    if page_text and page_text.strip():
                        estimated_tokens = int(len(page_text) * 0.25)
                        
                        self.page_texts.append({
                            'page_num': i + 1,
                            'text': page_text,
                            'tokens': estimated_tokens
                        })
                        self.full_text += f"\n\n--- SAYFA {i + 1} ---\n\n{page_text}"
                    
                    if progress_callback and (i % 5 == 0 or i == total_pages - 1):
                        progress_callback(int((i + 1) / total_pages * 100))
                        
        except Exception as e:
            raise Exception(f"PDF Hatası: {str(e)}")
        
        self.total_tokens = int(len(self.full_text) * 0.25)
        return len(self.page_texts)
    
    def _extract_keywords(self, question):
        words = question.lower().split()
        stopwords = {'bir', 've', 'için', 'ile', 'mi', 'mı', 'mu', 'mü', 'ne', 'nasıl', 'nedir'}
        return [w for w in words if len(w) > 2 and w not in stopwords]
    
    def _score_page(self, page_text, keywords):
        text_lower = page_text.lower()
        score = sum(text_lower.count(kw) for kw in keywords)
        return score
    
    def get_context_for_query(self, question, max_tokens=25000):
        available_tokens = max_tokens - 5000
        
        if self.total_tokens <= available_tokens:
            return self.full_text
        
        keywords = self._extract_keywords(question)
        
        scored_pages = []
        for page_data in self.page_texts:
            score = self._score_page(page_data['text'], keywords)
            scored_pages.append({
                'score': score,
                'page_num': page_data['page_num'],
                'text': page_data['text'],
                'tokens': page_data['tokens']
            })
        
        scored_pages.sort(key=lambda x: x['score'], reverse=True)
        
        selected_text = ""
        used_tokens = 0
        
        for page in scored_pages:
            if used_tokens + page['tokens'] > available_tokens:
                break
            selected_text += f"\n\n--- SAYFA {page['page_num']} ---\n\n{page['text']}"
            used_tokens += page['tokens']
        
        return selected_text if selected_text else self.full_text[:available_tokens * 4]
    
    def query(self, question, api_key):
        if not self.full_text:
            return "Lütfen önce bir PDF dosyası yükleyin."
        
        context_text = self.get_context_for_query(question)
        
        if not context_text.strip():
            return "###ASK_FALLBACK###"

        try:
            chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4o", temperature=0.2)
            
            system_prompt = f"""Sen bir teknik destek asistanısın ve kullanıcıya yüklenen PDF kullanım kılavuzunu açıklıyorsun.

BAĞLAM (Kullanım Kılavuzundan):
{context_text}

ÖNEMLİ KURALLAR:
1. SADECE yukarıdaki kullanım kılavuzundaki bilgileri kullan
2. Genel tavsiyeler verme (örn: "kullanım kılavuzuna başvurun" YASAK - zaten kullanım kılavuzunu okuyorsun!)
3. Eğer bilgi bağlamda YOKSA: "Bu bilgi kullanım kılavuzunda yer almıyor" de ve cevabı DURDUR
4. Adım adım NET talimatlar ver
5. Tuş/düğme isimlerini TAM olarak belirt (Örn: "OK tuşu", "Menü tuşu")
6. Eksiksiz ve detaylı cevap ver
7. Varsayımda bulunma, sadece bağlamdaki bilgiyi kullan

CEVAP TARZI:
- Direkt, net ve kılavuzdaki bilgiye dayalı
- Gereksiz giriş cümleleri kullanma
- "Daha fazla bilgi için..." cümleleri KULLANMA
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
            chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo", temperature=0.5)
            system_prompt = "Sen yardımcı bir asistansın. Kullanıcıya genel konularda yardımcı ol."
            
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