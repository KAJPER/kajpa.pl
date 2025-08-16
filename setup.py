#!/usr/bin/env python3
"""
Prosty setup dla AI Contact System
"""
import os
import sys

def main():
    print("🚀 AI Contact System - Setup")
    print(f"Python: {sys.version}")
    print(f"Katalog: {os.getcwd()}")
    
    # Sprawdź czy pliki istnieją
    files_to_check = [
        'app.py',
        'app_minimal.py', 
        'requirements.txt',
        'config.py'
    ]
    
    print("\n📁 Sprawdzanie plików:")
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - BRAK")
    
    # Sprawdź zmienne środowiskowe
    print("\n🔑 Zmienne środowiskowe:")
    env_vars = [
        'OPENAI_API_KEY',
        'COMPANY_EMAIL', 
        'SMTP_SERVER'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * 10}{value[-4:]}")
        else:
            print(f"❌ {var}: BRAK")
    
    print("\n✅ Setup completed!")
    return True

if __name__ == "__main__":
    main()
