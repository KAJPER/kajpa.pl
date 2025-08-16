import openai
from config import Config

class AIService:

    def __init__(self):
        
        if not Config.OPENAI_API_KEY:
            raise ValueError("Brak klucza API OpenAI w konfiguracji")
        
        openai.api_key = Config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generate_response(self, user_message: str, user_email: str = None, user_name: str = None) -> str:
        
        try:
            context = f"Zapytanie od: {user_name or 'Klient'}"
            if user_email:
                context += f" ({user_email})"
            context += f"\n\nPytanie: {user_message}"
            
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
            
            ai_response = ai_response.replace("[Twoje Imię]", "").replace("[twoje imię]", "")
            ai_response = ai_response.replace("Pozdrawiam,\nKonsultant ds. stron internetowych w Kajpa", "")
            ai_response = ai_response.strip()
            
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
            return self._get_fallback_response(user_name)
    
    def generate_chatbot_demo_response(self, user_message):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": Config.CHATBOT_DEMO_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            ai_response = ai_response.replace("[Twoje Imię]", "").replace("[twoje imię]", "")
            ai_response = ai_response.replace("Pozdrawiam,\nKonsultant ds. stron internetowych w Kajpa", "")
            ai_response = ai_response.replace("Pozdrawiam,\nAsystent AI Kajpa", "")
            ai_response = ai_response.strip()
            
            return ai_response
            
        except Exception as e:
            print(f"Błąd podczas generowania odpowiedzi demo chatbota: {str(e)}")
            return "Cześć! 👋 Jestem Asystentem AI Kajpa. Przepraszam, ale mam chwilowe problemy techniczne. Skontaktuj się z nami bezpośrednio: 📧 kontakt@kajpa.pl, 📞 +48 600 580 888"
    
    def _get_fallback_response(self, user_name: str = None) -> str:
        
        greeting = f"Dzień dobry {user_name}!" if user_name else "Dzień dobry!"
        
        return f

    def is_pricing_request(self, message: str) -> bool:
        
        pricing_keywords = [
            'cena', 'koszt', 'ile kosztuje', 'wycena', 'cennik', 'ile płacę',
            'budżet', 'koszty', 'ile wynosi', 'opłata', 'price', 'cost'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in pricing_keywords)