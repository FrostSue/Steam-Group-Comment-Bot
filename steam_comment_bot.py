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
import socket
import urllib.request
import contextlib
import configparser
from translation import get_translation

logging.basicConfig(
    filename='steam_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LanguageSelector:
    @staticmethod
    def select_language():
        while True:
            try:
                choice = input(get_translation("tr", "select_language"))
                if choice == "1":
                    return "tr"
                elif choice == "2":
                    return "en"
                else:
                    print(get_translation("tr", "invalid_choice"))
            except ValueError:
                print(get_translation("tr", "invalid_choice"))

def load_group_urls(language):
    try:
        config = configparser.ConfigParser()
        config.read('group-url.ini')
        
        first_groups = [url for key, url in config['first_groups'].items()]
        rest_groups = [url for key, url in config['rest_groups'].items()]
        
        return first_groups, rest_groups
    except Exception as e:
        error_msg = get_translation(language, "config_error", str(e))
        logging.error(error_msg)
        print(error_msg)
        raise

def check_internet_connection():
    try:
        with contextlib.closing(socket.create_connection(("8.8.8.8", 53), timeout=3)):
            return True
    except:
        return False

def wait_for_internet(language):
    if not check_internet_connection():
        logging.warning(get_translation(language, "no_internet"))
        print(get_translation(language, "no_internet"))
        while not check_internet_connection():
            time.sleep(5)
        logging.info(get_translation(language, "internet_restored"))
        print(get_translation(language, "internet_restored"))

class SteamGroupBot:
    def __init__(self, language):
        self.driver = None
        self.language = language
        self.setup_driver()
        self.last_connection_check = 0
        self.connection_check_interval = 60

    def setup_driver(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=chrome_options)
            logging.info(get_translation(self.language, "browser_start"))
            print(get_translation(self.language, "browser_start"))
        except Exception as e:
            error_msg = get_translation(self.language, "browser_error", str(e))
            logging.error(error_msg)
            print(error_msg)
            raise

    def check_connection_if_needed(self):
        current_time = time.time()
        if current_time - self.last_connection_check >= self.connection_check_interval:
            wait_for_internet(self.language)
            self.last_connection_check = current_time

    def login_check(self):
        try:
            logging.info(get_translation(self.language, "login_check"))
            print(get_translation(self.language, "login_check"))
            self.check_connection_if_needed()
            
            self.driver.get("https://steamcommunity.com")
            time.sleep(random.uniform(4, 6))

            if "login" in self.driver.current_url.lower():
                logging.warning(get_translation(self.language, "login_required"))
                print(get_translation(self.language, "login_required"))
                return False
            return True

        except Exception as e:
            error_msg = get_translation(self.language, "login_error", str(e))
            logging.error(error_msg)
            print(error_msg)
            return False

    def post_comment(self, group_url, comment_text, max_retries=3):
        for attempt in range(max_retries):
            try:
                self.check_connection_if_needed()
                
                logging.info(get_translation(self.language, "going_to_group", group_url))
                print(get_translation(self.language, "going_to_group", group_url))
                self.driver.get(group_url)
                time.sleep(random.uniform(4, 6))

                logging.info(get_translation(self.language, "searching_comment"))
                print(get_translation(self.language, "searching_comment"))
                comment_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "textarea.commentthread_textarea")
                    )
                )
                logging.info(get_translation(self.language, "comment_found"))
                print(get_translation(self.language, "comment_found"))

                self.driver.execute_script("arguments[0].scrollIntoView(true);", comment_box)
                time.sleep(random.uniform(1, 2))

                actions = ActionChains(self.driver)
                actions.move_to_element(comment_box).click().perform()
                time.sleep(random.uniform(1, 2))

                comment_box.clear()
                comment_box.send_keys(comment_text)
                time.sleep(random.uniform(1, 2))

                comment_area_id = comment_box.get_attribute("id")
                thread_id = comment_area_id.replace("_textarea", "")
                submit_button_id = f"{thread_id}_submit"
                
                post_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.ID, submit_button_id)
                    )
                )

                if not post_button.is_displayed():
                    raise Exception("Post button is not visible.")

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
                
                logging.info(get_translation(self.language, "comment_success", group_url))
                print(get_translation(self.language, "comment_success", group_url))
                return True

            except Exception as e:
                error_msg = get_translation(self.language, "comment_error", attempt + 1, max_retries, str(e))
                logging.error(error_msg)
                print(error_msg)
                
                if attempt == max_retries - 1:
                    self.check_connection_if_needed()
                    raise
                    
                time.sleep(random.uniform(5, 10))

def job(bot, group_url, comment_text):
    try:
        bot.post_comment(group_url, comment_text)
    except Exception as e:
        error_msg = get_translation(bot.language, "task_error", group_url, str(e))
        logging.error(error_msg)
        print(error_msg)

def post_to_first_groups(bot, first_group_urls, comment_text):
    for group_url in first_group_urls:
        try:
            job(bot, group_url, comment_text)
            time.sleep(random.uniform(30, 60))
        except Exception as e:
            error_msg = get_translation(bot.language, "first_group_error", group_url, str(e))
            logging.error(error_msg)
            print(error_msg)

def post_to_rest_groups(bot, rest_group_urls, comment_text):
    for group_url in rest_group_urls:
        try:
            job(bot, group_url, comment_text)
            time.sleep(random.uniform(30, 60))
        except Exception as e:
            error_msg = get_translation(bot.language, "other_groups_error", group_url, str(e))
            logging.error(error_msg)
            print(error_msg)

def schedule_tasks(bot, first_group_urls, rest_group_urls, comment_text):
    try:
        logging.info(get_translation(bot.language, "first_groups_posting"))
        print(get_translation(bot.language, "first_groups_posting"))
        
        post_to_first_groups(bot, first_group_urls, comment_text)
        
        current_time = datetime.now()
        schedule_time = f"{current_time.hour:02d}:{current_time.minute:02d}"
        schedule.every().day.at(schedule_time).do(post_to_first_groups, bot, first_group_urls, comment_text)
        
        logging.info(get_translation(bot.language, "rest_groups_posting"))
        print(get_translation(bot.language, "rest_groups_posting"))
        post_to_rest_groups(bot, rest_group_urls, comment_text)
        
        schedule.every(1).hours.do(post_to_rest_groups, bot, rest_group_urls, comment_text)

        logging.info(get_translation(bot.language, "schedule_success"))
        print(get_translation(bot.language, "schedule_success"))

    except Exception as e:
        error_msg = get_translation(bot.language, "schedule_error", str(e))
        logging.error(error_msg)
        print(error_msg)

def main():
    language = LanguageSelector.select_language()
    
    while True:
        try:
            logging.info(get_translation(language, "bot_starting"))
            print(get_translation(language, "bot_starting"))
            
            wait_for_internet(language)
            bot = SteamGroupBot(language)

            if not bot.login_check():
                logging.error(get_translation(language, "no_login"))
                print(get_translation(language, "no_login"))
                return

            first_groups, rest_groups = load_group_urls(language)

            comment_text = "YOUR COMMENT HERE!"

            schedule_tasks(bot, first_groups, rest_groups, comment_text)
            logging.info(get_translation(language, "schedule_set"))
            print(get_translation(language, "schedule_set"))

            while True:
                schedule.run_pending()
                time.sleep(1)

        except Exception as e:
            error_msg = get_translation(language, "main_error", str(e))
            logging.error(error_msg)
            print(error_msg)
            print(get_translation(language, "restarting"))
            time.sleep(5)

if __name__ == "__main__":
    main()
