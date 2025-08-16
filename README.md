# Kajpa.pl - Website & AI Contact System

Kompletny projekt strony internetowej agencji internetowej Kajpa z zaawansowanym systemem AI do obsługi kontaktów.

## 🏗️ Architektura Projektu

### Frontend (Website)
Responsywna strona internetowa z 4 głównymi sekcjami i dedykowanymi subpages

### Backend (AI System)  
Flask API z integracją OpenAI GPT-4 do automatycznych odpowiedzi na zapytania klientów

## 📁 Struktura Plików

### 🌐 Frontend - Strony HTML

#### Główne Strony
- **`index.html`** - Strona główna agencji internetowej z sekcjami: hero, o nas, usługi, portfolio, zespół, cennik, FAQ, kontakt. Zawiera integrację z AI backend przez formularz kontaktowy.
- **`portfolio.html`** - Prezentacja 5 projektów: EliteGram, Glowee AI, iWalk, LearnPilot, Rolletic z opisami technologii i rezultatów.

#### Subpages AI Solutions  
- **`chatboty-ai.html`** - Dedykowana strona dla chatbotów AI z demo na żywo, 3 pakietami cenowymi (2,5k-15k PLN), statystykami skuteczności.
- **`analityka-predykcyjna.html`** - Analityka predykcyjna z interaktywnym dashboard, case studies 94%+ dokładności, pakiety 8,5k-45k PLN.
- **`narzedzia-automatyzacji.html`** - Automatyzacja procesów biznesowych, kalkulator oszczędności, 6 kategorii automatyzacji, pakiety 4,5k-25k PLN.
- **`silniki-personalizacji.html`** - Personalizacja UX, porównanie strony standardowej vs spersonalizowanej, A/B testing, pakiety 6,5k-35k PLN.

#### Blog Pages
- **`blog-case-studies.html`** - Artykuł o case studies z konkretymi projektami i rezultatami
- **`blog-ceny-stron.html`** - Analiza rosnących kosztów tworzenia stron internetowych w 2024-2025
- **`blog-poradniki.html`** - Praktyczne poradniki dla klientów planujących strony internetowe  
- **`blog-trendy-2025.html`** - Przewidywane trendy webowe na 2025 rok

### 🤖 Backend - Python AI System

#### Core Application
- **`app.py`** - Główna aplikacja Flask z 4 endpointami: `/api/contact` (główny AI contact), `/api/chatbot-demo` (demo chatbota), `/api/analytics-demo` (demo analityki), `/health` (health check). Obsługuje CORS, JSON requests, error handling.

#### AI Services
- **`ai_service.py`** - Serwis OpenAI z 2 metodami: `generate_response()` używa głównego prompta dla kontaktów, `generate_chatbot_demo_response()` używa specjalnego prompta dla demo chatbota. Model GPT-4 dla kontaktów, GPT-4o-mini dla demo.

#### Configuration  
- **`config.py`** - Konfiguracja zmiennych środowiskowych (.env), 2 system prompty: `SYSTEM_PROMPT` dla głównego AI, `CHATBOT_DEMO_PROMPT` dla demo chatbota. Walidacja konfiguracji.

#### Email System
- **`email_service.py`** - Wysyłanie emaili przez SMTP (h24.seohost.pl:465 SSL). `send_ai_response_to_client()` wysyła odpowiedź AI do klienta, `send_notification_to_admin()` powiadamia administratora o nowym kontakcie.

### 🔧 Configuration & Testing

#### Dependencies
- **`requirements.txt`** - 6 pakietów Python: Flask 3.0.0, Flask-CORS 4.0.1, openai 1.35.0, python-dotenv 1.0.1, httpx 0.26.0, Werkzeug 3.0.1

