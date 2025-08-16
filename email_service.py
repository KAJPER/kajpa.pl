"""
Serwis do wysyłania maili - odpowiedzi do klientów i powiadomień
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from config import Config

class EmailService:
    """Serwis do wysyłania maili"""
    
    def __init__(self):
        """Inicjalizacja serwisu email"""
        Config.validate_config()
        
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.company_email = Config.COMPANY_EMAIL
        self.company_password = Config.COMPANY_EMAIL_PASSWORD
        self.notification_email = Config.NOTIFICATION_EMAIL
    
    def send_ai_response_to_client(self, client_email: str, client_name: str, 
                                 original_message: str, ai_response: str) -> bool:
        """
        Wysyła odpowiedź AI do klienta
        
        Args:
            client_email (str): Email klienta
            client_name (str): Imię klienta
            original_message (str): Oryginalna wiadomość klienta
            ai_response (str): Odpowiedź wygenerowana przez AI
        
        Returns:
            bool: True jeśli wysłano pomyślnie
        """
        try:
            # Utwórz wiadomość
            msg = MIMEMultipart()
            msg['From'] = self.company_email
            msg['To'] = client_email
            msg['Subject'] = f"Odpowiedź na Twoje zapytanie - Kajpa.pl"
            
            # Treść maila
            email_body = f"""
Dzień dobry {client_name}!

Dziękujemy za zainteresowanie naszymi usługami!

Oto odpowiedź na Twoje zapytanie:

{ai_response}

Jeśli masz dodatkowe pytania, chętnie na nie odpowiemy.

---
Twoje oryginalne zapytanie:
"{original_message}"
---

Z poważaniem,
Zespół Kajpa
www.kajpa.pl
kontakt@kajpa.pl
+48 600 580 888
"""
            
            msg.attach(MIMEText(email_body, 'plain', 'utf-8'))
            
            # Wyślij email
            return self._send_email(msg)
            
        except Exception as e:
            print(f"Błąd podczas wysyłania odpowiedzi do klienta: {str(e)}")
            return False
    
    def send_notification_to_admin(self, client_email: str, client_name: str, 
                                 original_message: str, ai_response: str) -> bool:
        """
        Wysyła powiadomienie do administratora o nowej odpowiedzi
        
        Args:
            client_email (str): Email klienta
            client_name (str): Imię klienta  
            original_message (str): Oryginalna wiadomość klienta
            ai_response (str): Odpowiedź wygenerowana przez AI
        
        Returns:
            bool: True jeśli wysłano pomyślnie
        """
        try:
            # Utwórz wiadomość
            msg = MIMEMultipart()
            msg['From'] = self.company_email
            msg['To'] = self.notification_email
            msg['Subject'] = f"[KAJPA] Nowe zapytanie od {client_name} - AI odpowiedziało"
            
            # Treść powiadomienia
            notification_body = f"""
NOWE ZAPYTANIE KLIENTA - AI AUTOMATYCZNIE ODPOWIEDZIAŁO

📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 Klient: {client_name}
📧 Email: {client_email}

ZAPYTANIE KLIENTA:
{original_message}

ODPOWIEDŹ AI WYSŁANA DO KLIENTA:
{ai_response}

---
To powiadomienie zostało wygenerowane automatycznie przez system AI Contact.
Skontaktuj się z klientem jeśli potrzebna jest dodatkowa obsługa.

System Kajpa AI Contact
"""
            
            msg.attach(MIMEText(notification_body, 'plain', 'utf-8'))
            
            # Wyślij powiadomienie
            return self._send_email(msg)
            
        except Exception as e:
            print(f"Błąd podczas wysyłania powiadomienia do admina: {str(e)}")
            return False
    
    def _send_email(self, msg: MIMEMultipart) -> bool:
        """
        Wewnętrzna funkcja do wysyłania maili przez SMTP
        
        Args:
            msg (MIMEMultipart): Przygotowana wiadomość email
        
        Returns:
            bool: True jeśli wysłano pomyślnie
        """
        try:
            # Utwórz bezpieczne połączenie SSL
            context = ssl.create_default_context()
            
            # Połącz z serwerem SMTP
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                # Zaloguj się
                server.login(self.company_email, self.company_password)
                
                # Wyślij email
                text = msg.as_string()
                server.sendmail(msg['From'], msg['To'], text)
                
                print(f"Email wysłany pomyślnie do: {msg['To']}")
                return True
                
        except smtplib.SMTPAuthenticationError as e:
            print(f"Błąd uwierzytelniania SMTP: {str(e)}")
            return False
        except smtplib.SMTPException as e:
            print(f"Błąd SMTP: {str(e)}")
            return False
        except Exception as e:
            print(f"Nieoczekiwany błąd podczas wysyłania maila: {str(e)}")
            return False
    
    def test_connection(self) -> bool:
        """
        Testuje połączenie z serwerem SMTP
        
        Returns:
            bool: True jeśli połączenie działa
        """
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.company_email, self.company_password)
                print("Połączenie z serwerem email działa poprawnie!")
                return True
        except Exception as e:
            print(f"Błąd połączenia z serwerem email: {str(e)}")
            return False
