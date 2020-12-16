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

# External
from youtubesearchpython import SearchVideos
import requests

#######################################################################

def print_result(msg):
    print(f"==> {msg}")

def print_header(msg):
    print(f"[+] {msg}")

def print_results(header, msg_lst):
    print_header(header)
    for msg in msg_lst:
        print_result(msg)

def search_youtube(cve):
    to_return = []
    search = SearchVideos(f'intitle:"{cve}" + "poc"', offset = 1, mode = "json", max_results = 3)
    jresults = json.loads(search.result())
    for res in jresults["search_result"]:
        link = res["link"]
        to_return.append(link)
    return to_return

def search_exploitdb(cve):
    cve = cve.removeprefix("CVE-")
    search = requests.get(f"https://www.exploit-db.com/search?cve={cve}")
    # pylint: disable=anomalous-backslash-in-string
    return re.findall("/exploits/[0-9]{1,6}", search.text)

def search_cvebase(cve):
    return

def search_github(cve):
    return

#######################################################################

def main():

    # TODO: argument parsing 

    # Get youtube results
    yt = search_youtube("test")
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

