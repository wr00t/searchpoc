#!/usr/bin/make -f

PKGNAME := searchpoc

BUILDDIR ?= build
VERSION  ?= 1.0.6
RELEASE  ?= 6

install:
	install -Dm755 ${PKGNAME}.py $(DESTDIR)$(PREFIX)/bin/${PKGNAME}

publish: clean
	find publish -type d -maxdepth 1 -exec make BUILDDIR=$(BUILDDIR) VERSION=$(VERSON) RELEASE=$(RELEASE) -C \{\} publish \;

version-bump:
	sed -i "s/^version.*/version=$(VERSION)/g" publish/install.sh
	sed -i "s/^VERSION.*/VERSION  ?= $(VERSION)/g" Makefile
	sed -i "s/^RELEASE.*/RELEASE  ?= $(RELEASE)/g" Makefile
	git add .
	git commit -m "Version bump: $(VERSION)"
	git push
	git tag $(VERSION)
	git push --tags

clean:
	[ -d $(BUILDDIR) ] && rm -rf $(BUILDDIR)
	find publish -type d -maxdepth 1 -exec make BUILDDIR=$(BUILDDIR) -C \{\} clean \; 