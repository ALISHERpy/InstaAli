from selenium import webdriver
from selenium.common import WebDriverException
import random
import os
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from data import account_list

class InstagramBot():
    """Instagram Bot From AlisherPY"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run in headless mode
        # self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)

    def close_driver(self):
        self.driver.quit()

    def login(self):

        driver = self.driver
        driver.get('https://www.instagram.com/')
        driver.maximize_window()
        wait = WebDriverWait(self.driver, 10)
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

        email_field.send_keys(self.username)
        password_field.send_keys(self.password)

        password_field.send_keys(Keys.RETURN)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                "x1n2onr6")))

        time.sleep(5)

    def generate_random_comment(self):
        # Select five random words from the list
        random_words = random.sample(account_list, 5)
        commented_words = ['@' + word for word in random_words]
        # Join the words to form the comment
        comment_text = '  |  '.join(commented_words)
        return comment_text + "  "

    def comment_to_posts(self, links, delay_time=2, accounts_for_comment=None):
        """Comment uchun account bering"""

        for link in links:
            if accounts_for_comment is None:
                accounts_for_comment = self.generate_random_comment()
            comment = accounts_for_comment
            # Open each post link
            driver = self.driver
            driver.get(link)
            # time.sleep(2)

            # Find the comment input field
            comment_input = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'textarea[aria-label="Add a comment…"]'))).click()

            # Create an instance of ActionChains
            actions = ActionChains(driver)
            actions.send_keys(comment)
            actions.send_keys(Keys.ENTER)
            # Perform the actions
            actions.perform()

            time.sleep(delay_time)

    def like_to_post(self, links_to_posts):

        """Post link bering,unga like bosadi"""
        driver = self.driver
        # Wait for the new page to fully load
        WebDriverWait(driver, 10)

        for link_to_post in links_to_posts:
            try:
                driver.get(link_to_post)
                # time.sleep(4)

                # Wait until the like button is clickable
                like_element=WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'xp7jhwk'))
                )
                svg_icon = like_element.find_element(By.TAG_NAME, "svg")
                aria_label = svg_icon.get_attribute("aria-label")

                if aria_label == "Like":
                    # print("This is a like button.")
                    like_element.click()
                elif aria_label == "Unlike":
                    # print("This is an unlike button.")
                    pass


            except Exception as e:
                pass
                # print(f"Error: {e}")


    def to_follow(self, link_to_account: str):
        """BU functionga bron bir accaunt link yuborasiz !
        va ushangga follow bosadi"""

        driver = self.driver
        # Wait for the new page to fully load
        WebDriverWait(driver, 10)

        try:

            driver.get(link_to_account)

            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow')]"))
            ).click()

        except Exception as e:
            pass

    def following_taker(self, account_link: str):
        driver = self.driver
        file_name = account_link.split("/")[-2]
        driver.get(account_link)
        time.sleep(3)  # Reduced sleep
        number_ofFollowing = 143  # Initialize number_ofFollowing variable

        elements = driver.find_elements(By.CLASS_NAME, "x1lliihq")
        for element in elements:
            text_content = element.text
            if "following" in text_content:
                number_ofFollowing = ''.join(filter(str.isdigit, text_content))
                # print(number_ofFollowing)

        # Check if number_ofFollowing has been assigned a value
        if number_ofFollowing is not None:
            file_name = f"{file_name}_{number_ofFollowing}followings.txt"
            file_path = os.path.join('following', file_name)

            if not os.path.exists(file_path):
                driver.get(account_link + "following/")
                time.sleep(4)  # Reduced sleep
                try:
                    following_urls = []

                    element = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "_aano")))
                    prev_height = driver.execute_script("return arguments[0].scrollHeight", element)
                    while True:
                        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
                        time.sleep(3)
                        new_height = driver.execute_script("return arguments[0].scrollHeight", element)
                        if new_height == prev_height:
                            break
                        prev_height = new_height

                    all_urls_div = element.find_elements(By.TAG_NAME, "a")
                    for url in all_urls_div:
                        url = url.get_attribute("href")
                        following_urls.append(url)

                    following_urls = list(set(following_urls))

                    if not os.path.exists('following'):
                        os.makedirs('following')

                    with open(os.path.join('following', file_name), "w") as text_file:
                        for link in following_urls:
                            text_file.write(link + "\n")

                    return following_urls

                except Exception as e:
                    print("Following page error:", e)
                    return 0

            else:
                print(f"File '{file_name}' already exists. Skipping writing.")
                with open(file_path, "r") as text_file:
                    following_urls = [line.strip() for line in text_file.read().splitlines() if line.strip()]
                return following_urls
        else:
            print("No 'following' text found.")
            return 0


        #########
    def bruteforce_follow(self, link_to_account: str):
        """BU functionga bron bir accaunt link yuborasiz !
        va u follow bosganlariga follow bosadi"""
        driver = self.driver

        following_links = self.following_taker(account_link=link_to_account)

        if following_links:
            for link in following_links:
                try:
                    driver.get(link)
                    # Wait until the specific button is clickable
                    follow_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow')]"))
                    )
                    follow_button.click()
                    # time.sleep(2)  # Adjust sleep time as needed
                except WebDriverException as ex:
                    print(f"WebDriverException occurred: {ex}")
                    print("Reloading the page...")
                    driver.refresh()
                    # Wait until the specific button is clickable after reload
                    try:
                        follow_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow')]"))
                        )
                        follow_button.click()
                        # time.sleep(2)  # Adjust sleep time as needed
                    except Exception as e:
                        print(f"Error clicking on the button after page reload: {e}")

        self.close_driver()

    def like_story(self, usernames):
        driver = self.driver


        for username in usernames:
            print(username)
            time.sleep(3)
            driver.get(f"https://www.instagram.com/stories/{username}/")
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[text()="View story"]'))).click()
            time.sleep(1)
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@aria-label="Like"]'))).click()
            # driver.find_element(By.XPATH,"//a[@title='Like']").click()
            # follow_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow')]"))
            # )
            driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/section/div[1]/div/div[5]/section/div/div[3]/div/div/div[2]/div[1]/span/div/div").click()


        time.sleep(111)