#### Setup & Testing
- **`setup.py`** - Skrypt sprawdzający istnienie plików projektu i zmiennych środowiskowych. Weryfikuje OPENAI_API_KEY, COMPANY_EMAIL, SMTP_SERVER.
- **`test_system.py`** - Kompleksowe testy: konfiguracji, AI service, email service, API endpoints. 4 główne testy z szczegółowym reportingiem.

### 📝 Content

#### Blog Content
- **`blog/Dlaczego strony są coraz droższe.txt`** - Artykuł o wzroście kosztów web developmentu o 300% w 5 lat, analiza przyczyn: AI, bezpieczeństwo, mobilność.
- **`blog/Poradniki dla klientów.txt`** - Praktyczne wskazówki dla klientów: wybór firmy, budżetowanie, proces tworzenia strony.
- **`blog/Trendy webowe 2025.txt`** - Prognozy technologiczne: Web 3.0, voice UI, AR/VR, sustainability w webdev.

### 🖼️ Assets

#### Images  
- **`images/`** - Zdjęcia zespołu (dawid.webp, kacper.webp, karolina.webp, krzysztof.webp), loga partnerów (logo_iwalk.svg, logo-glowee.png)
- **`images/blog/`** - Ilustracje do artykułów blogowych (blog-rosnące-ceny.webp, case-studies.webp, poradniki.webp, trendy.webp)
- **`images/portfolio/`** - Screenshots projektów portfolio w formacie .webp (elitegram.pl_.webp, glowee.ai_.webp, iwalk.pl_.webp, learnpilot.pl_.webp, rolletic.bialystok.pl_.webp)

#### Logos
- **`logo/`** - Kompletny brand kit Kajpa: PNG/WEBP w różnych rozmiarach, wersje białe/kolorowe, plik źródłowy PSD (logokajpa.psd)

## 🚀 Funkcjonalności

### 🤖 AI Contact System
1. **Automatyczne odpowiedzi** - OpenAI GPT-4 generuje spersonalizowane odpowiedzi na zapytania
2. **Wysyłanie emaili** - Automatyczne wysyłanie odpowiedzi AI do klientów z danymi kontaktowymi
3. **Powiadomienia admin** - Email do administratora o każdym nowym kontakcie
4. **Wyceny projektów** - AI przygotowuje wstępne wyceny na podstawie opisu projektu

### 🎭 Interactive Demos
1. **Chatbot Demo** - Prawdziwy AI chatbot GPT-4o-mini wytrenowany do prezentacji chatbotów
2. **Analytics Demo** - Symulowane dane analityczne z real-time refresh co 30s
3. **Calculator Demo** - Interaktywny kalkulator oszczędności z automatyzacji
4. **Comparison Demo** - Porównanie strony standardowej vs spersonalizowanej

### 📱 Responsive Design
1. **Mobile-first** - Pełna responsywność na wszystkich urządzeniach
2. **Hamburger menu** - Funkcjonalny na mobile z animacjami
3. **Horizontal scroll** - Tech stack i testimoniale przewijane na mobile
4. **Fixed header** - Zawsze widoczny header na mobile

## 🛠️ Technologie

### Frontend
- **HTML5** - Semantyczny markup
- **TailwindCSS** - Utility-first CSS framework
- **JavaScript ES6+** - Vanilla JS, Fetch API, async/await
- **Responsive Design** - Mobile-first approach

### Backend  
- **Python 3.11+** - Główny język backend
- **Flask 3.0.0** - Micro web framework
- **OpenAI API** - GPT-4 dla głównego AI, GPT-4o-mini dla demo
- **SMTP** - Email sending przez ssl

### Infrastructure
- **CORS** - Cross-Origin Resource Sharing dla frontend-backend komunikacji
- **Environment Variables** - Bezpieczne przechowywanie credentials w .env
- **Error Handling** - Kompleksowa obsługa błędów z fallback responses
- **JSON API** - RESTful endpoints z structured responses

## ⚙️ Konfiguracja

