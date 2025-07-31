@echo off
chcp 1254 >nul
cls
@echo off
chcp 1254 >nul
cls

set SITE=http://webmail.ilbank.gov.tr

echo       WEBMAIL HTTP ER���M TEST�
echo       Tarih: %DATE%   Saat: %TIME%

echo.

echo [1] Web sunucusuna eri�im deneniyor: %SITE%
curl --silent --head --fail %SITE% >nul

if %errorlevel%==0 (
    echo     [OK] Webmail sitesi AKT�F ve HTTP yan�t veriyor.
) else (
    echo     [HATA] Webmail sitesi PAS�F veya eri�ilemiyor.
)

echo.

pause
