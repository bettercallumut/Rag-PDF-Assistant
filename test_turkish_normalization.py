#!/usr/bin/env python3
"""
Türkçe Normalizasyon Test Scripti
Android'deki tutarsızlık sorununu test eder
"""

# Basit test fonksiyonu
def turkish_lower(text):
    """Türkçe karakter normalizasyonu"""
    turkish_map = {
        'I': 'ı',  'İ': 'i',
        'Ç': 'ç', 'Ğ': 'ğ',
        'Ö': 'ö', 'Ş': 'ş', 'Ü': 'ü'
    }
    return ''.join(turkish_map.get(c, c.lower()) for c in text)

# Test senaryoları
test_cases = [
    # (PDF'teki metin, Kullanıcı sorgusu, Eşleşmeli mi?)
    ("IŞIK AYARLARI", "ışık ayarları", True),
    ("GÖRÜNTÜ AYARLARI", "görüntü ayarları", True),
    ("İŞLEM MENUSU", "işlem menüsü", True),
    ("ZOOM FONKSİYONU", "zoom fonksiyonu", True),
    ("SES SETİ", "ses seti", True),
]

print("=" * 60)
print("TÜRKÇE NORMALİZASYON TESTİ")
print("=" * 60)

print("\n1️⃣  Python Standart .lower() Testi (YANLIŞ)")
print("-" * 60)
for pdf_text, user_query, should_match in test_cases:
    pdf_lower = pdf_text.lower()
    user_lower = user_query.lower()
    match = pdf_lower == user_lower
    status = "✅" if match == should_match else "❌"
    print(f"{status} PDF: '{pdf_text}' -> '{pdf_lower}'")
    print(f"   Query: '{user_query}' -> '{user_lower}'")
    print(f"   Eşleşme: {match} (Beklenen: {should_match})")
    print()

print("\n2️⃣  Türkçe turkish_lower() Testi (DOĞRU)")
print("-" * 60)
for pdf_text, user_query, should_match in test_cases:
    pdf_normalized = turkish_lower(pdf_text)
    user_normalized = turkish_lower(user_query)
    match = pdf_normalized == user_normalized
    status = "✅" if match == should_match else "❌"
    print(f"{status} PDF: '{pdf_text}' -> '{pdf_normalized}'")
    print(f"   Query: '{user_query}' -> '{user_normalized}'")
    print(f"   Eşleşme: {match} (Beklenen: {should_match})")
    print()

# Keyword matching testi
print("\n3️⃣  Keyword Matching Testi")
print("-" * 60)

pdf_content = "GÖRÜNTÜ AYARLARI MENUSU: IŞIK, PARLAKLK, KONTRAST"
user_query = "görüntü ayarları nasıl yapılır?"

print(f"PDF İçeriği (Normalized): {turkish_lower(pdf_content)}")
print(f"Kullanıcı Sorgusu (Normalized): {turkish_lower(user_query)}")

keywords = [w for w in turkish_lower(user_query).split() if len(w) > 2]
print(f"Çıkarılan Kelimeler: {keywords}")

pdf_normalized = turkish_lower(pdf_content)
found_keywords = [kw for kw in keywords if kw in pdf_normalized]
print(f"Bulunan Kelimeler: {found_keywords}")

score = sum(pdf_normalized.count(kw) for kw in keywords)
print(f"Skor: {score}")

if score > 0:
    print("✅ BAŞARILI: Keywords bulundu, cevap verilebilir!")
else:
    print("❌ BAŞARISIZ: Keywords bulunamadı")

print("\n" + "=" * 60)
print("TEST TAMAMLANDI")
print("=" * 60)
