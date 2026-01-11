#!/usr/bin/env python3
"""
Android Pydroid3 Otomatik Kurulum Scripti
PDF Asistanı için gerekli tüm paketleri kurar
"""

import sys
import subprocess

def install_package(package_name):
    """Paketi kur"""
    try:
        print(f"[>>] {package_name} kuruluyor...")
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 
            package_name, '--upgrade'
        ])
        print(f"[OK] {package_name} kuruldu!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[HATA] {package_name} kurulamadi: {e}\n")
        return False

def main():
    print("=" * 60)
    print("PDF ASISTANI - ANDROID KURULUM")
    print("=" * 60)
    print("\nGerekli paketler kuruluyor...\n")
    
    # Gerekli paketler (Rust gerektirmeyenler)
    packages = [
        'kivy',
        'openai==0.28.1',
        'PyPDF2',
        'python-dotenv'
    ]
    
    success = 0
    failed = 0
    
    for package in packages:
        if install_package(package):
            success += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"KURULUM TAMAMLANDI: {success} basarili, {failed} basarisiz")
    print("=" * 60)
    
    if failed == 0:
        print("\n[OK] Tum paketler basariyla kuruldu!")
        print("\nUygulamayi baslatmak icin:")
        print("  python main_kivy_android.py")
        return 0
    else:
        print("\n[UYARI] Bazi paketler kurulamadi!")
        print("Manuel kurulum icin:")
        print("  pip install openai==0.28.1 PyPDF2 python-dotenv")
        return 1

if __name__ == '__main__':
    sys.exit(main())
