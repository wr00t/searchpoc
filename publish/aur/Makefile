#!/usr/bin/make -f

PKGNAME := searchpoc
AURMAIL ?= v.casalino@protonmail.com
AURNAME ?= 5amu

publish:
	mkdir -p $(BUILDDIR)
	git clone ssh://aur@aur.archlinux.org/${PKGNAME}.git $(BUILDDIR)/${PKGNAME}
	cp PKGBUILD $(BUILDDIR)/${PKGNAME}-aur/PKGBUILD
	sed -i "s/<version>/$(VERSION)/g" $(BUILDDIR)/${PKGNAME}-aur/PKGBUILD
	sed -i "s/<release>/$(RELEASE)/g" $(BUILDDIR)/${PKGNAME}-aur/PKGBUILD
	cd $(BUILDDIR)/${PKGNAME}-aur && makepkg --printsrcinfo > .SRCINFO
	git --work-tree=$(BUILDDIR)/${PKGNAME}-aur --git-dir=$(BUILDDIR)/${PKGNAME}-aur/.git add .
	git --work-tree=$(BUILDDIR)/${PKGNAME}-aur --git-dir=$(BUILDDIR)/${PKGNAME}-aur/.git -c "user.email=$(AURMAIL)" -c "user.name=$(AURNAME)" commit -m "Bump to v$(VERSION)"
	git --work-tree=$(BUILDDIR)/${PKGNAME}-aur --git-dir=$(BUILDDIR)/${PKGNAME}-aur/.git push

clean:
	[ -d $(BUILDDIR) ] && rm -rf $(BUILDDIR) 