from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from datetime import datetime
from config import Config
from ai_service import AIService
from email_service import EmailService

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=["*"])
ai_service = AIService()
email_service = EmailService()


CONTACT_FORM_TEMPLATE = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kontakt AI - Kajpa.pl</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .loader {
            border: 4px solid #f3f4f6;
            border-radius: 50%;
            border-top: 4px solid #6366f1;
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-2xl">
        <!-- Header -->
        <div class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">Kontakt z AI Assistant</h1>
            <p class="text-gray-600">Zadaj pytanie o nasze usługi, a AI przygotuje dla Ciebie odpowiedź i wycenę</p>
        </div>
        
        <!-- Formularz -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <form id="contactForm" class="space-y-4">
                <div>
                    <label for="name" class="block text-sm font-medium text-gray-700 mb-1">Imię i nazwisko</label>
                    <input type="text" id="name" name="name" required 
                           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                </div>
                
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <input type="email" id="email" name="email" required 
                           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                </div>
                
                <div>
                    <label for="message" class="block text-sm font-medium text-gray-700 mb-1">Twoje pytanie</label>
                    <textarea id="message" name="message" rows="6" required placeholder="Opisz swój projekt, zadaj pytanie o cenę lub usługi..."
                              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"></textarea>
                </div>
                
                <button type="submit" id="submitBtn" 
                        class="w-full bg-indigo-600 text-white py-3 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 font-medium transition-colors">
                    <span id="submitText">🤖 Zapytaj AI o wycenę</span>
                    <div id="submitLoader" class="loader mx-auto hidden"></div>
                </button>
            </form>
        </div>
        
        <!-- Odpowiedź AI -->
        <div id="responseContainer" class="bg-white rounded-lg shadow-lg p-6 hidden">
            <h3 class="text-lg font-semibold text-gray-800 mb-3">Odpowiedź AI:</h3>
            <div id="aiResponse" class="prose max-w-none text-gray-700 whitespace-pre-line"></div>
            <div class="mt-4 p-3 bg-green-50 rounded-md">
                <p class="text-sm text-green-800">✅ Odpowiedź została wysłana na Twój email!</p>
                <p class="text-xs text-green-600 mt-1">Sprawdź skrzynkę odbiorczą (oraz spam) w ciągu kilku minut.</p>
            </div>
        </div>
        
        <!-- Error message -->
        <div id="errorContainer" class="bg-red-50 border border-red-200 rounded-lg p-4 hidden">
            <p class="text-red-800">❌ <span id="errorMessage"></span></p>
        </div>
        
        <!-- Info -->
        <div class="mt-8 text-center text-sm text-gray-500">
            <p>🤖 System AI automatycznie przygotuje odpowiedź i wyśle ją na Twój email</p>
            <p class="mt-1">📧 Dla pilnych spraw: <a href="mailto:kontakt@kajpa.pl" class="text-indigo-600 hover:underline">kontakt@kajpa.pl</a></p>
        </div>
    </div>

    <script>
        document.getElementById('contactForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const submitText = document.getElementById('submitText');
            const submitLoader = document.getElementById('submitLoader');
            const responseContainer = document.getElementById('responseContainer');
            const errorContainer = document.getElementById('errorContainer');
            
            // Pokaż loader
            submitText.classList.add('hidden');
            submitLoader.classList.remove('hidden');
            submitBtn.disabled = true;
            responseContainer.classList.add('hidden');
            errorContainer.classList.add('hidden');
            
            try {
                const formData = {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    message: document.getElementById('message').value
                };
                
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('aiResponse').textContent = result.ai_response;
                    responseContainer.classList.remove('hidden');
                    
                    // Wyczyść formularz
                    document.getElementById('contactForm').reset();
                } else {
                    throw new Error(result.error || 'Wystąpił błąd podczas przetwarzania zapytania');
                }
                
            } catch (error) {
                document.getElementById('errorMessage').textContent = error.message;
                errorContainer.classList.remove('hidden');
            } finally {
                // Ukryj loader
                submitText.classList.remove('hidden');
                submitLoader.classList.add('hidden');
                submitBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(CONTACT_FORM_TEMPLATE)

@app.route('/api/contact', methods=['POST', 'OPTIONS'])
def handle_contact():
    """
    API endpoint do obsługi zapytań kontaktowych
    
    Returns:
        JSON: Odpowiedź z wynikiem przetwarzania
    """
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:

        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Brak danych w żądaniu'}), 400
        

        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Pole {field} jest wymagane'}), 400
        
        client_name = data['name'].strip()
        client_email = data['email'].strip()
        client_message = data['message'].strip()
        

        print(f"Generowanie odpowiedzi AI dla: {client_email}")
        ai_response = ai_service.generate_response(
            user_message=client_message,
            user_email=client_email,
            user_name=client_name
        )
        

        print(f"Wysyłanie odpowiedzi do klienta: {client_email}")
        email_sent = email_service.send_ai_response_to_client(
            client_email=client_email,
            client_name=client_name,
            original_message=client_message,
            ai_response=ai_response
        )
        
        print(f"Wysyłanie powiadomienia do admina")
        notification_sent = email_service.send_notification_to_admin(
            client_email=client_email,
            client_name=client_name,
            original_message=client_message,
            ai_response=ai_response
        )
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'client_name': client_name,
            'client_email': client_email,
            'message': client_message,
            'ai_response': ai_response,
            'email_sent': email_sent,
            'notification_sent': notification_sent
        }
        
        with open('contact_log.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        return jsonify({
            'success': True,
            'message': 'Zapytanie zostało przetworzone pomyślnie',
            'ai_response': ai_response,
            'email_sent': email_sent,
            'notification_sent': notification_sent
        })
        
    except Exception as e:
        print(f"Błąd podczas przetwarzania zapytania: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Wystąpił błąd podczas przetwarzania zapytania'
        }), 500

