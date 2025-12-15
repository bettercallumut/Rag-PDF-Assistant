# text_processor.py
import re
import config

# Haritalamalar aynen kalabilir
SYMBOL_MAP = {
    "»": "", "«": "", "→": " sağ ok ", "←": " sol ok ", 
    "↑": " yukarı ok ", "↓": " aşağı ok ", "▲": " yukarı ok ", "▼": " aşağı ok ",
    "•": ", ", "●": ", ", "○": ", ", "★": " yıldız ", "☆": " yıldız ",
    "✓": " onay ", "✗": " iptal ", "×": " çarpı ", "÷": " bölü ",
    "±": " artı eksi ", "°": " derece ", "€": " euro ", "$": " dolar ",
    "&": " ve ", "%": " yüzde ", "@": " et ",
}

def basic_text_cleanup(text):
    result = text
    # Sembolleri değiştir
    for symbol, replacement in SYMBOL_MAP.items():
        if replacement is not None:
            result = result.replace(symbol, replacement)
            
    # Gereksiz boşlukları temizle
    result = re.sub(r'\s+', ' ', result)
    result = result.strip()
    return result

def process_text_for_tts(text):
    # DÜZELTME: Her cümle için OpenAI çağırmak çok pahalı ve yavaştı.
    # Bunu iptal ettik. Sadece basic cleanup yeterli.
    return basic_text_cleanup(text)