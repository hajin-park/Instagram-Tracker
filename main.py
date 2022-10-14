"""
Track instagram followers
Inconsistencies between followers and following
No two-factor authorization check
Only tracks followers and following
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class InstagramTracker:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get("https://www.instagram.com/")
        assert "Instagram" in self.driver.title

        self.followers_list = []
        self.following_list = []

    # Login to instagram
    def login(self, arg="default"):
        driver = self.driver
        username = str(input("\nEnter your login ID:\n"))
        password = str(input("\nEnter your password ID:\n"))

        if arg == "facebook":
            login_fb = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[5]/button')))
            login_fb.click()

            login_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'email')))
            login_pass = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'pass')))

        elif arg == "default":
            login_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username')))
            login_pass = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'password')))

        login_name.send_keys(username)
        login_pass.send_keys(password)
        login_pass.send_keys(Keys.RETURN)

        # try:
        #    verification = WebDriverWait(driver, 2).until(
        #        EC.presence_of_element_located((By.NAME, 'verificationCode')))
        #    code = int(input('Enter auth code:\n'))
        #    verification.send_keys(code)
        #    verification.send_keys(Keys.RETURN)
        # except:
        #    pass

        self.nav_to_profile()

    # Find users who don't follow and users not followed back
    def calculate_followers(self):
        for following in self.following_list.copy():
            try:
                self.followers_list.remove(following)
                self.following_list.remove(following)
            except:
                pass

        print("\n==Users that don't follow you back==")
        if self.following_list:
            for user in self.following_list:
                print(f"->{user}")
        else:
            print("[None]")

        print("\n==Users you don't follow back==")
        if self.followers_list:
            for user in self.followers_list:
                print(f"->{user}")
        else:
            print("[None]")

    # Collects following and followed users
    def search_follow_list(self, arg):
        driver = self.driver
        user_list_display = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'PZuss')))
        user_list = user_list_display.find_elements_by_tag_name('li')
        loaded_list = []

        while loaded_list != user_list:
            try:
                driver.execute_script(
                    "arguments[0].scrollIntoView();", user_list[-1])
                # increments too small will incorrectly load users
                time.sleep(0.75)
                loaded_list = user_list
            except Exception:
                loaded_list = []

            try:
                user_list = user_list_display.find_elements_by_tag_name('li')
            except Exception:
                loaded_list = []

        print(len(user_list))
        for user in user_list:
            try:
                username = user.find_element_by_class_name(
                    '_7UhW9   xLCgt        qyrsm KV-D4            se6yk       T0kll ').text
                self.followers_list.append(
                    username) if arg == "followers" else self.following_list.append(username)
            except Exception:
                user_list = user_list_display.find_elements_by_tag_name('li')

        driver.back()

    # Opens follow list
    def nav_to_follow_list(self, arg):
        driver = self.driver

        follow_display = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, arg)))
        follow_display.click()

        self.search_follow_list(arg)

    # Opens user profile
    def nav_to_profile(self):
        driver = self.driver

        profile = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span/img')))
        profile.click()

        profile = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/a[1]/div')))
        profile.click()

    # Main procedure
    def run(self):
        self.login("default")
        self.nav_to_follow_list("followers")
        self.nav_to_follow_list("following")
        print(self.followers_list)
        print(self.following_list)
        self.calculate_followers()
        self.driver.quit()


if __name__ == "__main__":
    InstagramTracker().run()
