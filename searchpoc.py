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
EXPLOIT_BASEURL = "https://www.exploit-db.com/exploits"
EXPLOITDB_URL_CSV = "https://raw.githubusercontent.com/offensive-security/exploitdb/master/files_exploits.csv"

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
        exploithtml = urllib.request.urlopen(f"{EXPLOIT_BASEURL}/{exdbid}").read().decode("utf-8") 
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
                links.append(f"{EXPLOIT_BASEURL}/{exdbid}")
    return links

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
    exploitdbcsv = DEF_EXPDB_CSV_LOC
    check_exploitdb_csv(os.path.join(os.getcwd(), exploitdbcsv))
    ed = search_exploitdb("CVE-2020-6418", exploitdbcsv)
    if len(ed) != 0:
        print_results("FROM EXPLOITDB (https://www.exploit-db.com/)", ed)

    # TODO: get cvebase results

    # TODO: get github results

    return

#######################################################################

if __name__ == "__main__":
    main()

