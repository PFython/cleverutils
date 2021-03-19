from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

def disable_logging(**kwargs):
    """ Experimental: run selenium in silent mode """
    options = webdriver.ChromeOptions()
    options.headless = kwargs.get("headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return options

class Login_to:
    """
    A collection of common login functions for a variety of websites.
    Each receives a (CleverSession) object (self) as its argument, typically
    comprising:

    .browser : a selenium webbrowswer object that has already been initialised
    .username : typically derived from CleverSession and keyring
    .password : typically a CleverSession @property based on keyring
    .login_url : URL to provide login credentials to

    the .add_current_browser() method appends the current (login) browser to
    self.browsers list.
    """


    @staticmethod
    def tplink(self, **kwargs):
        """
        Use selenium and CleverSession credentials to login to tplink modem
        """
        self.login_url = r"http://192.168.0.1/login.html"
        self.browser.get(self.login_url)
        self.browser.find_element_by_id("password").send_keys(self.password)
        self.browser.find_element_by_id("loginBtn").click()
        self.add_current_browser()

    @staticmethod
    def hackerrank(self, **kwargs):
        """ Use selenium and CleverSession credentials to login to HackerRank """
        self.login_url = r"https://www.hackerrank.com/auth/login?h_l=body_middle_left_button&h_r=login"
        self.browser.get(self.login_url)
        self.browser.find_element_by_id("input-1").send_keys(self.username)
        self.browser.find_element_by_id("input-2").send_keys(self.password)
        self.browser.find_element_by_xpath('//*[@id="tab-1-content-1"]/div[1]/form/div[4]/button').click()
        self.add_current_browser()


    @staticmethod
    def github(self, **kwargs):
        """ Use selenium and CleverSession credentials to login to Github """
        self.browser.get(self.login_url)
        self.browser.find_element_by_id("login_field").send_keys(self.username)
        self.browser.find_element_by_id("password").send_keys(self.password)
        self.browser.find_element_by_name("commit").click()
        self.add_current_browser()

    @staticmethod
    def twitter(self, **kwargs):
        """ Use selenium and CleverSession credentials to login to Github """
        self.browser.get(self.login_url)
        self.browser.find_element_by_name("session[username_or_email]").send_keys(self.username)
        self.browser.find_element_by_name("session[password]").send_keys(self.password)
        span = self.browser.find_elements_by_tag_name("span")
        [x for x in span if x.text=="Log in"][0].click()
        self.add_current_browser()

    @staticmethod
    def office365(self, **kwargs):
        """ Use selenium and CleverSession credentials to login to Office365 """
        self.browser.get(self.login_url)
        self.browser.find_element_by_id("i0116").send_keys(self.username)
        self.browser.find_element_by_id("idSIButton9").click()
        self.browser.find_element_by_id("i0118").send_keys(self.password)
        time.sleep(2)
        self.browser.find_element_by_id("idSIButton9").click()
        self.add_current_browser()


    @staticmethod
    def satchelone(self, **kwargs):
        """ Use selenium and CleverSession credentials to login to SatchelOne
        """
        # from satchelone_config import userid, pw
        self.browser.get(self.login_url)
        main_window = self.browser.window_handles[0]
        span = self.browser.find_elements_by_tag_name("span")
        [x for x in span if x.text=="Sign in with Office 365"][0].click()
        popup_window = self.browser.window_handles[1]
        self.browser.switch_to.window(popup_window)
        Login_to.office365()
        self.browser.switch_to.window(main_window)
        print("\n ⓘ  Waiting for SatchelOne dashboard to appear...")
        while self.browser.current_url != 'https://www.satchelone.com/dashboard':
            continue
        print("\n ✓  OK we're in!\n")
        self.add_current_browser()

class Scrape:
    """
    A collection of common scraper/collector functions for a variety of
    websites.  Each receives a (CleverSession) object (self) as its argument, typically comprising:

    .browser : a selenium webbrowswer object that has already been initialised
    """

    @staticmethod
    def tplink(self, **kwargs):
        return
