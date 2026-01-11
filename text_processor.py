import re
import config

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
    for symbol, replacement in SYMBOL_MAP.items():
        if replacement is not None:
            result = result.replace(symbol, replacement)
    result = re.sub(r'\s+', ' ', result)
    result = result.strip()
    return result

def process_text_for_tts(text):
    return basic_text_cleanup(text)
