import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from config import Config

class EmailService:

    def __init__(self):
        
        Config.validate_config()
        
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.company_email = Config.COMPANY_EMAIL
        self.company_password = Config.COMPANY_EMAIL_PASSWORD
        self.notification_email = Config.NOTIFICATION_EMAIL
    
    def send_ai_response_to_client(self, client_email: str, client_name: str, 
                                 original_message: str, ai_response: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.company_email
            msg['To'] = client_email
            msg['Subject'] = f"Odpowiedź na Twoje zapytanie - Kajpa.pl"
            
            email_body = f"""Dzień dobry {client_name}!

Dziękujemy za kontakt z firmą Kajpa. Oto odpowiedź na Twoje zapytanie:

---

{ai_response}

---

Jeśli masz dodatkowe pytania, śmiało odpowiedz na tego maila lub zadzwoń!

📧 kontakt@kajpa.pl
📞 +48 600 580 888

Pozdrawiamy,
Zespół Kajpa
"""
            
            msg.attach(MIMEText(email_body, 'plain', 'utf-8'))
            return self._send_email(msg)
            
        except Exception as e:
            print(f"Błąd podczas wysyłania odpowiedzi do klienta: {str(e)}")
            return False

    def send_notification_to_admin(self, client_email: str, client_name: str, 
                                 original_message: str, ai_response: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.company_email
            msg['To'] = self.notification_email
            msg['Subject'] = f"[KAJPA] Nowe zapytanie od {client_name} - AI odpowiedziało"
            
            notification_body = f"""Otrzymano nowe zapytanie od klienta:

👤 Klient: {client_name}
📧 Email: {client_email}
📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 ZAPYTANIE:
{original_message}

🤖 ODPOWIEDŹ AI:
{ai_response}

---
System AI Kajpa.pl
"""
            
            msg.attach(MIMEText(notification_body, 'plain', 'utf-8'))
            return self._send_email(msg)
            
        except Exception as e:
            print(f"Błąd podczas wysyłania powiadomienia do admina: {str(e)}")
            return False

    def _send_email(self, msg) -> bool:
        try:
            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.company_email, self.company_password)
                
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
        
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.company_email, self.company_password)
                print("Połączenie z serwerem email działa poprawnie!")
                return True
        except Exception as e:
            print(f"Błąd połączenia z serwerem email: {str(e)}")
            return False