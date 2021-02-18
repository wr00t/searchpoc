# 👓 searchpoc 👓

## Description

Why manually look for a PoC in the wild, wild web? This python script can query github.com, exploit-db.com, youtube.com and cvebase.com to get as much PoCs as you can get. Enjoy!

## Install

### From the AUR

```bash
# Or whatever AUR helper
paru -S searchpoc
```

### From the PPA

```bash
# Add the ppa
curl -s --compressed "https://ppa.casali.no/key.gpg" | sudo apt-key add -
sudo curl -s --compressed -o /etc/apt/sources.list.d/5amu-debtools.list "https://ppa.casali.no/5amu-debtools.list"
sudo apt update

# Install the package
sudo apt install searchpoc
```

### Using the script

```bash
curl -sL https://raw.githubusercontent.com/5amu/searchpoc/master/publish/install.sh | sudo sh
```

## Usage

```
./searchpoc.py --help
 ____                      _
/ ___|  ___  __ _ _ __ ___| |__  _ __   ___   ___
\___ \ / _ \/ _` | '__/ __| '_ \| '_ \ / _ \ / __|
 ___) |  __/ (_| | | | (__| | | | |_) | (_) | (__
|____/ \___|\__,_|_|  \___|_| |_| .__/ \___/ \___|
                                |_|
             - by 5amu (github.com/5amu/searchpoc)

usage: searchpoc.py [-h] [-f F] [-m {yt,gh,cb} [{yt,gh,cb} ...]] [cve]

Search PoCs in the wild

positional arguments:
  cve                   Newline separated cve list in file

optional arguments:
  -h, --help            show this help message and exit
  -f F, --file F        Newline separated cve list in file
  -m {yt,gh,cb,ed} [{yt,gh,cb,ed} ...], --mode {yt,gh,cb} [{yt,gh,cb} ...]
                        Where should the program search? More parameters are allowed, default is all.
```
