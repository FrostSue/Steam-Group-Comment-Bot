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

logging.basicConfig(
    filename='steam_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_internet_connection():
    """Function to check internet connection"""
    try:
        with contextlib.closing(socket.create_connection(("8.8.8.8", 53), timeout=3)):
            return True
    except:
        return False

def wait_for_internet():
    """Wait until internet connection is restored"""
    if not check_internet_connection():
        logging.warning("No internet connection. Waiting for reconnection...")
        print("No internet connection. Waiting for reconnection...")
        while not check_internet_connection():
            time.sleep(5)
        logging.info("Internet connection restored!")
        print("Internet connection restored!")

class SteamGroupBot:
    def __init__(self):
        self.driver = None
        self.setup_driver()
        self.last_connection_check = 0
        self.connection_check_interval = 60

    def setup_driver(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=chrome_options)
            logging.info("Chrome browser started successfully.")
            print("Chrome browser started successfully.")
        except Exception as e:
            logging.error(f"Error starting browser: {str(e)}")
            print(f"Error starting browser: {str(e)}")
            raise

    def check_connection_if_needed(self):
        """Check connection only if enough time has passed since last check"""
        current_time = time.time()
        if current_time - self.last_connection_check >= self.connection_check_interval:
            wait_for_internet()
            self.last_connection_check = current_time

    def login_check(self):
        try:
            logging.info("Checking Steam login...")
            print("Checking Steam login...")
            self.check_connection_if_needed()
            
            self.driver.get("https://steamcommunity.com")
            time.sleep(random.uniform(4, 6))

            if "login" in self.driver.current_url.lower():
                logging.warning("Login required!")
                print("Login required!")
                return False
            return True

        except Exception as e:
            logging.error(f"Login check error: {str(e)}")
            print(f"Login check error: {str(e)}")
            return False

    def post_comment(self, group_url, comment_text, max_retries=3):
        for attempt in range(max_retries):
            try:
                self.check_connection_if_needed()
                
                logging.info(f"\nNavigating to group: {group_url}")
                print(f"\nNavigating to group: {group_url}")
                self.driver.get(group_url)
                time.sleep(random.uniform(4, 6))

                logging.info("Searching for comment area...")
                print("Searching for comment area...")
                comment_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "textarea.commentthread_textarea")
                    )
                )
                logging.info("Comment area found.")
                print("Comment area found.")

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
                    raise Exception("Post button not visible")

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
                
                logging.info(f"Comment successfully posted! Group: {group_url}")
                print(f"Comment successfully posted! Group: {group_url}")
                return True

            except Exception as e:
                logging.error(f"Comment posting error (Attempt {attempt + 1}/{max_retries}): {str(e)}")
                print(f"Comment posting error (Attempt {attempt + 1}/{max_retries}): {str(e)}")
                
                if attempt == max_retries - 1:
                    self.check_connection_if_needed()
                    raise
                    
                time.sleep(random.uniform(5, 10))

def job(bot, group_url, comment_text):
    try:
        bot.post_comment(group_url, comment_text)
    except Exception as e:
        logging.error(f"Job error - Group: {group_url}, Error: {str(e)}")
        print(f"Job error - Group: {group_url}, Error: {str(e)}")

def post_to_first_groups(bot, first_group_urls, comment_text):
    """Post to first groups"""
    for group_url in first_group_urls:
        try:
            job(bot, group_url, comment_text)
            time.sleep(random.uniform(30, 60))
        except Exception as e:
            logging.error(f"First group posting error - Group: {group_url}, Error: {str(e)}")
            print(f"First group posting error - Group: {group_url}, Error: {str(e)}")

def post_to_rest_groups(bot, rest_group_urls, comment_text):
    """Post to remaining groups"""
    for group_url in rest_group_urls:
        try:
            job(bot, group_url, comment_text)
            time.sleep(random.uniform(30, 60))
        except Exception as e:
            logging.error(f"Other groups posting error - Group: {group_url}, Error: {str(e)}")
            print(f"Other groups posting error - Group: {group_url}, Error: {str(e)}")

def schedule_tasks(bot, first_group_urls, rest_group_urls, comment_text):
    try:
        logging.info("Posting to first groups...")
        print("Posting to first groups...")
        
        post_to_first_groups(bot, first_group_urls, comment_text)
        
        current_time = datetime.now()
        schedule_time = f"{current_time.hour:02d}:{current_time.minute:02d}"
        schedule.every().day.at(schedule_time).do(post_to_first_groups, bot, first_group_urls, comment_text)
        
        logging.info("Posting to other groups...")
        print("Posting to other groups...")
        post_to_rest_groups(bot, rest_group_urls, comment_text)
        
        schedule.every(1).hours.do(post_to_rest_groups, bot, rest_group_urls, comment_text)

        logging.info("All schedules successfully set.")
        print("All schedules successfully set.")

    except Exception as e:
        logging.error(f"Schedule tasks general error: {str(e)}")
        print(f"Schedule tasks general error: {str(e)}")

def main():
    while True:
        try:
            logging.info("Starting bot...")
            print("Starting bot...")
            
            wait_for_internet()  
            bot = SteamGroupBot()

            if not bot.login_check():
                logging.error("Not logged into Steam! Please log into your Steam account in Chrome.")
                print("Not logged into Steam! Please log into your Steam account in Chrome.")
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

            comment_text = "Your comment text here!"

            schedule_tasks(bot, first_group_urls, rest_group_urls, comment_text)
            logging.info("Scheduling set. Bot will run according to defined schedules.")
            print("Scheduling set. Bot will run according to defined schedules.")

            while True:
                schedule.run_pending()
                time.sleep(1)

        except Exception as e:
            logging.error(f"Error in main program: {str(e)}")
            print(f"Error in main program: {str(e)}")
            print("Restarting program...")
            time.sleep(5)

if __name__ == "__main__":
    main()
