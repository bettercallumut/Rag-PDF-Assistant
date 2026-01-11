import openai
import PyPDF2

class RAGSystem:
    def __init__(self):
        self.full_text = ""
        self.page_texts = []
        self.total_tokens = 0
    
    @staticmethod
    def turkish_lower(text):
        turkish_map = {
            'I': 'ı',
            'İ': 'i',
            'Ç': 'ç',
            'Ğ': 'ğ',
            'Ö': 'ö',
            'Ş': 'ş',
            'Ü': 'ü'
        }
        
        result = []
        for char in text:
            if char in turkish_map:
                result.append(turkish_map[char])
            else:
                result.append(char.lower())
        
        return ''.join(result)
        
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
                        page_text_normalized = self.turkish_lower(page_text)
                        estimated_tokens = int(len(page_text_normalized) * 0.25)
                        
                        self.page_texts.append({
                            'page_num': i + 1,
                            'text': page_text_normalized,
                            'tokens': estimated_tokens
                        })
                        self.full_text += f"\n\n--- SAYFA {i + 1} ---\n\n{page_text_normalized}"
                    
                    if progress_callback and (i % 5 == 0 or i == total_pages - 1):
                        progress_callback(int((i + 1) / total_pages * 100))
                        
        except Exception as e:
            raise Exception(f"PDF Hatası: {str(e)}")
        
        self.total_tokens = int(len(self.full_text) * 0.25)
        return len(self.page_texts)
    
    def _extract_keywords(self, question):
        words = self.turkish_lower(question).split()
        stopwords = {'bir', 've', 'için', 'ile', 'mi', 'mı', 'mu', 'mü', 'ne', 'nasıl', 'nedir', 'nasil'}
        return [w for w in words if len(w) > 2 and w not in stopwords]
    
    def _score_page(self, page_text, keywords):
        text_lower = self.turkish_lower(page_text) if page_text == page_text.upper() else page_text
        score = sum(text_lower.count(kw) for kw in keywords)
        return score
    
    def get_context_for_query(self, question, max_tokens=15000):
        available_tokens = max_tokens - 3000
        
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
            openai.api_key = api_key
            
            system_prompt = f"""PDF kullanım kılavuzundaki bilgilere göre cevap ver.

BAĞLAM:
{context_text}

KURALLAR:
1. Sadece yukarıdaki bilgiyi kullan
2. Kısa ve net açıkla
3. Bilgi yoksa "Bu bilgi kılavuzda yok" de
4. Adım adım anlat
5. Tuş/düğme isimlerini belirt
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.2,
                max_tokens=800
            )
            
            return response.choices[0].message.content

        except openai.error.RateLimitError as e:
            import time
            error_str = str(e)
            
            if "retry after" in error_str.lower():
                print("[RPM] Rate limit - 5 saniye beklenip tekrar denenecek...")
                time.sleep(5)
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": question}
                        ],
                        temperature=0.2,
                        max_tokens=800
                    )
                    return response.choices[0].message.content
                except Exception:
                    pass
            
            return "[HATA] API limiti aşıldı. 10 saniye bekleyip tekrar deneyin."
        
        except openai.error.InvalidRequestError as e:
            return "[HATA] PDF çok büyük. Daha kısa PDF veya daha spesifik soru kullanın."
        
        except openai.error.AuthenticationError as e:
            return "[HATA] API key geçersiz. config.py dosyasını kontrol edin."
        
        except Exception as e:
            error_msg = str(e)
            if "rate limit" in error_msg.lower():
                return "[HATA] API limiti aşıldı. Lütfen 10 saniye bekleyin."
            elif "quota" in error_msg.lower():
                return "[HATA] OpenAI kredisi bitti. Hesabınızı kontrol edin."
            else:
                return f"[HATA] {error_msg[:150]}"

    def query_general(self, question, api_key):
        try:
            openai.api_key = api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen yardımcı bir asistansın. Kullanıcıya genel konularda yardımcı ol."},
                    {"role": "user", "content": question}
                ],
                temperature=0.5
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Hata: {e}"

    def generate_summary(self, text, api_key):
        try:
            openai.api_key = api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Bu metni sesli okunmak üzere 1-2 cümleyle özetle. Gereksiz detayları at, direkt sonucu söyle."},
                    {"role": "user", "content": text}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception:
            return text[:300] + "..."
