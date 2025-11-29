from openai import OpenAI
import config

SYMBOL_MAP = {
    "»": "",
    "«": "",
    "→": " sağ ok tuşu ",
    "←": " sol ok tuşu ",
    "↑": " yukarı ok tuşu ",
    "↓": " aşağı ok tuşu ",
    "▲": " yukarı ok tuşu ",
    "▼": " aşağı ok tuşu ",
    "◄": " sol ok tuşu ",
    "►": " sağ ok tuşu ",
    "Λ": " yukarı ok tuşu ",
    "V": None,
    "∧": " yukarı ok tuşu ",
    "∨": " aşağı ok tuşu ",
    "•": ", ",
    "●": ", ",
    "○": ", ",
    "■": ", ",
    "□": ", ",
    "★": " yıldız ",
    "☆": " yıldız ",
    "✓": " tik işareti ",
    "✗": " çarpı işareti ",
    "✕": " çarpı işareti ",
    "×": " çarpı ",
    "÷": " bölü ",
    "±": " artı eksi ",
    "≤": " küçük eşit ",
    "≥": " büyük eşit ",
    "≠": " eşit değil ",
    "∞": " sonsuz ",
    "°": " derece ",
    "€": " euro ",
    "£": " sterlin ",
    "¥": " yen ",
    "©": " telif hakkı ",
    "®": " tescilli marka ",
    "™": " ticari marka ",
    "§": " paragraf ",
    "¶": " paragraf ",
    "†": ", ",
    "‡": ", ",
    "…": "...",
    "–": " - ",
    "—": " - ",
    "'": "'",
    "'": "'",
    """: '"',
    """: '"',
    "„": '"',
}

BUTTON_PATTERNS = [
    (r'\bV\b', ' aşağı ok tuşu '),
    (r'\bP\+\b', ' P artı tuşu '),
    (r'\bP\-\b', ' P eksi tuşu '),
    (r'\bP\–\b', ' P eksi tuşu '),
    (r'\bCH\+\b', ' kanal artı tuşu '),
    (r'\bCH\-\b', ' kanal eksi tuşu '),
    (r'\bVOL\+\b', ' ses artı tuşu '),
    (r'\bVOL\-\b', ' ses eksi tuşu '),
    (r'\bOK\b', ' OK tuşu '),
    (r'\bMENU\b', ' menü tuşu '),
    (r'\bEXIT\b', ' çıkış tuşu '),
    (r'\beXIT\b', ' çıkış tuşu '),
    (r'\bHOME\b', ' ana sayfa tuşu '),
    (r'\bBACK\b', ' geri tuşu '),
    (r'\bENTER\b', ' giriş tuşu '),
    (r'\bPOWER\b', ' güç tuşu '),
    (r'\bSOURCE\b', ' kaynak tuşu '),
    (r'\bINPUT\b', ' giriş tuşu '),
    (r'\bMUTE\b', ' sessiz tuşu '),
    (r'\bPLAY\b', ' oynat tuşu '),
    (r'\bPAUSE\b', ' duraklat tuşu '),
    (r'\bSTOP\b', ' durdur tuşu '),
    (r'\bREC\b', ' kayıt tuşu '),
    (r'\bREW\b', ' geri sar tuşu '),
    (r'\bFF\b', ' ileri sar tuşu '),
    (r'\bTOOl\b', ' tool '),
    (r'\bTOOL\b', ' tool '),
    (r'\bTOOLS\b', ' tools '),
    (r'\bHDMI\b', ' HDMI '),
    (r'\bUSB\b', ' USB '),
    (r'\bAUX\b', ' AUX '),
]

def basic_text_cleanup(text):
    import re
    result = text
    for symbol, replacement in SYMBOL_MAP.items():
        if replacement is not None:
            result = result.replace(symbol, replacement)
    for pattern, replacement in BUTTON_PATTERNS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    result = re.sub(r'\s+', ' ', result)
    result = result.strip()
    return result

def process_text_for_tts(text):
    try:
        client = OpenAI(api_key=config.API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """Metni sesli okuma için düzenle. Kurallar:
1. Özel karakterleri (», «, →, ←, ↑, ↓, Λ, V vb.) Türkçe karşılıklarıyla değiştir
2. "V" harfi ok bağlamında kullanılıyorsa "aşağı ok tuşu" yap
3. "Λ" veya yukarı ok sembolleri "yukarı ok tuşu" yap
4. Kısaltmaları aç (HDMI, USB vb. olduğu gibi kalsın)
5. Tuş isimlerini anlaşılır yap (P+, P-, CH+ vb.)
6. Sadece düzenlenmiş metni döndür, açıklama ekleme"""
                },
                {"role": "user", "content": text}
            ],
            temperature=0.1,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except:
        return basic_text_cleanup(text)
