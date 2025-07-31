import os
import time
import smtplib
import requests
import winsound
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import queue


EMAIL = "@gmail.com" #mail girilecek
PASSWORD = "cq" #geçiş anahtarı girilecek
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Parola_Url sabti
PAROLA_URL = "https://parola.ilbank.gov.tr/ilbank/"
# YBS_URL sabiti
YBS_URL = "https://ybs.ilbank.gov.tr"

class WebmailMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Webmail Kontrol Sistemi")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        
        self.monitoring = False
        self.monitor_thread = None
        self.log_queue = queue.Queue()
        
        
        self.create_widgets()
        
        
        self.check_log_queue()
        
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        
        title_label = ttk.Label(main_frame, text="🚀 Webmail Kontrol Sistemi", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        
        control_frame = ttk.LabelFrame(main_frame, text="Kontrol", padding="10")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(1, weight=1)
        
    
        self.start_stop_btn = ttk.Button(control_frame, text="▶️ Başlat", 
                                        command=self.toggle_monitoring, width=15)
        self.start_stop_btn.grid(row=0, column=0, padx=(0, 10))
        
        
        test_frame = ttk.Frame(control_frame)
        test_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Button(test_frame, text="📧 Mail Testi", 
                  command=self.test_mail).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(test_frame, text="🔊 Ses Testi", 
                  command=self.test_sound).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(test_frame, text="🌐 Webmail Testi", 
                  command=self.test_webmail).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(test_frame, text="🌐 Parola Kontrol Et",
                  command=self.test_parola).grid(row=0, column=3, padx=(0, 5))
        ttk.Button(test_frame, text="🌐 YBS Kontrol Et", command=self.test_ybs).grid(row=0, column=4, padx=(0, 5))
        
    
        
        
        status_frame = ttk.LabelFrame(main_frame, text="Sistem Durumu", padding="10")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        
        self.status_labels = {}
        status_items = [
            ("monitoring", "📊 İzleme Durumu:", "Durduruldu"),
            ("last_check", "🕐 Son Kontrol:", "Henüz yapılmadı"),
            ("webmail_status", "🌐 Webmail Durumu:", "Bilinmiyor"),
            ("parola_status", "🌐 Parola Durumu:", "Bilinmiyor"),
            ("ybs_status", "🌐 YBS Durumu:", "Bilinmiyor"),
            ("email_status", "📧 Mail Durumu:", "Bilinmiyor"),
            ("next_check", "⏰ Sonraki Kontrol:", "Bilinmiyor")
        ]
        
        for i, (key, label_text, default_value) in enumerate(status_items):
            ttk.Label(status_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, padx=(0, 10))
            self.status_labels[key] = ttk.Label(status_frame, text=default_value, 
                                               font=("Arial", 9, "bold"))
            self.status_labels[key].grid(row=i, column=1, sticky=tk.W)
        
        
        # -
        logs_frame = ttk.LabelFrame(main_frame, text="Sistem Logları", padding="10")
        logs_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.columnconfigure(1, weight=1)
        logs_frame.columnconfigure(2, weight=1)
        logs_frame.rowconfigure(0, weight=1)

        # Webmail Log 
        webmail_log_frame = ttk.Frame(logs_frame)
        webmail_log_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=3)
        ttk.Label(webmail_log_frame, text="Webmail Logları").pack()
        self.webmail_log_text = scrolledtext.ScrolledText(webmail_log_frame, height=12, width=35, font=("Consolas", 9))
        self.webmail_log_text.pack(fill=tk.BOTH, expand=True)
        ttk.Button(webmail_log_frame, text="🗑️ Temizle", command=lambda: self.webmail_log_text.delete(1.0, tk.END)).pack(pady=(2,0))

        # Parola Log
        parola_log_frame = ttk.Frame(logs_frame)
        parola_log_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=3)
        ttk.Label(parola_log_frame, text="Parola Logları").pack()
        self.parola_log_text = scrolledtext.ScrolledText(parola_log_frame, height=12, width=35, font=("Consolas", 9))
        self.parola_log_text.pack(fill=tk.BOTH, expand=True)
        ttk.Button(parola_log_frame, text="🗑️ Temizle", command=lambda: self.parola_log_text.delete(1.0, tk.END)).pack(pady=(2,0))

        # YBS Log
        ybs_log_frame = ttk.Frame(logs_frame)
        ybs_log_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=3)
        ttk.Label(ybs_log_frame, text="YBS Logları").pack()
        self.ybs_log_text = scrolledtext.ScrolledText(ybs_log_frame, height=12, width=35, font=("Consolas", 9))
        self.ybs_log_text.pack(fill=tk.BOTH, expand=True)
        ttk.Button(ybs_log_frame, text="🗑️ Temizle", command=lambda: self.ybs_log_text.delete(1.0, tk.END)).pack(pady=(2,0))
        
        
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(info_frame, text=f"📧 Mail: {EMAIL}").pack(side=tk.LEFT)
        ttk.Label(info_frame, text="⏰ Kontrol Aralığı: 5 dakika").pack(side=tk.RIGHT)
    
    def log_message(self, message, target_box=None):
        """Log mesajını ilgili kutuya ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        if target_box is not None:
            target_box.insert(tk.END, formatted_message)
            target_box.see(tk.END)
            target_box.update_idletasks()
        else:
            # -
            self.webmail_log_text.insert(tk.END, formatted_message)
            self.webmail_log_text.see(tk.END)
            self.webmail_log_text.update_idletasks()
    
    def check_log_queue(self):
        """Log kuyruğunu kontrol et ve mesajları göster"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message)
                self.log_text.see(tk.END)
                self.log_text.update_idletasks()
        except queue.Empty:
            pass
        finally:
            
            self.root.after(100, self.check_log_queue)
    
    def toggle_monitoring(self):
        """İzlemeyi başlat/durdur"""
        if not self.monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()
    
    def start_monitoring(self):
        """İzlemeyi başlat"""
        self.monitoring = True
        self.start_stop_btn.config(text="⏹️ Durdur")
        self.status_labels["monitoring"].config(text="Çalışıyor", foreground="green")
        
        # 
        self.log_message("🚀 Webmail kontrol sistemi başlatıldı", self.webmail_log_text)
        self.log_message(f"📧 Mail adresi: {EMAIL}", self.webmail_log_text)
        self.log_message("⏰ Kontrol aralığı: 5 dakika", self.webmail_log_text)
        self.log_message("🔊 Sesli uyarı: Aktif", self.webmail_log_text)
        self.log_message("-" * 50, self.webmail_log_text)
        
        
        self.play_startup_beep()
        
        
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """İzlemeyi durdur"""
        self.monitoring = False
        self.start_stop_btn.config(text="▶️ Başlat")
        self.status_labels["monitoring"].config(text="Durduruldu", foreground="red")
        
        self.log_message("🛑 Webmail kontrol sistemi durduruldu")
        self.play_shutdown_beep()
    
    def monitor_loop(self):
        """Otomatik izleme döngüsü"""
        while self.monitoring:
            try:
                self.check_webmail()
                self.check_parola()
                self.check_ybs()  
                self.status_labels["last_check"].config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                self.status_labels["next_check"].config(text=(datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"))
                self.log_message(f"[⏳] 5 dakika bekleniyor... {datetime.now().strftime('%H:%M:%S')}")
                for _ in range(350):
                    if not self.monitoring:
                        break
                    time.sleep(1)
            except Exception as e:
                self.log_message(f"🚨 Ana döngüde hata: {e}")
                self.play_error_beep()
                time.sleep(5)
    
    def check_webmail(self):
        """Webmail kontrolü"""
        url = "http://webmail.ilbank.gov.tr"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            self.log_message(f"🔍 Webmail kontrolü başlatılıyor... {current_time}", self.webmail_log_text)
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                self.log_message(f"✅ Webmail çalışıyor. HTTP 200 OK", self.webmail_log_text)
                self.status_labels["webmail_status"].config(text="✅ Çalışıyor", foreground="green")
                return True
            else:
                self.log_message(f"❌ Webmail yanıt verdi ama hata kodu: {response.status_code}", self.webmail_log_text)
                self.status_labels["webmail_status"].config(text=f"❌ Hata ({response.status_code})", foreground="red")
                self.send_alert_with_beep(
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
            self.log_message(f"❌ Webmail zaman aşımı hatası", self.webmail_log_text)
            self.status_labels["webmail_status"].config(text="❌ Zaman Aşımı", foreground="red")
            self.send_alert_with_beep(
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
            self.log_message(f"❌ Webmail bağlantı hatası", self.webmail_log_text)
            self.status_labels["webmail_status"].config(text="❌ Bağlantı Hatası", foreground="red")
            self.send_alert_with_beep(
                f"🔌 Webmail Bağlantı Hatası - {current_time}",
                f"Webmail sunucusuna bağlantı kurulamadı.\n\n"
                f"URL: {url}\n"
                f"Zaman: {current_time}\n\n"
                f"Sunucu kapalı olabilir veya ağ sorunu var!",
                is_critical=True
            )
            return False
            
        except Exception as e:
            self.log_message(f"❌ Webmail kontrolünde beklenmeyen hata: {e}", self.webmail_log_text)
            self.status_labels["webmail_status"].config(text="❌ Genel Hata", foreground="red")
            self.send_alert_with_beep(
                f"🚨 Webmail Genel Hata - {current_time}",
                f"Webmail kontrolünde beklenmeyen bir hata oluştu.\n\n"
                f"URL: {url}\n"
                f"Hata: {str(e)}\n"
                f"Zaman: {current_time}\n\n"
                f"Lütfen sistem durumunu kontrol edin!",
                is_critical=True
            )
            return False
    
    def send_alert_email(self, subject, body):
        """Mail gönder"""
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
            # -
            self.log_message(f"📧 Hata uyarısı maili başarıyla gönderildi: {subject}", self.webmail_log_text)
            self.status_labels["email_status"].config(text="✅ Çalışıyor", foreground="green")
            return True
        except smtplib.SMTPAuthenticationError as e:
            self.log_message(f"HATA - Kimlik doğrulama: Gmail kimlik bilgileri hatalı: {e}", self.webmail_log_text)
            self.status_labels["email_status"].config(text="❌ Kimlik Hatası", foreground="red")
            return False
        except smtplib.SMTPException as e:
            self.log_message(f"HATA - SMTP: Mail gönderme hatası: {e}", self.webmail_log_text)
            self.status_labels["email_status"].config(text="❌ SMTP Hatası", foreground="red")
            return False
        except Exception as e:
            self.log_message(f"HATA - Genel: Mail gönderilemedi: {e}", self.webmail_log_text)
            self.status_labels["email_status"].config(text="❌ Genel Hata", foreground="red")
            return False
    
    def send_alert_with_beep(self, subject, body, is_critical=False):
        """Hata durumunda hem mail hem bip sesi gönder"""
        # -
        self.log_message(f"🚨 HATA TESPİT EDİLDİ! Uyarılar gönderiliyor...", self.webmail_log_text)
        if is_critical:
            self.play_error_beep()
        else:
            self.play_alert_beep()
        mail_sent = self.send_alert_email(subject, body)
        if mail_sent:
            self.log_message("✅ Hem bip sesi hem mail uyarısı başarıyla gönderildi!", self.webmail_log_text)
        else:
            self.log_message("⚠️ Mail gönderilemedi ama bip sesi verildi!", self.webmail_log_text)
    
    def play_alert_beep(self):
        """Hata durumunda uyarı bip sesi"""
        try:
            winsound.Beep(800, 500)
            time.sleep(0.2)
            winsound.Beep(800, 500)
            self.log_message("🔊 Uyarı bip sesi çalındı")
        except Exception as e:
            self.log_message(f"HATA - Bip sesi: Uyarı sesi çalınamadı: {e}")
    
    def play_error_beep(self):
        """Kritik hata durumunda bip sesi"""
        try:
            for _ in range(3):
                winsound.Beep(1000, 300)
                time.sleep(0.1)
            self.log_message("🔊 Kritik hata bip sesi çalındı")
        except Exception as e:
            self.log_message(f"HATA - Bip sesi: Kritik hata sesi çalınamadı: {e}")
    
    def play_startup_beep(self):
        """Başlangıç bip sesi çal"""
        try:
            winsound.Beep(1000, 200)
            time.sleep(0.1)
            winsound.Beep(1200, 200)
            self.log_message("🔊 Başlangıç bip sesi çalındı", self.webmail_log_text)  
        except Exception as e:
            self.log_message(f"HATA - Bip sesi: Başlangıç sesi çalınamadı: {e}", self.webmail_log_text)
    
    def play_shutdown_beep(self):
        """Sistem kapanış bip sesi"""
        try:
            winsound.Beep(800, 200)
            time.sleep(0.1)
            winsound.Beep(600, 200)
            self.log_message("🔊 Kapanış bip sesi çalındı")
        except Exception as e:
            self.log_message(f"HATA - Bip sesi: Kapanış sesi çalınamadı: {e}")
    
    def test_mail(self):
        """Mail gönderme testi"""
        self.log_message("🧪 Mail gönderme testi başlatılıyor...", self.webmail_log_text)
        success = self.send_alert_email(
            "🧪 Mail Testi",
            "Bu bir test mailidir. Mail gönderme sistemi çalışıyor."
        )
        if success:
            self.log_message("✅ Mail testi başarılı!", self.webmail_log_text)
        else:
            self.log_message("❌ Mail testi başarısız!", self.webmail_log_text)
    
    def test_sound(self):
        """Bip sesi testi"""
        self.log_message("🔊 Bip sesi testi başlatılıyor...")
        
        def play_test_sounds():
            self.log_message("Başlangıç sesi:")
            self.play_startup_beep()
            time.sleep(1)
            self.log_message("Uyarı sesi:")
            self.play_alert_beep()
            time.sleep(1)
            self.log_message("Kritik hata sesi:")
            self.play_error_beep()
            time.sleep(1)
            self.log_message("Kapanış sesi:")
            self.play_shutdown_beep()
            self.log_message("✅ Bip sesi testi tamamlandı!")
        
        
        threading.Thread(target=play_test_sounds, daemon=True).start()
    
    def test_webmail(self):
        """Webmail testi"""
        self.log_message("🌐 Webmail testi başlatılıyor...", self.webmail_log_text)
        # -
        threading.Thread(target=self._test_webmail_thread, daemon=True).start()
    
    def _test_webmail_thread(self):
        """Webmail testini ayrı thread'de çalıştır"""
        success = self.check_webmail()
        if success:
            self.log_message("✅ Webmail testi başarılı!", self.webmail_log_text)
        else:
            self.log_message("❌ Webmail testi başarısız!", self.webmail_log_text)
    


    def check_parola(self):
        """Sabit web sitesi adresini kontrol et"""
        url = PAROLA_URL
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_message(f"🔍 Parola kontrolü başlatılıyor: {url} ({current_time})", self.parola_log_text)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, timeout=30, headers=headers, verify=False)  # HTTPS için verify=False eklendi
            if response.status_code == 200:
                self.log_message(f"✅ {url} çalışıyor. HTTP 200 OK", self.parola_log_text)
                self.status_labels["parola_status"].config(text="✅ Çalışıyor", foreground="green")
            else:
                self.log_message(f"❌ {url} yanıt verdi ama hata kodu: {response.status_code}", self.parola_log_text)
                self.status_labels["parola_status"].config(text=f"❌ Hata ({response.status_code})", foreground="red")
                # Hata durumunda mail gönder
                self.send_alert_with_beep(
                    f"⚠️ Parola Sitesi Hata - {current_time}",
                    f"Parola sitesi yanıt verdi ama hata kodu döndürdü.\n\n"
                    f"URL: {url}\n"
                    f"HTTP Kodu: {response.status_code}\n"
                    f"Zaman: {current_time}\n\n"
                    f"Lütfen kontrol edin!",
                    is_critical=False
                )
        except requests.exceptions.Timeout:
            self.log_message(f"❌ {url} zaman aşımı hatası (30 sn)", self.parola_log_text)
            self.status_labels["parola_status"].config(text="❌ Zaman Aşımı", foreground="red")
            # Zaman aşımı durumunda mail gönder
            self.send_alert_with_beep(
                f"⏰ Parola Sitesi Zaman Aşımı - {current_time}",
                f"Parola sitesine erişim zaman aşımına uğradı.\n\n"
                f"URL: {url}\n"
                f"Zaman: {current_time}\n"
                f"Timeout: 30 saniye\n\n"
                f"Site yavaş yanıt veriyor veya erişilemiyor!",
                is_critical=True
            )
        except requests.exceptions.ConnectionError:
            self.log_message(f"❌ {url} bağlantı hatası", self.parola_log_text)
            self.status_labels["parola_status"].config(text="❌ Bağlantı Hatası", foreground="red")
            # Bağlantı hatası durumunda mail gönder
            self.send_alert_with_beep(
                f"🔌 Parola Sitesi Bağlantı Hatası - {current_time}",
                f"Parola sitesine bağlantı kurulamadı.\n\n"
                f"URL: {url}\n"
                f"Zaman: {current_time}\n\n"
                f"Site kapalı olabilir veya ağ sorunu var!",
                is_critical=True
            )
        except Exception as e:
            self.log_message(f"❌ {url} kontrolünde beklenmeyen hata: {e}", self.parola_log_text)
            self.status_labels["parola_status"].config(text="❌ Genel Hata", foreground="red")
            # Genel hata durumunda mail gönder
            self.send_alert_with_beep(
                f"🚨 Parola Sitesi Genel Hata - {current_time}",
                f"Parola kontrolünde beklenmeyen bir hata oluştu.\n\n"
                f"URL: {url}\n"
                f"Hata: {str(e)}\n"
                f"Zaman: {current_time}\n\n"
                f"Lütfen sistem durumunu kontrol edin!",
                is_critical=True
            )

    def test_parola(self):
        """Parola testi (manuel buton)"""
        self.log_message("🌐 Parola testi başlatılıyor...", self.parola_log_text)
        # Arayüz donma sorunumu çözmek için
        threading.Thread(target=self._test_parola_thread, daemon=True).start()
    
    def _test_parola_thread(self):
        """Parola testini ayrı thread'de çalıştır"""
        self.check_parola()
    
    def check_ybs(self):
        """YBS kontrolü"""
        url = YBS_URL
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_message(f"🔍 YBS kontrolü başlatılıyor... {current_time}", self.ybs_log_text)
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                self.log_message(f"✅ YBS çalışıyor. HTTP 200 OK", self.ybs_log_text)
                self.status_labels["ybs_status"].config(text="✅ Çalışıyor", foreground="green")
                return True
            else:
                self.log_message(f"❌ YBS yanıt verdi ama hata kodu: {response.status_code}", self.ybs_log_text)
                self.status_labels["ybs_status"].config(text=f"❌ Hata ({response.status_code})", foreground="red")
                # Hata durumunda mail gönder
                self.send_alert_with_beep(
                    f"⚠️ YBS Hata - {current_time}",
                    f"YBS sitesi yanıt verdi ama hata kodu döndürdü.\n\n"
                    f"URL: {url}\n"
                    f"HTTP Kodu: {response.status_code}\n"
                    f"Zaman: {current_time}\n\n"
                    f"Lütfen kontrol edin!",
                    is_critical=False
                )
                return False
        except requests.exceptions.Timeout:
            self.log_message(f"❌ YBS zaman aşımı hatası", self.ybs_log_text)
            self.status_labels["ybs_status"].config(text="❌ Zaman Aşımı", foreground="red")
            # Zaman aşımı durumunda mail gönder
            self.send_alert_with_beep(
                f"⏰ YBS Zaman Aşımı - {current_time}",
                f"YBS sitesine erişim zaman aşımına uğradı.\n\n"
                f"URL: {url}\n"
                f"Zaman: {current_time}\n"
                f"Timeout: 30 saniye\n\n"
                f"Site yavaş yanıt veriyor veya erişilemiyor!",
                is_critical=True
            )
            return False
        except requests.exceptions.ConnectionError:
            self.log_message(f"❌ YBS bağlantı hatası", self.ybs_log_text)
            self.status_labels["ybs_status"].config(text="❌ Bağlantı Hatası", foreground="red")
            # Bağlantı hatası durumunda mail gönder
            self.send_alert_with_beep(
                f"🔌 YBS Bağlantı Hatası - {current_time}",
                f"YBS sitesine bağlantı kurulamadı.\n\n"
                f"URL: {url}\n"
                f"Zaman: {current_time}\n\n"
                f"Site kapalı olabilir veya ağ sorunu var!",
                is_critical=True
            )
            return False
        except Exception as e:
            self.log_message(f"❌ YBS kontrolünde beklenmeyen hata: {e}", self.ybs_log_text)
            self.status_labels["ybs_status"].config(text="❌ Genel Hata", foreground="red")
            # Genel hata durumunda mail gönder
            self.send_alert_with_beep(
                f"🚨 YBS Genel Hata - {current_time}",
                f"YBS kontrolünde beklenmeyen bir hata oluştu.\n\n"
                f"URL: {url}\n"
                f"Hata: {str(e)}\n"
                f"Zaman: {current_time}\n\n"
                f"Lütfen sistem durumunu kontrol edin!",
                is_critical=True
            )
            return False

    def test_ybs(self):
        """YBS testi (manuel buton)"""
        self.log_message("🌐 YBS testi başlatılıyor...", self.ybs_log_text)
        # Arayüz donma sorunum için
        threading.Thread(target=self._test_ybs_thread, daemon=True).start()
    
    def _test_ybs_thread(self):
        """YBS testini ayrı thread'de çalıştır"""
        success = self.check_ybs()
        if success:
            self.log_message("✅ YBS testi başarılı!", self.ybs_log_text)
        else:
            self.log_message("❌ YBS testi başarısız!", self.ybs_log_text)
    
    def clear_logs(self):
        """Logları temizle"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("🗑️ Loglar temizlendi")
    
    def on_closing(self):
        """Pencere kapatılırken temizlik yap"""
        if self.monitoring:
            if messagebox.askokcancel("Çıkış", "İzleme devam ediyor. Çıkmak istediğinizden emin misiniz?"):
                self.stop_monitoring()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = WebmailMonitorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 