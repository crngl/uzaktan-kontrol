import os
import time
import smtplib
import requests
import winsound
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

EMAIL = "@gmail.com" #mail girilecek
PASSWORD = "c" #geçiş anahtarı girilecek
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  


def play_alert_beep():
    """Hata durumunda uyarı bip sesi"""
    try:
        
        winsound.Beep(800, 500)
        time.sleep(0.2)
        winsound.Beep(800, 500)
        print("[🔊] Uyarı bip sesi çalındı")
    except Exception as e:
        print(f"[HATA - Bip sesi] Uyarı sesi çalınamadı: {e}")

def play_error_beep():
    """Kritik hata durumunda bip sesi"""
    try:
         
        for _ in range(3):
            winsound.Beep(1000, 300)
            time.sleep(0.1)
        print("[🔊] Kritik hata bip sesi çalındı")
    except Exception as e:
        print(f"[HATA - Bip sesi] Kritik hata sesi çalınamadı: {e}")

def play_startup_beep():
    """Sistem başlangıç bip sesi"""
    try:
        
        winsound.Beep(600, 200)
        time.sleep(0.1)
        winsound.Beep(800, 200)
        print("[🔊] Başlangıç bip sesi çalındı")
    except Exception as e:
        print(f"[HATA - Bip sesi] Başlangıç sesi çalınamadı: {e}")

def play_shutdown_beep():
    """Sistem kapanış bip sesi"""
    try:
        
        winsound.Beep(800, 200)
        time.sleep(0.1)
        winsound.Beep(600, 200)
        print("[🔊] Kapanış bip sesi çalındı")
    except Exception as e:
        print(f"[HATA - Bip sesi] Kapanış sesi çalınamadı: {e}")

def send_alert_email(subject, body):
    try:
        
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = EMAIL
        msg['To'] = EMAIL
        
        
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()  
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        
        print(f"[📧] Hata uyarısı maili başarıyla gönderildi: {subject}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"[HATA - Kimlik doğrulama] Gmail kimlik bilgileri hatalı: {e}")
        print("Gmail uygulama şifresini kontrol edin!")
        return False
    except smtplib.SMTPException as e:
        print(f"[HATA - SMTP] Mail gönderme hatası: {e}")
        return False
    except Exception as e:
        print(f"[HATA - Genel] Mail gönderilemedi: {e}")
        return False


def send_alert_with_beep(subject, body, is_critical=False):
    print(f"[🚨] HATA TESPİT EDİLDİ! Uyarılar gönderiliyor...")
    
    
    if is_critical:
        play_error_beep()
    else:
        play_alert_beep()
    
    
    mail_sent = send_alert_email(subject, body)
    
    if mail_sent:
        print("[✅] Hem bip sesi hem mail uyarısı başarıyla gönderildi!")
    else:
        print("[⚠️] Mail gönderilemedi ama bip sesi verildi!")

def check_webmail():
    url = "http://webmail.ilbank.gov.tr"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        print(f"[🔍] Webmail kontrolü başlatılıyor... {current_time}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"[✅] Webmail çalışıyor. HTTP 200 OK")
            return True
        else:
            print(f"[❌] Webmail yanıt verdi ama hata kodu: {response.status_code}")
            send_alert_with_beep(
                f"⚠️ Webmail Uyarısı - {current_time}",
                f"Webmail sunucusu yanıt verdi ama hata kodu döndürdü.\n\n"
                f"URL: {url}\n"
                f"HTTP Kodu: {response.status_code}\n"
                f"Zaman: {current_time}\n\n"
                f"Lütfen kontrol edin!",
                is_critical=False
            )
            return False
            
    except requests.exceptions.Timeout:
        print(f"[❌] Webmail zaman aşımı hatası")
        send_alert_with_beep(
            f"⏰ Webmail Zaman Aşımı - {current_time}",
            f"Webmail sunucusuna erişim zaman aşımına uğradı.\n\n"
            f"URL: {url}\n"
            f"Zaman: {current_time}\n"
            f"Timeout: 10 saniye\n\n"
            f"Sunucu yavaş yanıt veriyor veya erişilemiyor!",
            is_critical=True
        )
        return False
        
    except requests.exceptions.ConnectionError:
        print(f"[❌] Webmail bağlantı hatası")
        send_alert_with_beep(
            f"🔌 Webmail Bağlantı Hatası - {current_time}",
            f"Webmail sunucusuna bağlantı kurulamadı.\n\n"
            f"URL: {url}\n"
            f"Zaman: {current_time}\n\n"
            f"Sunucu kapalı olabilir veya ağ sorunu var!",
            is_critical=True
        )
        return False
        
    except Exception as e:
        print(f"[❌] Webmail kontrolünde beklenmeyen hata: {e}")
        send_alert_with_beep(
            f"🚨 Webmail Genel Hata - {current_time}",
            f"Webmail kontrolünde beklenmeyen bir hata oluştu.\n\n"
            f"URL: {url}\n"
            f"Hata: {str(e)}\n"
            f"Zaman: {current_time}\n\n"
            f"Lütfen sistem durumunu kontrol edin!",
            is_critical=True
        )
        return False

def test_mail_sending():
    print("[🧪] Mail gönderme testi başlatılıyor...")
    success = send_alert_email(
        "🧪 Mail Testi",
        "Bu bir test mailidir. Mail gönderme sistemi çalışıyor."
    )
    if success:
        print("[✅] Mail testi başarılı!")
    else:
        print("[❌] Mail testi başarısız!")
    return success


def test_beep_sounds():
    print("[🔊] Bip sesi testi başlatılıyor...")
    print("Başlangıç sesi:")
    play_startup_beep()
    time.sleep(1)
    print("Uyarı sesi:")
    play_alert_beep()
    time.sleep(1)
    print("Kritik hata sesi:")
    play_error_beep()
    time.sleep(1)
    print("Kapanış sesi:")
    play_shutdown_beep()
    print("[✅] Bip sesi testi tamamlandı!")

if __name__ == "__main__":
    print("🚀 Webmail Kontrol Sistemi Başlatılıyor...")
    print(f"📧 Mail adresi: {EMAIL}")
    print("⏰ Kontrol aralığı: 5 dakika")
    print("🔊 Sesli uyarı: Bip sesleri")
    print("-" * 50)
    
    
    print("İlk çalıştırma - testler yapılıyor...")
    test_beep_sounds()
    test_mail_sending()
    print("-" * 50)
    
    
    play_startup_beep()
    
    while True:
        try:
            check_webmail()
            print(f"[⏳] 5 dakika bekleniyor... {datetime.now().strftime('%H:%M:%S')}")
            time.sleep(350)  
        except KeyboardInterrupt:
            print("\n[🛑] Program kullanıcı tarafından durduruldu.")
            play_shutdown_beep()
            break
        except Exception as e:
            print(f"[🚨] Ana döngüde hata: {e}")
            play_error_beep()
            time.sleep(350)  
