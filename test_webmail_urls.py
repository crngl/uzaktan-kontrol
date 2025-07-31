import requests
import time
from datetime import datetime

def test_url(url, timeout=10):
    """URL'yi test et ve yanıt süresini ölç"""
    start_time = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"✅ {url}")
        print(f"   HTTP Kodu: {response.status_code}")
        print(f"   Yanıt Süresi: {response_time:.2f} saniye")
        print(f"   Başlık: {response.headers.get('Server', 'Bilinmiyor')}")
        return True, response_time
        
    except requests.exceptions.Timeout:
        print(f"❌ {url} - Zaman aşımı ({timeout}s)")
        return False, timeout
    except requests.exceptions.ConnectionError:
        print(f"❌ {url} - Bağlantı hatası")
        return False, 0
    except Exception as e:
        print(f"❌ {url} - Hata: {e}")
        return False, 0

def main():
    print("🌐 Webmail URL Testi")
    print("=" * 50)
    print(f"Test Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test edilecek URL'ler
    urls = [
        "http://webmail.ilbank.gov.tr",
        "https://webmail.ilbank.gov.tr",
        "http://mail.ilbank.gov.tr",
        "https://mail.ilbank.gov.tr",
        "http://webmail.ilbank.com.tr",
        "https://webmail.ilbank.com.tr"
    ]
    
    successful_urls = []
    
    for url in urls:
        success, response_time = test_url(url, timeout=15)
        if success:
            successful_urls.append((url, response_time))
        print()
    
    print("=" * 50)
    print("📊 Test Sonuçları:")
    print(f"Toplam URL: {len(urls)}")
    print(f"Başarılı: {len(successful_urls)}")
    print(f"Başarısız: {len(urls) - len(successful_urls)}")
    
    if successful_urls:
        print("\n🏆 En Hızlı URL'ler:")
        successful_urls.sort(key=lambda x: x[1])  # Yanıt süresine göre sırala
        for i, (url, response_time) in enumerate(successful_urls[:3], 1):
            print(f"{i}. {url} ({response_time:.2f}s)")
    else:
        print("\n❌ Hiçbir URL erişilebilir değil!")
        print("Lütfen internet bağlantınızı kontrol edin.")

if __name__ == "__main__":
    main() 