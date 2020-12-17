#!/usr/bin/env python3

"""
=======THIS IS OVERLY DOCUMENTED=======
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
import sys

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

# Print all results in a all lists
def print_results(*res_mat):
    print(f"==={sys.argv[1]}===")
    for res_lst in res_mat:
        if len(res_lst) == 0:
            return
        for res in res_lst:
            print(res)

# Search videos regarding the asked cve using some Google style keywords
def search_youtube(cve):
    
    # https://pypi.org/project/youtube-search-python/
    # Search results and load them as json objects
    search = SearchVideos(f'intitle:"{cve}" + "poc"', offset = 1, mode = "json", max_results = 3)
    jresults = json.loads(search.result())
    
    # Extract the links and return them
    to_return = []
    for res in jresults["search_result"]:
        link = res["link"]
        to_return.append(link)
    return to_return

# Notation of raw page on github is: 
# https://<url>/cvebase/cvebase.com/main/cve/2000/1xxx/CVE-2000-1209.md
# So from cve (CVE-1234-5678) we have to take 5xxx
def search_cvebase(cve):
    
    # Check for longer numbers (eg: CVE-2019-11111)
    if len(cve) == 13:    
        folder = f"{cve[9]}xxx"
    elif len(cve) == 14:
        folder = f"{cve[9:10]}xxx"
    
    # Getting the year from the first part
    year = f"{cve[4:8]}"
    
    # https://raw.githubusercontent.com/cvebase/cvebase.com/main/cve/{}/{}/{}.md
    url = CVEBASE_URL.format(year, folder, cve) 
    
    # Connect, or skip if not HTTP 200
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return []
    
    # Find all urls in response returning them as list of str
    html = response.read().decode("utf-8")
    return re.findall(r'(https?://[^\s]+)', html)


# Using GH APIs https://docs.github.com/en/free-pro-team@latest/rest/reference/search
def search_github(cve):
    
    # https://api.github.com/search/repositories?q={}&page=1
    url = GITHUB_API_Q.format(cve)
    
    # Connect, or skip if not HTTP 200
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return []
    
    # Refer to the api to know the json format
    ghresp = json.loads(response.read().decode("utf-8"))

    # Return if no result is shown
    if ghresp["total_count"] == 0: return []
    
    # From json extract links to repos
    to_return = []
    for item in ghresp["items"]:
        to_return.append(item["html_url"])
    return to_return

#######################################################################

def main():

    if len(sys.argv) != 2:
        message("Pass just 1 cve as argument")
        exit(1)

    print_results(
        search_youtube(sys.argv[1]), 
        search_cvebase(sys.argv[1]), 
        search_github(sys.argv[1])
        )
    return

#######################################################################

if __name__ == "__main__":
    main()

