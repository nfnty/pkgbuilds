#!/usr/bin/env bash

DATE=`date --iso-8601 | sed 's/-/./g'`

sed -i "s/^pkgver=.*$/pkgver=0.13.0_$DATE/" rust-nightly-bin/PKGBUILD
sed -i "s/^pkgver=.*$/pkgver=0.0.1_$DATE/" cargo-nightly-bin/PKGBUILD

unset DATE

cd rust-nightly-bin
makepkg --noconfirm -s -r -L -i
cd ../cargo-nightly-bin
makepkg --noconfirm -s -r -L -i
