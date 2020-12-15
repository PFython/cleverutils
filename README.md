# `cleverutils`
![Replace with your own inspirational logo here](https://github.com/PFython/cleverutils/blob/main/cleverutils.png?raw=true)


# 1. OVERVIEW
Some handy Python utilities and code snippets (beginner to intermediate level) used so often by the author that he took the time to package them up and share on Github/PyPI.  Hopefully they might be of use to other Pythonistas somehwere, some time...

# 2. INSTALLATION

    pip install cleverutils

# 3. BASIC USE

To access the main Session/Login/Scraper classes:

    >>> from cleverutils import CleverSession, Login_to
    >>> cs = CleverSession()
    >>> cs.start()

To access individual functions in `clevergui`:

    >>> from cleverutils import start_gui, button_menu, text_input

`start_gui`, `button_menu`, and `text_input` are simply wrappers around frequently used `PySimpleGUI` functions using a predefined "house style".

# 4. UNDER THE BONNET

Uses `selenium` for webbrowser automation and scraping, `PySimpleGUI` for nice, simple input prompts(\*) and `keyring` for getting/setting credentials.  Uses [`cleverdict`](https://github.com/PFython/cleverdict) for general data management and its handy auto-save/JSON features.

`chomedriver.exe` is included in this repository but you can replace with the latest `selenium` web-driver for your preferred browser.  Please see `selenium` docs/tutorials widely available elsewhere.

# 5. CONTRIBUTING

Hopefully `cleverutils` will be of interest to people getting started with `selenium` and web scraping generally or working with Github, Twitter etc. and not wanting to use their API.  `cleverutils` isn't super elegant or even PEP8 compliant, but does solve simple web scraping challenges quickly, understandably, and extensibly.

Contact Peter Fison peter@southwestlondon.tv or feel free to raise Pull Requests / Issue in the normal Github way.

# 6. PAYING IT FORWARD


If `cleverutils` helps you save time and focus on more important things, please feel free to to show your appreciation by starring the repository on Github.

I'd also be delighted if you wanted to:

<a href="https://www.buymeacoffee.com/{self.github_id}" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" width="217px" ></a>
