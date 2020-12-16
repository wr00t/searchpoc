#!/usr/bin/env python3

"""
DESCRIPTION:
Tool to search on the internet (exploit-db, youtube, cvebase, github) for 
public PoCs, given one or more CVEs in the format of CVE-XXXX-XXXX.
AUTHOR: 
Valerio Casalino <casalinovalerio.cv@gmail.com>
LICENSE:
Refer to the git repo.
"""

#######################################################################

# Built-in
import json
import re
import os

# External
from youtubesearchpython import SearchVideos
import requests
import selenium
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 

#######################################################################

def print_result(msg):
    print(f"==> {msg}")

def print_header(msg):
    print(f"[+] {msg}")

def print_results(header, msg_lst):
    print_header(header)
    for msg in msg_lst:
        print_result(msg)

def get_webdriver(url):
    try:
        browser = webdriver.Firefox() 
        browser.get(url)
        return browser
    except (Exception):
        pass

    return None

def search_youtube(cve):
    to_return = []
    search = SearchVideos(f'intitle:"{cve}" + "poc"', offset = 1, mode = "json", max_results = 3)
    jresults = json.loads(search.result())
    for res in jresults["search_result"]:
        link = res["link"]
        to_return.append(link)
    return to_return

def search_exploitdb(cve):
    cve = re.sub("CVE-", "", cve)
    page = get_webdriver(f"https://www.exploit-db.com/search?cve={cve}")
    page.find_elements(By.TAG_NAME, 'tbody')
    exit(0)
    # pylint: disable=anomalous-backslash-in-string
    return [] # re.findall("CVE", search.text)

def search_cvebase(cve):
    return

def search_github(cve):
    return

#######################################################################

def main():

    # TODO: argument parsing 

    # Get youtube results
    yt = [] # search_youtube("test")
    if len(yt) != 0:
        print_results("FROM YOUTUBE (https://www.youtube.com/)", yt)
    
    # Get exploitdb results
    ed = search_exploitdb("CVE-2020-6418")
    if len(ed) != 0:
        print_results("FROM EXPLOITDB (https://www.exploit-db.com/)", ed)

    # TODO: get cvebase results

    # TODO: get github results

    return

#######################################################################

if __name__ == "__main__":
    main()

