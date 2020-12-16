# Auto-generated by easyPyPI: https://github.com/PFython/easypypi
# Preserve current formatting to ensure easyPyPI compatibility.

from pathlib import Path
from setuptools import find_packages
from setuptools import setup

NAME = "cleverutils"
GITHUB_USERNAME = "Pfython"
VERSION = "0.19"
DESCRIPTION = "Some handy Python utilities and code snippets used repeatedly by the author and considered beginner to intermediate level of difficulty.  Published just in case they're of use to other Pythonistas somehwere, some time."
LICENSE = "MIT License"
AUTHOR = "Peter Fison"
EMAIL = "peter@southwestlondon.tv"
URL = "https://github.com/Pfython/cleverutils"
KEYWORDS = "cleverutils utils, cleverdict, cleversession, selenium, keyring, pysimplegui"
CLASSIFIERS = "Development Status :: 3 - Alpha, Intended Audience :: Developers, Operating System :: OS Independent, Programming Language :: Python :: 3.6, Programming Language :: Python :: 3.7, Programming Language :: Python :: 3.8, Programming Language :: Python :: 3.9, Topic :: Internet :: WWW/HTTP :: Browsers, Topic :: Internet :: WWW/HTTP :: Session, Topic :: Utilities"
REQUIREMENTS = "cleverdict, pysimplegui, selenium, keyring, pyperclip"


def comma_split(text: str):
    """
    Returns a list of strings after splitting original string by commas
    Applied to KEYWORDS, CLASSIFIERS, and REQUIREMENTS
    """
    if type(text) == list:
        return [x.strip() for x in text]
    return [x.strip() for x in text.split(",")]


if __name__ == "__main__":
    setup(
        name=NAME,
        packages=find_packages(),
        version=VERSION,
        license=LICENSE,
        description=DESCRIPTION,
        long_description=(Path(__file__).parent / "README.md").read_text(),
        long_description_content_type="text/markdown",
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        download_url=f"{URL}/archive/{VERSION}.tar.gz",
        keywords=comma_split(KEYWORDS),
        install_requires=comma_split(REQUIREMENTS),
        classifiers=comma_split(CLASSIFIERS),
    )