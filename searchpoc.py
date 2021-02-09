#!/usr/bin/env python3

"""
=======THIS IS OVERLY DOCUMENTED=======
DESCRIPTION:
Tool to search on the internet (youtube, cvebase, github) for 
public PoCs, given one or more CVEs in the format of CVE-XXXX-XXXX.
AUTHOR: 
Valerio Casalino <casalinovalerio.cv@gmail.com>
LICENSE:
Refer to the git repo.
"""
# TODO:
#       - Implement a search for exploitdb

#######################################################################

# Built-in
import json
import re
import os
import urllib.request
import sys
import argparse
from termcolor import colored


#######################################################################

CVEBASE_URL = "https://raw.githubusercontent.com/cvebase/cvebase.com/main/cve/{}/{}/{}.md"
GHAPI_QUERY = "https://api.github.com/search/repositories?q={}&page=1"
YOUTUBE_URL = "https://youtube.com/results?search_query={}"

#######################################################################

# Print all results in a all lists
def print_results(*res_mat):
    result = []
    for res_lst in res_mat:
        if len(res_lst) == 0:
            continue
        for res in res_lst:
            result.append(res)
    if len(result) == 0 : return
    str_res = ", ".join(list(set(result)))
    print(f"{sys.argv[1]}: {str_res}")

# Search videos regarding the asked cve using some Google style keywords
# Heavily inspired by https://github.com/joetats/youtube_search
def search_youtube(cve):

    query = urllib.parse.quote(f'intitle:"{cve}" + "poc"')
    url = YOUTUBE_URL.format(query)

    try:
        found = False
        while not found:
            response = urllib.request.urlopen(url)
            response = response.read().decode("utf-8")
            found = "ytInitialData" in response
    except urllib.error.HTTPError:
        return []

    results = []
    start = (
        response.index("ytInitialData")
        + len("ytInitialData")
        + 3
    )
    end = response.index("};", start) + 1

    json_str = response[start:end]
    data = json.loads(json_str)

    for video in data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]:
        res = {}
        if "videoRenderer" in video.keys():
            video_data = video.get("videoRenderer", {})
            res = video_data.get("videoId", None)
            results.append(res)

    for i in range(len(results)):
        results[i] = f"https://youtube.com/watch?v={results[i]}"

    return results

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
    url = GHAPI_QUERY.format(cve)
    
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

def banner():
    print(colored(" ____                      _                      ","red"))
    print(colored("/ ___|  ___  __ _ _ __ ___| |__  _ __   ___   ___ ","red"))
    print(colored("\\___ \\ / _ \\/ _` | '__/ __| '_ \\| '_ \\ / _ \\ / __|","red"))
    print(colored(" ___) |  __/ (_| | | | (__| | | | |_) | (_) | (__ ","red"))
    print(colored("|____/ \\___|\\__,_|_|  \\___|_| |_| .__/ \\___/ \\___|","red"))
    print(colored("                                |_| ","red"))
    print(colored("             - by 5amu (github.com/5amu/searchpoc)\n", "red"))


# Parse arguments from command line
def argument_parsing():
    parser = argparse.ArgumentParser(
        prog='searchpoc.py',
        description=f"{banner()}Search PoCs in the wild"
        )
    parser.add_argument('-f', '--file', default=None, help='Newline separated cve list in file')
    """ parser.add_argument('-f', '--file', default=None, help='')
    parser.add_argument('-f', '--file', default=None, help='Newline separated cve list in file') """
    parser.add_argument('cve', nargs='+', help='Newline separated cve list in file')

    return parser.parse_args()


# Wrapper for computing the cve
def run_with(cve):
    print_results(
        search_youtube(cve), 
        search_cvebase(cve), 
        search_github(cve)
        )

def main():

    args = argument_parsing()
    
    if args.cve:
        run_with(args.cve)
    
    return

#######################################################################

if __name__ == "__main__":
    main()

