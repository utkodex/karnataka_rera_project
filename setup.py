from setuptools import find_packages,setup

setup(name="karnataka-scraping-system",
       version="0.0.1",
       author="utkarsh",
       author_email="bizzboosterdata@gmail.com",
       packages=find_packages(),
       install_requires=['gspread', 'selenium', 'webdriver-manager', 'google-auth', 'bs4', 'undetected-chromedriver']
       )