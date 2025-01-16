translations = {
    "tr": {
        "select_language": "Lütfen bir dil seçin/Please select a language:\n1. Türkçe\n2. English\nSeçiminiz/Your choice (1-2): ",
        "invalid_choice": "Geçersiz seçim! Lütfen tekrar deneyin.",
        "browser_start": "Chrome tarayıcı başarıyla başlatıldı.",
        "browser_error": "Tarayıcı başlatılırken hata oluştu: {}",
        "login_check": "Steam login kontrolü yapılıyor...",
        "login_required": "Login gerekiyor!",
        "login_error": "Login kontrolünde hata: {}",
        "going_to_group": "\nGruba gidiliyor: {}",
        "searching_comment": "Yorum alanı aranıyor...",
        "comment_found": "Yorum alanı bulundu.",
        "comment_success": "Yorum başarıyla gönderildi! Grup: {}",
        "comment_error": "Yorum gönderme hatası (Deneme {}/{}): {}",
        "task_error": "Görev hatası - Grup: {}, Hata: {}",
        "first_groups_posting": "İlk gruplara post atılıyor...",
        "rest_groups_posting": "Diğer gruplara post atılıyor...",
        "schedule_success": "Tüm zamanlamalar başarıyla ayarlandı.",
        "schedule_error": "Zamanlama görevleri genel hata: {}",
        "bot_starting": "Bot başlatılıyor...",
        "no_login": "Steam'e giriş yapılmamış! Lütfen Chrome'da Steam hesabınıza giriş yapın.",
        "schedule_set": "Zamanlama ayarlandı. Bot, belirlenen programlara göre çalışacak.",
        "main_error": "Ana programda hata: {}",
        "restarting": "Program yeniden başlatılıyor...",
        "no_internet": "İnternet bağlantısı yok. Yeniden bağlanmayı bekliyorum...",
        "internet_restored": "İnternet bağlantısı tekrar sağlandı!",
        "first_group_error": "İlk grup post hatası - Grup: {}, Hata: {}",
        "other_groups_error": "Diğer gruplar post hatası - Grup: {}, Hata: {}",
        "config_error": "Grup URL'leri dosyası okunamadı: {}"
    },
    "en": {
        "select_language": "Please select a language:\n1. Türkçe\n2. English\nYour choice (1-2): ",
        "invalid_choice": "Invalid choice! Please try again.",
        "browser_start": "Chrome browser started successfully.",
        "browser_error": "Error occurred while starting browser: {}",
        "login_check": "Checking Steam login...",
        "login_required": "Login required!",
        "login_error": "Login check error: {}",
        "going_to_group": "\nGoing to group: {}",
        "searching_comment": "Searching for comment area...",
        "comment_found": "Comment area found.",
        "comment_success": "Comment successfully posted! Group: {}",
        "comment_error": "Comment posting error (Attempt {}/{}): {}",
        "task_error": "Task error - Group: {}, Error: {}",
        "first_groups_posting": "Posting to first groups...",
        "rest_groups_posting": "Posting to rest groups...",
        "schedule_success": "All schedules set successfully.",
        "schedule_error": "Schedule tasks general error: {}",
        "bot_starting": "Starting bot...",
        "no_login": "Not logged into Steam! Please log into your Steam account in Chrome.",
        "schedule_set": "Schedule set. Bot will run according to the defined programs.",
        "main_error": "Error in main program: {}",
        "restarting": "Restarting program...",
        "no_internet": "No internet connection. Waiting for reconnection...",
        "internet_restored": "Internet connection restored!",
        "first_group_error": "First group posting error - Group: {}, Error: {}",
        "other_groups_error": "Other groups posting error - Group: {}, Error: {}",
        "config_error": "Could not read group URLs file: {}"
    }
}

def get_translation(lang, key, *args):
    try:
        text = translations[lang][key]
        if args:
            return text.format(*args)
        return text
    except KeyError:
        return f"Missing translation: {key}"
