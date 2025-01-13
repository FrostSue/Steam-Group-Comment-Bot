
# Steam Group Comment Bot

**Steam Group Comment Bot**, Steam gruplarına düzenli aralıklarla yorum göndermek için tasarlanmış bir otomasyon aracıdır. Selenium kullanarak çalışır ve belirlediğiniz gruplara belirttiğiniz zamanlama ayarlarına göre otomatik olarak yorum gönderir.

## Özellikler
- Belirlediğiniz gruplara otomatik olarak yorum gönderir.
- İlk 5 gruba günde bir kez yorum gönderir.
- Geri kalan gruplara, çalıştırıldığı andan itibaren bir saat arayla yorum gönderir.
- Kullanıcı dostu ve kolay yapılandırılabilir.

## Gereksinimler
- Python 3.8 veya üstü
- Google Chrome tarayıcısı
- ChromeDriver (Google Chrome sürümünüzle uyumlu olmalıdır)

## Kurulum

1. **Depoyu klonlayın veya indirin:**
   
   ```bash
   git clone https://github.com/kullaniciadi/steam-group-comment-bot.git
   cd steam-group-comment-bot
   ```

2. **Gerekli bağımlılıkları yükleyin:**

   ```bash
   pip install -r requirements.txt
   ```

3. **ChromeDriver'ı sisteminize ekleyin:**
   - [ChromeDriver indirme sayfasından](https://chromedriver.chromium.org/downloads) tarayıcı sürümünüze uygun olanı indirin.
   - `PATH` ortam değişkeninize ChromeDriver'ı ekleyin veya script içinde ChromeDriver'ın tam yolunu belirtin.

4. **Steam hesabınıza giriş yapın:**
   - Google Chrome'u aşağıdaki komutla başlatın:
     
     ```bash
     chrome.exe --remote-debugging-port=9222
     ```
   
   - Açılan tarayıcıdan Steam hesabınıza giriş yapın.

5. **Script'i çalıştırın:**

   ```bash
   python steam_comment_bot.py
   ```

## Kullanım

1. Script dosyasındaki `first_group_urls` ve `rest_group_urls` listelerine yorum göndermek istediğiniz grup URL'lerini ekleyin.
2. `comment_text` değişkenine gönderilecek yorum metnini yazın.
3. Script'i çalıştırarak otomasyonu başlatın.

## Yapılandırma

Zamanlama ve grup ayarlarını özelleştirmek için kodda şu bölümleri düzenleyebilirsiniz:
- **`first_group_urls`**: İlk gruplar (günde bir kez yorum yapılır).
- **`rest_group_urls`**: Diğer gruplar (1 saatlik aralıklarla yorum yapılır).
- **`comment_text`**: Gönderilecek yorum metni.

## Katkı Sağlama

Katkılarınızı memnuniyetle karşılıyoruz! Yeni özellikler eklemek veya hataları düzeltmek isterseniz, bir **pull request** göndermekten çekinmeyin.
