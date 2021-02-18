#!/bin/sh

url="https://github.com/5amu/searchpoc/archive/${VERSION}.tar.gz"

mkdir -p archive src
wget "${url}" -O "archive/${PKGNAME}-${VERSION}.tar.gz"
tar xzf "archive/${PKGNAME}-${VERSION}.tar.gz" --directory=src

mkdir -p "${PKGNAME}/DEBIAN" "${PKGNAME}/usr/bin"

cat > "${PKGNAME}/DEBIAN/control" <<EOF
Package: ${PKGNAME} 
Version: ${VERSION}
Section: base
Priority: optional 
Architecture: all 
Depends: python3 
Maintainer: ${PPANAME} <${PPAMAIL}> 
Description: Search a PoC for a (or some) given CVE id.
EOF

install -Dm755 "src/${PKGNAME}-${VERSION}/searchpoc.py" "${PKGNAME}/usr/bin/searchpoc"

dpkg-deb --build "${PKGNAME}"

git clone github.com:5amu/debtools && cd debtools
mv "../${PKGNAME}.deb" .

# Packages & Packages.gz
dpkg-scanpackages --multiversion . > Packages
gzip -k -f Packages

# Release, Release.gpg & InRelease
apt-ftparchive release . > Release
gpg --default-key "${PPAMAIL}" -abs -o - Release > Release.gpg
gpg --default-key "${PPAMAIL}" --clearsign -o - Release > InRelease

# Commit & push
git add -A
git -c "user.name=${PPANAME}" -c "user.email=${PPAMAIL}" commit -m "${PKGNAME}: version bump -> ${VERSION}"
git push
