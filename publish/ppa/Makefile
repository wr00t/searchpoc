#!/usr/bin/make -f

PKGNAME := searchpoc
PPAMAIL ?= v.casalino@protonmail.com
PPANAME ?= 5amu

build-image:
	sudo docker build -t ppa-publisher .

publish: build-image
	sudo docker run -it --rm -v "$$HOME/.ssh:/home/publisher/.ssh" -v "$$HOME/.gnupg:/home/publisher/.gnupg"  -e "PKGNAME=${PKGNAME}" -e "PPAMAIL=$(PPAMAIL)" -e "PPANAME=$(PPANAME)" -e "VERSION=$(VERSION)" ppa-publisher

clean:
	[ -d $(BUILDDIR) ] && rm -rf $(BUILDDIR)