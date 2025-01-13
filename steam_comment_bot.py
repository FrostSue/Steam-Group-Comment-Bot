from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import schedule
import random
import logging
from datetime import datetime

logging.basicConfig(
    filename='steam_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SteamGroupBot:
    def __init__(self):
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=chrome_options)
            logging.info("Chrome tarayıcı başarıyla başlatıldı.")
            print("Chrome tarayıcı başarıyla başlatıldı.")
        except Exception as e:
            logging.error(f"Tarayıcı başlatılırken hata oluştu: {str(e)}")
            print(f"Tarayıcı başlatılırken hata oluştu: {str(e)}")
            raise

    def login_check(self):
        try:
            logging.info("Steam login kontrolü yapılıyor...")
            print("Steam login kontrolü yapılıyor...")
            self.driver.get("https://steamcommunity.com")
            time.sleep(random.uniform(4, 6))

            if "login" in self.driver.current_url.lower():
                logging.warning("Login gerekiyor!")
                print("Login gerekiyor!")
                return False
            return True

        except Exception as e:
            logging.error(f"Login kontrolünde hata: {str(e)}")
            print(f"Login kontrolünde hata: {str(e)}")
            return False

    def post_comment(self, group_url, comment_text, max_retries=3):
        for attempt in range(max_retries):
            try:
                logging.info(f"\nGruba gidiliyor: {group_url}")
                print(f"\nGruba gidiliyor: {group_url}")
                self.driver.get(group_url)
                time.sleep(random.uniform(4, 6))

                logging.info("Yorum alanı aranıyor...")
                print("Yorum alanı aranıyor...")
                comment_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "textarea.commentthread_textarea")
                    )
                )
                logging.info("Yorum alanı bulundu.")
                print("Yorum alanı bulundu.")

                self.driver.execute_script("arguments[0].scrollIntoView(true);", comment_box)
                time.sleep(random.uniform(1, 2))

                actions = ActionChains(self.driver)
                actions.move_to_element(comment_box).click().perform()
                time.sleep(random.uniform(1, 2))

                comment_box.clear()
                comment_box.send_keys(comment_text)
                time.sleep(random.uniform(1, 2))

                logging.info("Post Comment butonu aranıyor...")
                print("Post Comment butonu aranıyor...")
                
                comment_area_id = comment_box.get_attribute("id")
                thread_id = comment_area_id.replace("_textarea", "")
                submit_button_id = f"{thread_id}_submit"
                
                post_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.ID, submit_button_id)
                    )
                )

                if not post_button.is_displayed():
                    raise Exception("Post butonu görünür değil")

                self.driver.execute_script("arguments[0].scrollIntoView(true);", post_button)
                time.sleep(random.uniform(1, 2))

                try:
                    post_button.click()
                except:
                    self.driver.execute_script("arguments[0].click();", post_button)

                time.sleep(3)
                
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 
                    "div.commentthread_comment.responsive_body_text")) > 0
                )
                
                logging.info(f"Yorum başarıyla gönderildi! Grup: {group_url}")
                print(f"Yorum başarıyla gönderildi! Grup: {group_url}")
                return True

            except TimeoutException as e:
                logging.error(f"Timeout hatası (Deneme {attempt + 1}/{max_retries}): {str(e)}")
                print(f"Timeout hatası (Deneme {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(random.uniform(5, 10))
                
            except Exception as e:
                logging.error(f"Yorum gönderme hatası (Deneme {attempt + 1}/{max_retries}): {str(e)}")
                print(f"Yorum gönderme hatası (Deneme {attempt + 1}/{max_retries}): {str(e)}")
                logging.error(f"Mevcut URL: {self.driver.current_url}")
                print(f"Mevcut URL: {self.driver.current_url}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(random.uniform(5, 10))

def job(bot, group_url, comment_text):
    try:
        bot.post_comment(group_url, comment_text)
    except Exception as e:
        logging.error(f"Job hatası - Grup: {group_url}, Hata: {str(e)}")
        print(f"Job hatası - Grup: {group_url}, Hata: {str(e)}")

def post_to_first_groups(bot, first_group_urls, comment_text):
    """İlk gruplara post atma işlemi"""
    for group_url in first_group_urls:
        try:
            job(bot, group_url, comment_text)
            time.sleep(random.uniform(30, 60))
        except Exception as e:
            logging.error(f"İlk grup post hatası - Grup: {group_url}, Hata: {str(e)}")
            print(f"İlk grup post hatası - Grup: {group_url}, Hata: {str(e)}")

def post_to_rest_groups(bot, rest_group_urls, comment_text):
    """Diğer gruplara post atma işlemi"""
    for group_url in rest_group_urls:
        try:
            job(bot, group_url, comment_text)
            time.sleep(random.uniform(30, 60))
        except Exception as e:
            logging.error(f"Diğer gruplar post hatası - Grup: {group_url}, Hata: {str(e)}")
            print(f"Diğer gruplar post hatası - Grup: {group_url}, Hata: {str(e)}")

def schedule_tasks(bot, first_group_urls, rest_group_urls, comment_text):
    try:
        logging.info("İlk gruplara post atılıyor...")
        print("İlk gruplara post atılıyor...")
        
        post_to_first_groups(bot, first_group_urls, comment_text)
        
        current_time = datetime.now()
        schedule_time = f"{current_time.hour:02d}:{current_time.minute:02d}"
        schedule.every().day.at(schedule_time).do(post_to_first_groups, bot, first_group_urls, comment_text)
        
        logging.info("Diğer gruplara post atılıyor...")
        print("Diğer gruplara post atılıyor...")
        post_to_rest_groups(bot, rest_group_urls, comment_text)
        
        schedule.every(1).hours.do(post_to_rest_groups, bot, rest_group_urls, comment_text)

        logging.info("Tüm zamanlamalar başarıyla ayarlandı.")
        print("Tüm zamanlamalar başarıyla ayarlandı.")

    except Exception as e:
        logging.error(f"Schedule tasks genel hata: {str(e)}")
        print(f"Schedule tasks genel hata: {str(e)}")

def main():
    try:
        logging.info("Bot başlatılıyor...")
        print("Bot başlatılıyor...")
        bot = SteamGroupBot()

        if not bot.login_check():
            logging.error("Steam'e giriş yapılmamış! Lütfen Chrome'da Steam hesabınıza giriş yapın.")
            print("Steam'e giriş yapılmamış! Lütfen Chrome'da Steam hesabınıza giriş yapın.")
            return

        first_group_urls = [
            "https://steamcommunity.com/groups/group1",
            "https://steamcommunity.com/groups/group2",
            "https://steamcommunity.com/groups/group3",
            "https://steamcommunity.com/groups/group4",
            "https://steamcommunity.com/groups/group5",
        ]

        rest_group_urls = [
            "https://steamcommunity.com/groups/group6",
            "https://steamcommunity.com/groups/group7",
            "https://steamcommunity.com/groups/group8",
            "https://steamcommunity.com/groups/group9",
            "https://steamcommunity.com/groups/group10",
        ]

        comment_text = "Atılacak olan yorumunuzu buraya yazın"

        schedule_tasks(bot, first_group_urls, rest_group_urls, comment_text)
        logging.info("Zamanlama ayarlandı. Bot, belirlenen programlara göre çalışacak.")
        print("Zamanlama ayarlandı. Bot, belirlenen programlara göre çalışacak.")

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        logging.error(f"Ana programda hata: {str(e)}")
        print(f"Ana programda hata: {str(e)}")

if __name__ == "__main__":
    main()
