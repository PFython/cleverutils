"""
A collection of commonly used functions, classes, and methods based on the CleverDict data class and tailored to the author's current level and style of Python coding.
"""

from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import webbrowser
import PySimpleGUI as sg
from pathlib import Path
from cleverdict import CleverDict
import pyperclip
import inspect
import json
import keyring

def timer(func):
    """
    Wrapper to start the clock, runs func(), then stop the clock. Simples.
    Designed to work as a decorator... just put @timer in the line above the
    original function.
    """
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        data = func(*args, **kwargs)
        print(f"\n ⏱  Function {func.__name__!r} took {round(time.perf_counter()-start,2)} seconds to complete.\n")
        return (data)
    return wrapper

class CleverSession(CleverDict):
    """
    Alternative to using global variable to pass around session data.
    Subclass of CleverDict for easy data handling and auto-save features.
    """
    index = CleverDict()
    choices = {"https://github.com/login": "Github",
               "https://twitter.com": "Twitter",
               "https://www.satchelone.com/login": "SatchelOne"}
    sg_options = {"title": "CleverSession", "keep_on_top": True}  # PySimpleGUI options
    keyring_config_root = keyring.util.platform_.config_root()
    keyring_data_root = keyring.util.platform_.data_root()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sg_options = CleverSession.sg_options
        self.start_gui()
        self.check_and_prompt("url")
        if self.get("url"):
            self.account = CleverSession.choices[self.url]
            self.get_username()
        if not self.get("dirpath"):
            self.dirpath = Path().cwd()

    def get_username(self):
        """
        Loads (last modified) username from keyring. May not work on iOS.
        """
        try:
            self.username = keyring.get_credential(self.account, None).username
        except:
            print("\n  ⚠ .get_username() only supported on Windows OS.")
            print("\n     Trying creating .username manually first.")

    def check_and_prompt(self, *args):
        """
        Checks for existence/non-False value of an argument, and if required
        calls the specified method to prompt for a value.  Different methods
        may be needed for different input types e.g. file, folder, checkboxes, database read, REST API call, or regular input().

        args : attributes (as strings) to look for; try to use logical order.
        """
        buttons = {"url": "Please enter a link (URL) to the target website:",}
        text = {"username": "Please enter a username/login ID{}:",
                "password": "Please enter a password{}:"}
        choices = CleverSession.choices
        for attribute in args:
            prompt = buttons.get(attribute) or text.get(attribute) or f"Please enter a value for .{attribute} :"
            prompt = prompt.replace("{}", f" for your {self.account} account" if self.get("account") else "")
            if attribute == "password":
                self.check_and_prompt("url", "username")
                if not keyring.get_password(choices[self.url], self.username):
                    self.set_password(text_input(prompt))
            elif not self.get(attribute):
                if attribute in buttons:
                    value = button_menu(choices)
                else:  # Includes attributes in neither buttons nor text
                    value = text_input(prompt)
                if value:
                    self[attribute] = value

    @property
    def password(self):
        """ Retrieve password from keyring """
        return keyring.get_password(CleverSession.choices[self.url], self.username)

    def set_password(self, value):
        """ Set password in keyring """
        if value:
            keyring.set_password(CleverSession.choices[self.url], self.username, value)

    def delete_password(self):
        """ Delete password from keyring """
        keyring.delete_password(CleverSession.choices[self.url], self.username)

    def login_with_webbrowser(self):
        self.check_and_prompt("url", "username", "password")
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.browser.get(self.url)
        dispatch = {"github.com": login_to_github,
                    "twitter.com": login_to_twitter,
                    "satchelone.com": login_to_satchelone}
        for website, func in dispatch.items():
            if website in self.url:
                func()
                break

    def start_gui(self, **kwargs):
        """
        Toggles between normal output and routing stdout/stderr to PySimpleGUI

        redirect: send (almost) all stdout/stderr to Debug Window & replace print()
        """
        if kwargs.get("redirect"):
            global print
            self.old_print = print
            print = sg.Print
            options = {"do_not_reroute_stdout": False, "keep_on_top": True}
            print(**options)
            print("Rerouting stdout/stderr to PySimpleGUI Debug Window...")
        sg.change_look_and_feel("DarkAmber")
        # Redirect stdout and stderr to Debug Window:
        sg.set_options(
            message_box_line_width=80,
            debug_win_size=(100, 30),
            icon = "cleverdict.ico",
            font = "calibri 12",
        )

    def save(self, name, value):
        """ Generic auto-save confirmation applied CleverDict """
        if "password" not in str(name).lower():
            print(f" ⓘ  {name} = {value} {type(value)}")

    def start(self):
        """ Shortcut/Alias for starting a webbrowser session and logging in """
        self.login_with_webbrowser()

