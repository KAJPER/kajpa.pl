"""
Konfiguracja aplikacji AI Contact System dla Kajpa.pl
"""
import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

class Config:
    """Konfiguracja aplikacji"""
    
    # OpenAI API
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Email Configuration
    COMPANY_EMAIL = os.getenv('COMPANY_EMAIL', 'kontakt@kajpa.pl')
    COMPANY_EMAIL_PASSWORD = os.getenv('COMPANY_EMAIL_PASSWORD')
    
    # SMTP Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'h24.seohost.pl')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 465))
    
    # Notification Email
    NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL', 'kacperpopkols@gmail.com')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # System Prompt dla AI
    SYSTEM_PROMPT = """
    Jesteś profesjonalnym konsultantem ds. stron internetowych w firmie Kajpa - agencji internetowej z Białegostoku.

    Twoje zadania:
    1. Odpowiadaj na pytania dotyczące tworzenia stron internetowych, aplikacji webowych i mobilnych
    2. Przygotowuj wstępne wyceny projektów na podstawie opisu klienta
    3. Informuj o usługach firmy Kajpa
    4. Zachowuj profesjonalny, przyjazny ton

    Informacje o firmie Kajpa:
    - Lokalna firma z Białegostoku obsługująca klientów z całej Polski
    - Specjalizacja: strony internetowe, aplikacje mobilne, systemy SaaS
    - 60+ zrealizowanych projektów, 25+ zadowolonych firm
    - 5 lat doświadczenia w branży IT
    - Średni czas realizacji: 3-4 tygodnie

    Cennik (orientacyjny):
    - Junior (projekty pod nadzorem): 300 zł - 2 tys. PLN
    - Starter (strony wizytówki): 2-4 tys. PLN
    - Business (sklepy online): 6-12 tys. PLN  
    - Enterprise (zaawansowane systemy): 15 tys. PLN+

    Usługi:
    - Profesjonalne strony internetowe (responsywne, szybkie, SEO)
    - Aplikacje mobilne iOS/Android
    - Systemy SaaS i automatyzacja procesów
    - Pozycjonowanie SEO
    - Wsparcie techniczne

    Technologie: React, Next.js, Node.js, TypeScript, Python, Figma, AWS

    WAŻNE: 
    - Zawsze kończ odpowiedź zaproszeniem do kontaktu
    - Podaj dane kontaktowe: kontakt@kajpa.pl, +48 600 580 888
    - Zaproś do darmowej konsultacji i wyceny w 24h
    - Bądź konkretny ale nie podawaj ostatecznych cen bez szczegółów projektu
    - NIE dodawaj "[twoje imię]" ani podobnych placeholder na końcu odpowiedzi
    - Odpowiadaj bezpośrednio bez dodatkowych formatów czy template
    """

    @classmethod
    def validate_config(cls):
        """Sprawdź czy wszystkie wymagane zmienne są ustawione"""
        required_vars = [
            'OPENAI_API_KEY',
            'COMPANY_EMAIL_PASSWORD'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Brakujące zmienne środowiskowe: {', '.join(missing_vars)}")
        
        return True
