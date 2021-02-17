#!/usr/bin/make -f

PKGNAME := searchpoc

BUILDDIR ?= bin
VERSION  ?= 1.0.3
RELEASE  ?= 3

build:
	mkdir -p $(BUILDDIR)
	cd $(BUILDDIR) && nuitka3 --show-progress --standalone ../${PKGNAME}.py

install:
	install -Dm755 $(BUILDDIR)/${PKGNAME}.dist/${PKGNAME} $(DESTDIR)$(PREFIX)/bin/${PKGNAME}

publish-aur: build
	mkdir -p $(BUILDDIR)
	git clone ssh://aur@aur.archlinux.org/${PKGNAME}.git $(BUILDDIR)/${PKGNAME}-aur
	cp $(SCRIPTDIR)/PKGBUILD $(BUILDDIR)/${PKGNAME}-aur/PKGBUILD
	sed -i "s/<version>/$(VERSION)/g" $(BUILDDIR)/${PKGNAME}-aur/PKGBUILD
	sed -i "s/<release>/$(RELEASE)/g" $(BUILDDIR)/${PKGNAME}-aur/PKGBUILD
	cd $(BUILDDIR)/${PKGNAME}-aur && makepkg --printsrcinfo > .SRCINFO
	git --work-tree=$(BUILDDIR)/${PKGNAME}-aur --git-dir=$(BUILDDIR)/${PKGNAME}-aur/.git add .
	git --work-tree=$(BUILDDIR)/${PKGNAME}-aur --git-dir=$(BUILDDIR)/${PKGNAME}-aur/.git -c "user.email=$(AURMAIL)" -c "user.name=$(AURNAME)" commit -m "Bump to v$(VERSION)"
	git --work-tree=$(BUILDDIR)/${PKGNAME}-aur --git-dir=$(BUILDDIR)/${PKGNAME}-aur/.git push

version-bump:
	sed -i "s/^VERSION.*/VERSION  ?= $(VERSION)/g" Makefile
	sed -i "s/^RELEASE.*/RELEASE  ?= $(RELEASE)/g" Makefile
	git add .
	git commit -m "Version bump: $(VERSION)"
	git push
	git tag $(VERSION)
	git push --tags

clean:
	[ -d $(BUILDDIR) ] && rm -rf $(BUILDDIR)