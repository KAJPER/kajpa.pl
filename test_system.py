"""
Skrypt testowy dla AI Contact System
"""
import requests
import json
from config import Config
from email_service import EmailService
from ai_service import AIService

def test_configuration():
    """Test konfiguracji"""
    print("🔧 Testowanie konfiguracji...")
    try:
        Config.validate_config()
        print("✅ Konfiguracja jest poprawna")
        return True
    except Exception as e:
        print(f"❌ Błąd konfiguracji: {e}")
        return False

def test_ai_service():
    """Test serwisu AI"""
    print("\n🤖 Testowanie serwisu AI...")
    try:
        ai = AIService()
        response = ai.generate_response(
            user_message="Ile kosztuje strona internetowa?",
            user_email="test@example.com",
            user_name="Test User"
        )
        print("✅ AI Service działa poprawnie")
        print(f"Przykładowa odpowiedź (pierwsze 100 znaków): {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Błąd AI Service: {e}")
        return False

def test_email_service():
    """Test serwisu email"""
    print("\n📧 Testowanie serwisu email...")
    try:
        email_service = EmailService()
        connection_ok = email_service.test_connection()
        if connection_ok:
            print("✅ Połączenie email działa")
            return True
        else:
            print("❌ Problem z połączeniem email")
            return False
    except Exception as e:
        print(f"❌ Błąd Email Service: {e}")
        return False

def test_api_endpoint():
    """Test API endpoint (jeśli serwer działa)"""
    print("\n🌐 Testowanie API endpoint...")
    try:
        # Test health check
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check działa")
            
            # Test contact endpoint
            test_data = {
                "name": "Test User",
                "email": "test@example.com", 
                "message": "To jest test systemu AI Contact"
            }
            
            contact_response = requests.post(
                "http://localhost:5000/api/contact",
                json=test_data,
                timeout=30
            )
            
            if contact_response.status_code == 200:
                result = contact_response.json()
                if result.get('success'):
                    print("✅ API Contact endpoint działa")
                    return True
                else:
                    print(f"❌ API zwróciło błąd: {result.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ API Contact endpoint błąd: {contact_response.status_code}")
                return False
        else:
            print(f"❌ Health check błąd: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Serwer nie jest uruchomiony (nie można połączyć z localhost:5000)")
        print("   Uruchom 'python app.py' w osobnym terminalu i spróbuj ponownie")
        return False
    except Exception as e:
        print(f"❌ Błąd API test: {e}")
        return False

def main():
    """Uruchom wszystkie testy"""
    print("=" * 50)
    print("🧪 AI CONTACT SYSTEM - TESTY")
    print("=" * 50)
    
    tests = [
        ("Konfiguracja", test_configuration),
        ("AI Service", test_ai_service), 
        ("Email Service", test_email_service),
        ("API Endpoints", test_api_endpoint)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} się nie powiódł: {e}")
            results.append((test_name, False))
    
    # Podsumowanie
    print("\n" + "=" * 50)
    print("📊 PODSUMOWANIE TESTÓW")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nWynik: {passed}/{len(results)} testów przeszło pomyślnie")
    
    if passed == len(results):
        print("\n🎉 Wszystkie testy przeszły! System jest gotowy do użycia.")
        print("\n🚀 Uruchom aplikację: python app.py")
        print("🌐 Formularz: http://localhost:5000")
    else:
        print("\n⚠️  Niektóre testy nie przeszły. Sprawdź konfigurację.")
        print("\n💡 Upewnij się, że:")
        print("   1. Plik .env zawiera wszystkie wymagane zmienne")
        print("   2. Klucz OpenAI API jest poprawny")
        print("   3. Ustawienia email są prawidłowe")

if __name__ == "__main__":
    main()