def to_json(self, never_save = False, **kwargs):
    """
    Return CleverDict serialised to JSON.

    KWARGS
    never_save: Exclude field in CleverDict.never_save if True eg passwords
    file: Save to file if True or filepath

    """
    # .get_aliases finds attributes created after __init__:
    fields_dict = {key: self.get(key) for key in self.get_aliases()}
    if never_save:
        fields_dict = {k:v for k,v in fields_dict if k not in never_save}
    json_str = json.dumps(fields_dict, indent=4)
    path = kwargs.get("file")
    if path:
        path = Path(path)
        with path.open("w") as file:
            file.write(json_str)
        frame = inspect.currentframe().f_back.f_locals
        ids = [k for k, v in frame.items() if v is self]
        id = ids[0] if len(ids) == 1 else "/".join(ids)
        print(f"\n ⓘ  Saved '{id}' in JSON format to:\n    {path.absolute()}")
    return json_str

def login_to_github():
    """ Use selenium and CleverSession credentials to login to Github """
    self.browser.find_element_by_id("login_field").send_keys(self.username)
    self.browser.find_element_by_id("password").send_keys(self.password)
    self.browser.find_element_by_name("commit").click()

def login_to_twitter():
    """ Use selenium and CleverSession credentials to login to Github """
    self.browser.find_element_by_name("session[username_or_email]").send_keys(self.username)
    self.browser.find_element_by_name("session[password]").send_keys(self.password)
    span = self.browser.find_elements_by_tag_name("span")
    [x for x in span if x.text=="Log in"][0].click()

def login_to_Office365():
    """ Use selenium and CleverSession credentials to login to Office365 """
    self.browser.find_element_by_id("i0116").send_keys(self.username)
    self.browser.find_element_by_id("idSIButton9").click()
    self.browser.find_element_by_id("i0118").send_keys(self.password)
    time.sleep(2)
    self.browser.find_element_by_id("idSIButton9").click()

def login_to_satchelone():
    """ Use selenium and CleverSession credentials to login to SatchelOne """
    # from satchelone_config import userid, pw
    main_window = self.browser.window_handles[0]
    span = self.browser.find_elements_by_tag_name("span")
    [x for x in span if x.text=="Sign in with Office 365"][0].click()
    popup_window = self.browser.window_handles[1]
    self.browser.switch_to.window(popup_window)
    login_to_Office365()
    self.browser.switch_to.window(main_window)
    print("\n ⓘ  Waiting for SatchelOne dashboard to appear...")
    while browser.current_url != 'https://www.satchelone.com/dashboard':
        continue
    print("\n ✓  OK we're in!\n")

def button_menu(choices: iter, prompt=None):
    """
    Presents a general purpose button selection menu using PySimpleGUI.
    Returns the text of the selected button (the 'event')
    """
    prompt = prompt or "Please select a website:"
    width = max([len(x) for x in choices]) +2
    layout=[[sg.Text(prompt, font="calibri 14 bold")]]
    layout.extend(
            [[sg.Button(button_text=url, size=(width,1), font="calibri 12")]
                for url in choices])
    layout.extend([[sg.Text("You can use Tab & Space to navigate", font="calibri 11 italic")]])
    window = sg.Window("cleversession", layout, keep_on_top=True, element_justification="center")
    event, _ = window.read()
    window.close()
    return event

def text_input(prompt, **kwargs):
    """
    Presents a general purpose prompt for text input using PySimpleGUI.
    Returns the text entered, or None if closed with Cancel or X.
    """
    kwargs.update(self.sg_options)
    if "password" in prompt.lower():
        kwargs.update({"password_char": "*"})
    kwargs['default_text'] = kwargs.get('default_text') or ""
    return sg.popup_get_text(prompt, **kwargs)

self= CleverSession()

# self.start()
