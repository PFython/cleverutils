from .cleverutils import timer
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
    A collection of common login/scraper/collector functions for a variety of
    websites.  Each receives a (CleverSession) object as its argument, typically comprising:

    .browser : a selenium webbrowswer object that has already been initialised
    .username : typically derived from CleverSession and keyring
    .password : typically a CleverSession @property based on keyring
    """
    @staticmethod
    @timer
    def github(self, browser=None, **kwargs):
        """ Use selenium and CleverSession credentials to login to Github """
        if browser is None:
                browser = webdriver.Chrome(options=disable_logging(**kwargs))
        browser.implicitly_wait(kwargs.get("wait") or 3)
        browser.get(self.url)
        browser.find_element_by_id("login_field").send_keys(self.username)
        browser.find_element_by_id("password").send_keys(self.password)
        browser.find_element_by_name("commit").click()
        if not hasattr(self, "browsers"):
            self.browsers = []
        self.browsers += [browser]

    @staticmethod
    @timer
    def twitter(self, browser=None, **kwargs):
        """ Use selenium and CleverSession credentials to login to Github """
        if browser is None:
                browser = webdriver.Chrome(options=disable_logging(**kwargs))
        browser.implicitly_wait(kwargs.get("wait") or 3)
        browser.get(self.url)
        browser.find_element_by_name("session[username_or_email]").send_keys(self.username)
        browser.find_element_by_name("session[password]").send_keys(self.password)
        span = browser.find_elements_by_tag_name("span")
        [x for x in span if x.text=="Log in"][0].click()
        if not hasattr(self, "browsers"):
            self.browsers = []
        self.browsers += [browser]

    @staticmethod
    @timer
    def office365(self, browser=None, **kwargs):
        """ Use selenium and CleverSession credentials to login to Office365 """
        if browser is None:
                browser = webdriver.Chrome(options=disable_logging(**kwargs))
        browser.implicitly_wait(kwargs.get("wait") or 3)
        browser.get(self.url)
        browser.find_element_by_id("i0116").send_keys(self.username)
        browser.find_element_by_id("idSIButton9").click()
        browser.find_element_by_id("i0118").send_keys(self.password)
        time.sleep(2)
        browser.find_element_by_id("idSIButton9").click()
        if not hasattr(self, "browsers"):
            self.browsers = []
        self.browsers += [browser]

    @timer
    @staticmethod
    def satchelone(self, browser=None, **kwargs):
        """ Use selenium and CleverSession credentials to login to SatchelOne
        """
        if browser is None:
            browser = webdriver.Chrome(options=disable_logging(**kwargs))
        # from satchelone_config import userid, pw
        browser.implicitly_wait(kwargs.get("wait") or 3)
        browser.get(self.url)
        main_window = browser.window_handles[0]
        span = browser.find_elements_by_tag_name("span")
        [x for x in span if x.text=="Sign in with Office 365"][0].click()
        popup_window = browser.window_handles[1]
        browser.switch_to.window(popup_window)
        Login_to.office365()
        browser.switch_to.window(main_window)
        print("\n ⓘ  Waiting for SatchelOne dashboard to appear...")
        while browser.current_url != 'https://www.satchelone.com/dashboard':
            continue
        print("\n ✓  OK we're in!\n")
        if not hasattr(self, "browsers"):
            self.browsers = []
        self.browsers += [browser]
