# 👓 searchpoc 👓

## Description

Why manually look for a PoC in the wild, wild web? This python script can query github.com, exploit-db.com, youtube.com and cvebase.com to get as much PoCs as you can get. Enjoy!

## Install

### From the AUR

```bash
# Or whatever AUR helper
paru -S searchpoc
```

### From Github

```bash
git clone https://github.com/5amu/searchpoc
cd searchpoc
sudo mv searchpoc.py /usr/bin/searchpoc
sudo chmod 755 /usr/bin/searchpoc

# OR

sudo wget "https://github.com/5amu/searchpoc/raw/v0.0.1/searchpoc.py" -O /usr/bin/searchpoc
sudo chmod 755 /usr/bin/searchpoc
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
