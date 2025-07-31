@echo off
title Webmail Kontrol Sistemi
echo 🚀 Webmail Kontrol Sistemi başlatılıyor...
echo.
echo 📧 Mail: cerengol21@gmail.com
echo ⏰ Kontrol aralığı: 5 dakika
echo 🔊 Sesli uyarı: Aktif
echo.
echo Masaüstü uygulaması açılıyor...
echo.

python kontrol_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Hata: Python veya gerekli kütüphaneler bulunamadı!
    echo.
    echo Lütfen şunları kontrol edin:
    echo 1. Python yüklü mü?
    echo 2. requirements.txt dosyasındaki kütüphaneler yüklü mü?
    echo 3. kontrol_gui.py dosyası mevcut mu?
    echo.
    pause
) else (
    echo.
    echo ✅ Uygulama başarıyla kapatıldı.
)

pause 