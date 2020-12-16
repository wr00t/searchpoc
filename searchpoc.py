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

# External
from youtubesearchpython import SearchVideos

#######################################################################

def print_result(msg):
    print(f"==> {msg}")

def print_header(msg):
    print(f"[+] {msg}")

def search_youtube(cve):
    search = SearchPlaylists(f'intitle:"{cve}" intitle:"poc"', offset = 1, mode = "json", max_results = 5)

    return

def search_exploitdb(cve):
    return

def search_cvebase(cve):
    return

def search_github(cve):
    return

#######################################################################

def main():
    
    return

#######################################################################

if __name__ == "__main__":
    main()


