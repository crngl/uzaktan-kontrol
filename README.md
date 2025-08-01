# Webmail Kontrol Sistemi

Bu proje, webmail sunucusunun sürekli olarak izlenmesi ve sorun durumunda uyarı gönderilmesi için geliştirilmiş bir Python uygulamasıdır.

## Özellikler

- 🌐 **Webmail İzleme**: Webmail sunucusunu 5 dakikada bir kontrol eder
- 📧 **Email Uyarıları**: Sorun durumunda otomatik email gönderir
- 🔊 **Sesli Uyarılar**: Farklı durumlar için bip sesleri
- 🖥️ **Masaüstü Arayüzü**: Kullanıcı dostu GUI ile kolay kontrol
- 📊 **Gerçek Zamanlı Durum**: Sistem durumunu anlık takip
- 📝 **Detaylı Loglar**: Tüm işlemlerin kayıtları

## Kurulum

1. **Python Kurulumu**: Python 3.7 veya üzeri gerekli
2. **Kütüphaneleri Yükle**:
   ```bash
   pip install -r requirements.txt
   ```

## Kullanım

### Masaüstü Uygulaması (Önerilen)

1. `webmail_monitor.bat` dosyasına çift tıklayın
2. Veya komut satırından:
   ```bash
   python kontrol_gui.py
   ```

### Komut Satırı Uygulaması

```bash
python kontrol.py
```

## Arayüz Özellikleri

### Kontrol Paneli
- **▶️ Başlat/⏹️ Durdur**: İzlemeyi başlatır veya durdurur
- **📧 Mail Testi**: Email gönderme sistemini test eder
- **🔊 Ses Testi**: Bip seslerini test eder
- **🌐 Webmail Testi**: Webmail bağlantısını test eder

### Sistem Durumu
- **📊 İzleme Durumu**: Sistemin çalışıp çalışmadığı
- **🕐 Son Kontrol**: En son kontrol zamanı
- **🌐 Webmail Durumu**: Webmail sunucusunun durumu
- **📧 Mail Durumu**: Email gönderme sisteminin durumu
- **⏰ Sonraki Kontrol**: Bir sonraki kontrol zamanı

### Log Alanı
- Tüm sistem aktivitelerinin detaylı kayıtları
- Gerçek zamanlı güncelleme
- Logları temizleme özelliği

## Uyarı Türleri

### Sesli Uyarılar
- **Başlangıç Sesi**: Sistem başlatıldığında
- **Uyarı Sesi**: Normal hata durumunda
- **Kritik Hata Sesi**: Ciddi sorun durumunda
- **Kapanış Sesi**: Sistem durdurulduğunda

### Email Uyarıları
- **⚠️ Webmail Uyarısı**: HTTP hata kodları
- **⏰ Zaman Aşımı**: Sunucu yavaş yanıt veriyor
- **🔌 Bağlantı Hatası**: Sunucu erişilemiyor
- **🚨 Genel Hata**: Beklenmeyen hatalar

## Yapılandırma

**Dikkat:**  
Uygulamayı kullanmadan önce, kendi e-posta adresinizi (`EMAIL`) ve geçiş/uygulama anahtarınızı (`PASSWORD`) hem `kontrol_gui.py` hem de `kontrol.py` dosyalarına eklemelisiniz. Aksi takdirde e-posta gönderimi çalışmaz.  

Email ayarlarını `kontrol_gui.py` dosyasında değiştirebilirsiniz:

```python
EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

**Not**: Gmail için "Uygulama Şifresi" kullanmanız gerekir.

## Dosya Yapısı

```
uzaktan_kontrol/
├── kontrol.py          # Komut satırı uygulaması
├── kontrol_gui.py      # Masaüstü uygulaması
├── webmail_monitor.bat # Başlatma dosyası
├── requirements.txt    # Gerekli kütüphaneler
└── README.md          # Bu dosya
```

## Sistem Gereksinimleri

- Windows 10/11
- Python 3.7+
- İnternet bağlantısı
- Gmail hesabı (uygulama şifresi ile)

## Sorun Giderme

### Uygulama Açılmıyor
1. Python'un yüklü olduğundan emin olun
2. `pip install -r requirements.txt` komutunu çalıştırın
3. `kontrol_gui.py` dosyasının mevcut olduğunu kontrol edin

### Email Gönderilmiyor
1. Gmail uygulama şifresini kontrol edin
2. İnternet bağlantısını kontrol edin
3. Gmail hesabında 2FA'nın açık olduğundan emin olun

### Ses Çalmıyor
1. Sistem sesinin açık olduğunu kontrol edin
2. Windows ses sürücülerinin güncel olduğundan emin olun

## Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında lisanslanmıştır.

Detaylar için `LICENSE` dosyasını inceleyebilirsiniz.

## İletişim

Sorularınız için: cerengol21@gmail.com 
