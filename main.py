import multiprocessing
import shutil
import sys
from calendar import c
from itertools import count
from operator import le
from xml.dom.minidom import Document
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import socket

from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)
import pyautogui
import pyperclip
import csv
import pandas as pd
from glob import glob
import os
import random
from selenium.webdriver.common.keys import Keys
import requests
import pathlib
from selenium.webdriver.common.action_chains import ActionChains
import random


def is_connected():
    hostname = "one.one.one.one"
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception:
        pass  # we ignore any errors, returning False
    return False


def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def write_category(category, driver, wordpress_link, current_title):
    driver.find_element(By.TAG_NAME, "textarea").click()
    driver.find_element(By.TAG_NAME, "textarea").send_keys(
        f'Give me in list. The blog you have  just  written falls  in which categories within the following categories : {category}.')
    time.sleep(2)
    driver.find_element(By.TAG_NAME, "textarea").send_keys(Keys.RETURN)
    time.sleep(5)


def main():
    output_file_name = input("Output file  name  without (.csv) = ")
    profile_link = []
    profile_username = []

    count = 0
    prev = 0
    current = 0

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)  # version_main allows to specify your chrome version instead of following chrome global version
    driver.maximize_window()
    driver.get("https://twitter.com/i/flow/login")
    print("Put your cursor  from where  you want to scrap.")
    my_input = input("Enter the 'S' for start scraping the profile ")

    if my_input == 'S':
        while True:
            count = count + 1
            html_doc = driver.page_source

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html_doc, 'html.parser')

            # Find the 'a' tags with the specified attributes
            a_tags = soup.find_all('a', attrs={'role': 'link'})

            # Iterate over the tags and extract the href values and text
            for tag in a_tags:
                try:
                    href = None
                    text = None
                    href = tag.get('href')
                    text = tag.text
                    #print(f'href: {href}, text: {text}')
                    if text is not None and href is not None:
                        if text.startswith('@') and text not in profile_username:
                            profile_link.append(href)
                            profile_username.append(text)

                            current = len(profile_username)
                            print('current = ', current)


                except:
                    pass

            # Scroll down
            pyautogui.scroll(-800)  # scroll down 10 "clicks"

            # Wait for the page to load
            time.sleep(2)

            # print('profile_link = ', len(profile_link))
            # print('profile_username = ', len(profile_username))
            #
            # print('profile_link = ', profile_link)
            # print('profile_username = ', profile_username)
            #
            # profile_link = list(set(profile_link))
            # profile_username = list(set(profile_username))
            # print('profile_link = ', len(profile_link))
            # print('profile_username = ', len(profile_username))
            # print('profile_link = ', profile_link)
            # print('profile_username = ', profile_username)
            # profile_link = ['https://twitter.com' + s for s in profile_link]
            #
            # print('profile_link = ', len(profile_link))
            # print('profile_username = ', len(profile_username))
            #
            # print('profile_link = ', profile_link)
            # print('profile_username = ', profile_username)

            df = pd.DataFrame({
                "tweeter_profile_link": profile_link,
                "tweeter_profile_name": profile_username
            })
            df.to_csv(output_file_name + ".csv", index=True, encoding="utf-8")

            if count % 60 == 0 and current == prev:
                count = 0
                break
            else:
                prev = current


if __name__ == '__main__':
    try:
        main()
    except:
        print("Done")
        raise