### Wymagane Zmienne Środowiskowe (.env)
```
OPENAI_API_KEY=sk-proj-xxxxx
COMPANY_EMAIL=kontakt@kajpa.pl  
COMPANY_EMAIL_PASSWORD=xxxxx
SMTP_SERVER=xxxxx
SMTP_PORT=465
NOTIFICATION_EMAIL=admin@kajpa.pl
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=production-secret-key
```

### Instalacja
```bash
pip install -r requirements.txt
python setup.py          # Weryfikacja konfiguracji
python test_system.py    # Uruchomienie testów
python app.py            # Start aplikacji
```

## 📊 API Endpoints

### `/api/contact` (POST)
Główny endpoint do obsługi formularza kontaktowego
- **Input**: `{name, email, message}`
- **Process**: OpenAI GPT-4 → Email do klienta → Powiadomienie admin
- **Output**: `{success, ai_response, timestamp}`

### `/api/chatbot-demo` (POST)  
Demo chatbota z prawdziwym AI
- **Input**: `{message}`
- **Process**: OpenAI GPT-4o-mini z chatbot promptem
- **Output**: `{success, response, demo_mode, timestamp}`

### `/api/analytics-demo` (POST)
Symulowane dane analityczne
- **Input**: `{action: 'refresh'}`
- **Process**: Generowanie realistic random data
- **Output**: `{success, data: {metrics, alerts, forecasts}, timestamp}`

### `/health` (GET)
Health check wszystkich serwisów
- **Output**: `{status, services: {ai, email, chatbot_demo, analytics_demo}, timestamp}`

## 🎯 Kluczowe Funkcje

### AI System Prompts
1. **Główny prompt** - Konsultant ds. stron internetowych, cennik 300zł-15k+, kontakt zawsze na końcu
2. **Chatbot prompt** - Specjalista chatbotów, 3 pakiety, konkretne korzyści biznesowe, krótkие odpowiedzi

### Email Templates  
1. **Klient** - Profesjonalny email z odpowiedzią AI + dane kontaktowe + CTA
2. **Admin** - Powiadomienie o nowym kontakcie z pełnymi danymi klienta

### Error Handling
1. **AI fallback** - Zapasowe odpowiedzi gdy OpenAI nie działa
2. **Email fallback** - Logs błędów email z retry mechanism  
3. **CORS errors** - Przyjazne komunikaty o problemach połączenia
4. **Validation** - Walidacja inputów i konfiguracji

## 📈 Performance & Security

### Optymalizacje
- **Image formats** - WebP dla wszystkich zdjęć (70% mniejsze pliki)
- **CSS optimization** - TailwindCSS CDN z tree-shaking
- **API efficiency** - GPT-4o-mini dla demo (szybsze, tańsze)
- **Caching headers** - Odpowiednie cache dla assets

### Bezpieczeństwo
- **Environment variables** - Sensytywne dane w .env nie w kodzie
- **HTTPS enforcement** - SSL/TLS dla SMTP i API calls
- **Input validation** - Walidacja wszystkich user inputs
- **Error masking** - Nie ujawnianie internal errors użytkownikom

## 🌍 Deployment

### Development
```bash
python app.py  # http://localhost:5000
```

### Production (VPS)
```bash
# Na serwerze VPS
python app.py
```

### Frontend URLs
- **Local**: `http://127.0.0.1:5500/`
- **Production**: Statyczne pliki HTML
- **API**: `http://127.0.0.1:5000/api/`

## 📞 Contact & Credits

**Projekt**: Kajpa.pl - Agencja Internetowa  
**Lokalizacja**: Białystok, Polska  
**Email**: kontakt@kajpa.pl  
**Telefon**: +48 600 580 888  

**Zespół**:
- Kacper - CEO & Główny Developer
- Dawid - Frontend Developer  
- Karolina - UI/UX Designer
- Krzysztof - Kierownik

**Technologie**: React, Next.js, Node.js, TypeScript, Python, Figma, AWS, OpenAI GPT-4