@app.route('/api/test-email', methods=['GET'])
def test_email():
    """Endpoint do testowania połączenia email"""
    try:
        connection_ok = email_service.test_connection()
        return jsonify({
            'success': connection_ok,
            'message': 'Połączenie email działa' if connection_ok else 'Błąd połączenia email'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chatbot-demo', methods=['POST', 'OPTIONS'])
def chatbot_demo():
    """
    Demo endpoint dla chatbota na stronie chatboty-ai.html
    Używa prawdziwego OpenAI AI z specjalnym promptem dla chatbotów
    """
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Brak wiadomości'}), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({'error': 'Wiadomość nie może być pusta'}), 400
        
        print(f"Demo chatbot - pytanie użytkownika: {user_message}")
        
        ai_response = ai_service.generate_chatbot_demo_response(user_message)
        
        print(f"Demo chatbot - odpowiedź AI: {ai_response[:100]}...")
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'timestamp': datetime.now().isoformat(),
            'demo_mode': True
        }), 200
        
    except Exception as e:
        print(f"Błąd w demo chatbota: {str(e)}")
        return jsonify({
            'error': 'Przepraszam, wystąpił błąd z AI. Spróbuj ponownie.',
            'fallback_message': 'Jeśli problem będzie się powtarzał, skontaktuj się z nami: kontakt@kajpa.pl',
            'demo_mode': True
        }), 500

