#!/usr/bin/env python3

"""
DESCRIPTION:
Tool to search on the internet (shodan, youtube, cvebase, github) for 
public PoCs, given one or more CVEs in the format of CVE-XXXX-XXXX.
AUTHOR: 
Valerio Casalino <casalinovalerio.cv@gmail.com>
LICENSE:
Refer to the git repo.
"""
# TODO:
#       - Use built in imports only
#       - Implement a search for exploitdb
#       - Handle urllib better (exceptions)
#       - Argument parsing and aking the script usable
#       - Code style refinements

#######################################################################

# Built-in
import json
import re
import os
import urllib.request

# External
from youtubesearchpython import SearchVideos

#######################################################################

CVEBASE_URL = "https://raw.githubusercontent.com/cvebase/cvebase.com/main/cve/{}/{}/{}.md"
GITHUB_API_Q = "https://api.github.com/search/repositories?q={}&page=1"
GITHUB_API_H = "application/vnd.github.v3+json"

#######################################################################

# Just a logging function
def message(msg):
    print(f"[+] {msg}")

# Print all results in a list with custom header
def print_results(header, res_lst):
    print("[+][+]", header)
    for res in res_lst:
        print(res)

# Search videos regarding the asked cve using some Google style keywords
def search_youtube(cve):
    to_return = []
    # https://pypi.org/project/youtube-search-python/
    search = SearchVideos(f'intitle:"{cve}" + "poc"', offset = 1, mode = "json", max_results = 3)
    jresults = json.loads(search.result())
    for res in jresults["search_result"]:
        link = res["link"]
        to_return.append(link)
    return to_return

# Notation of raw page on github is: 
# https://<url>/cvebase/cvebase.com/main/cve/2000/1xxx/CVE-2000-1209.md
# So from cve (CVE-1234-5678) we have to take 5xxx
def search_cvebase(cve):    
    folder = f"{cve[9]}xxx"
    year = f"{cve[4:8]}"
    url = CVEBASE_URL.format(year, folder, cve)
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return []
    html = response.read().decode("utf-8")
    return re.findall(r'(https?://[^\s]+)', html)

# Using GH APIs https://docs.github.com/en/free-pro-team@latest/rest/reference/search
def search_github(cve):
    url = GITHUB_API_Q.format(cve)
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return []
    ghresp = json.loads(response.read().decode("utf-8"))
    if ghresp["total_count"] == 0:
        return []
    to_return = []
    for item in ghresp["items"]:
        to_return.append(item["html_url"])
    return to_return

#######################################################################

def main():

    # Get youtube results
    yt = search_youtube("test")
    if len(yt) != 0:
        print_results("FROM YOUTUBE (https://www.youtube.com/)", yt)

    cb = search_cvebase("CVE-2000-1209")
    if len(cb) != 0:
        print_results("FROM CVEBASE (https://www.cvebase.com/)", cb)

    gh = search_github("CVE-2000-1350")
    if len(gh) != 0:
        print_results("FROM GITHUB (https://github.com/)", gh)

    return

#######################################################################

if __name__ == "__main__":
    main()

