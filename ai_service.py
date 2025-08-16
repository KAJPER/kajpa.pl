"""
Serwis AI wykorzystujący OpenAI API do odpowiadania na zapytania klientów
"""
import openai
from config import Config

class AIService:
    """Serwis do komunikacji z OpenAI API"""
    
    def __init__(self):
        """Inicjalizacja serwisu AI"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("Brak klucza API OpenAI w konfiguracji")
        
        # Ustaw klucz API dla OpenAI
        openai.api_key = Config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generate_response(self, user_message: str, user_email: str = None, user_name: str = None) -> str:
        """
        Generuje odpowiedź AI na zapytanie użytkownika
        
        Args:
            user_message (str): Wiadomość od użytkownika
            user_email (str, optional): Email użytkownika
            user_name (str, optional): Imię użytkownika
        
        Returns:
            str: Odpowiedź wygenerowana przez AI
        """
        try:
            # Przygotuj kontekst z danymi użytkownika
            context = f"Zapytanie od: {user_name or 'Klient'}"
            if user_email:
                context += f" ({user_email})"
            context += f"\n\nPytanie: {user_message}"
            
            # Wywołaj OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",  # Użyj najnowszego modelu
                messages=[
                    {
                        "role": "system", 
                        "content": Config.SYSTEM_PROMPT
                    },
                    {
                        "role": "user", 
                        "content": context
                    }
                ],
                max_tokens=1000,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Usuń niepotrzebne placeholder i dodaj kontakt
            # Wyczyść odpowiedź z placeholder
            ai_response = ai_response.replace("[Twoje Imię]", "").replace("[twoje imię]", "")
            ai_response = ai_response.replace("Pozdrawiam,\nKonsultant ds. stron internetowych w Kajpa", "")
            ai_response = ai_response.strip()
            
            # Dodaj dodatkowe informacje kontaktowe na końcu
            contact_footer = """

---
📧 kontakt@kajpa.pl  
📞 +48 600 580 888  
🌐 kajpa.pl  

💡 Skorzystaj z darmowej konsultacji i otrzymaj wycenę w 24h!

Pozdrawiamy,  
Zespół Kajpa
"""
            
            return ai_response + contact_footer
            
        except Exception as e:
            print(f"Błąd podczas generowania odpowiedzi AI: {str(e)}")
            # Fallback odpowiedź w przypadku błędu
            return self._get_fallback_response(user_name)
    
    def _get_fallback_response(self, user_name: str = None) -> str:
        """
        Zwraca zapasową odpowiedź w przypadku problemów z AI
        
        Args:
            user_name (str, optional): Imię użytkownika
        
        Returns:
            str: Zapasowa odpowiedź
        """
        greeting = f"Dzień dobry {user_name}!" if user_name else "Dzień dobry!"
        
        return f"""{greeting}

Dziękujemy za zainteresowanie naszymi usługami!

Jesteśmy agencją internetową Kajpa z Białegostoku, specjalizującą się w:
• Profesjonalnych stronach internetowych
• Aplikacjach mobilnych 
• Sklepach online
• Systemach SaaS i automatyzacji

Realizujemy projekty dla firm z całej Polski. Mamy już 60+ ukończonych projektów i 5 lat doświadczenia.

Chętnie odpowiemy na wszystkie Twoje pytania i przygotujemy bezpłatną wycenę!

📧 kontakt@kajpa.pl  
📞 +48 600 580 888  
🌐 kajpa.pl  

💡 Skorzystaj z darmowej konsultacji i otrzymaj wycenę w 24h!

Pozdrawiamy,  
Zespół Kajpa"""

    def is_pricing_request(self, message: str) -> bool:
        """
        Sprawdza czy wiadomość zawiera zapytanie o cenę
        
        Args:
            message (str): Wiadomość do sprawdzenia
        
        Returns:
            bool: True jeśli to zapytanie o cenę
        """
        pricing_keywords = [
            'cena', 'koszt', 'ile kosztuje', 'wycena', 'cennik', 'ile płacę',
            'budżet', 'koszty', 'ile wynosi', 'opłata', 'price', 'cost'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in pricing_keywords)