@app.route('/api/analytics-demo', methods=['POST', 'OPTIONS'])
def analytics_demo():
    """
    Demo endpoint dla analityki predykcyjnej na stronie analityka-predykcyjna.html
    Generuje symulowane dane analityczne i prognozy
    """
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        data = request.get_json()
        action = data.get('action', 'refresh') if data else 'refresh'
        
        import random
        import time
        
        current_time = int(time.time())
        
        sales_growth = round(random.uniform(15.0, 35.0), 1)
        new_customers = random.randint(280, 420)
        churn_risk = round(random.uniform(8.0, 18.0), 1)
        conversion_rate = round(random.uniform(2.8, 5.4), 1)
        revenue_forecast = random.randint(45000, 85000)
        market_trend = random.choice(['wzrostowy', 'stabilny', 'opadający'])
        
        alerts = [
            {
                'type': 'warning',
                'icon': '⚠️',
                'title': 'Alert predykcyjny',
                'message': f'AI wykryła trend: {random.randint(45, 85)}% większe zainteresowanie produktem {random.choice(["A", "B", "X", "Premium"])} w weekend. Rekomendujemy zwiększenie zapasów o {random.randint(20, 40)}%.'
            },
            {
                'type': 'success', 
                'icon': '🎯',
                'title': 'Okazja biznesowa',
                'message': f'Model przewiduje {random.randint(25, 45)}% wzrost konwersji dla segmentu klientów 25-35 lat. Czas na kampanię marketingową!'
            },
            {
                'type': 'info',
                'icon': '📈', 
                'title': 'Trend rynkowy',
                'message': f'Analiza konkurencji wskazuje na {random.randint(15, 30)}% spadek aktywności w Twoim sektorze. Możliwość przejęcia udziału w rynku!'
            },
            {
                'type': 'warning',
                'icon': '👥',
                'title': 'Ryzyko churn',
                'message': f'{random.randint(12, 28)} klientów premium wykazuje oznaki rezygnacji. AI rekomenduje akcję retencyjną w ciągu 7 dni.'
            }
        ]
        
        current_alert = random.choice(alerts)
        
        forecasts = {
            '7_days': {
                'visitors': random.randint(1200, 2800),
                'sales': random.randint(8, 24),
                'revenue': random.randint(12000, 35000)
            },
            '30_days': {
                'visitors': random.randint(5000, 12000), 
                'sales': random.randint(45, 120),
                'revenue': random.randint(65000, 180000)
            },
            '90_days': {
                'visitors': random.randint(18000, 45000),
                'sales': random.randint(180, 450), 
                'revenue': random.randint(280000, 650000)
            }
        }
        
        metrics = {
            'sales_growth': {
                'value': f'+{sales_growth}%',
                'label': 'Przewidywany wzrost sprzedaży',
                'period': 'w następnym kwartale',
                'trend': 'up' if sales_growth > 20 else 'stable'
            },
            'new_customers': {
                'value': str(new_customers),
                'label': 'Nowych klientów', 
                'period': 'prognoza na ten miesiąc',
                'trend': 'up' if new_customers > 350 else 'stable'
            },
            'churn_risk': {
                'value': f'{churn_risk}%',
                'label': 'Ryzyko churn',
                'period': 'klienci premium', 
                'trend': 'down' if churn_risk < 12 else 'warning'
            },
            'conversion_rate': {
                'value': f'{conversion_rate}%',
                'label': 'Współczynnik konwersji',
                'period': 'trend 30-dniowy',
                'trend': 'up' if conversion_rate > 4.0 else 'stable'
            }
        }
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'data': {
                'metrics': metrics,
                'alert': current_alert,
                'forecasts': forecasts,
                'market_trend': market_trend,
                'accuracy': random.randint(94, 98),
                'last_update': f'Zaktualizowano {random.randint(1, 5)} min temu'
            }
        }), 200
        
    except Exception as e:
        print(f"Błąd w demo analityki: {str(e)}")
        return jsonify({
            'error': 'Błąd generowania prognozy',
            'fallback_message': 'Skontaktuj się z nami: kontakt@kajpa.pl'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'ai': bool(Config.OPENAI_API_KEY),
            'email': bool(Config.COMPANY_EMAIL_PASSWORD),
            'chatbot_demo': 'operational',
            'analytics_demo': 'operational'
        }
    })

if __name__ == '__main__':
    try:
        Config.validate_config()
        print("✅ Konfiguracja OK")
        
        if email_service.test_connection():
            print("✅ Połączenie email OK")
        else:
            print("⚠️  Ostrzeżenie: Problem z połączeniem email")
        
        print("\n🚀 Uruchamianie aplikacji AI Contact System...")
        print("📧 Formularz dostępny na: http://localhost:5000")
        print("🔧 API dostępne na: http://localhost:5000/api/contact")
        print("❤️  Health check: http://localhost:5000/health")
        
        app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Błąd podczas uruchamiania aplikacji: {str(e)}")
        print("\n💡 Sprawdź czy plik .env zawiera wszystkie wymagane zmienne:")
        print("   - OPENAI_API_KEY")
        print("   - COMPANY_EMAIL_PASSWORD")