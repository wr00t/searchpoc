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
import urllib.request

# TODO: use only built ins
# External
from youtubesearchpython import SearchVideos

#######################################################################

DEF_EXPDB_CSV_LOC = "files_exploits.txt"
EXPLOIT_BASEURL = "https://www.exploit-db.com/exploits/{}"
EXPLOITDB_URL_CSV = "https://raw.githubusercontent.com/offensive-security/exploitdb/master/files_exploits.csv"
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

# This function does nothing if the file already exist, but writes a custom
# file with id:cves line by line to put in the current working directory (or where specified)
def check_exploitdb_csv(to_write):
    if os.path.exists(to_write):
        message(f"{to_write} already exist, skipping...")
        return
    
    message("Hang on... This will be long")
    fp = open(to_write, "a")
    response = urllib.request.urlopen(EXPLOITDB_URL_CSV)
    firstline = True
    for line in response:
        if firstline:
            firstline = False
            continue
        fields = line.split(b",")
        exdbid = fields[0].decode("utf-8")
        url = EXPLOIT_BASEURL.format(exdbid)
        exploithtml = urllib.request.urlopen(url).read().decode("utf-8") 
        # pylint: disable=anomalous-backslash-in-string
        cvenum = ",".join(list(set(re.findall("CVE-\d{4}-\d{2}",exploithtml))))
        fp.write(f"{cvenum}:{exdbid}\n")
    fp.close()

# This will look in a custom file, previously specified, for a match cve -> exploit-link
def search_exploitdb(cve, dbfile):
    links = []
    with open(dbfile, "r") as customdb:
        for line in customdb.readlines():
            if re.match(cve, line):
                exdbid = line.split(":")[0]
                to_append = EXPLOIT_BASEURL.format(exdbid)
                links.append(to_append)
    return links

def search_cvebase(cve):
    # Notation of raw page on github is: 
    # https://<url>/cvebase/cvebase.com/main/cve/2000/1xxx/CVE-2000-1209.md
    # So from cve (CVE-1234-5678) we have to take 5xxx
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

    # TODO: argument parsing 

    # Get youtube results
    yt = [] # search_youtube("test")
    if len(yt) != 0:
        print_results("FROM YOUTUBE (https://www.youtube.com/)", yt)
    
    # TODO: find better solution
    # Get exploitdb results
    # exploitdbcsv = DEF_EXPDB_CSV_LOC
    # check_exploitdb_csv(os.path.join(os.getcwd(), exploitdbcsv))
    # ed = search_exploitdb("CVE-2020-6418", exploitdbcsv)
    # if len(ed) != 0:
    #     print_results("FROM EXPLOITDB (https://www.exploit-db.com/)", ed)

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

