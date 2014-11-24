#!/usr/bin/env bash

DATE=`date --iso-8601 | sed 's/-/./g'`

sed -i "s/^pkgver=.*$/pkgver=$DATE/" 'rust-nightly-bin/PKGBUILD'
sed -i "s/^pkgver=.*$/pkgver=$DATE/" 'cargo-nightly-bin/PKGBUILD'

unset DATE

cd 'rust-nightly-bin'
makepkg --noconfirm -s -r -L -i
cd '../cargo-nightly-bin'
makepkg --noconfirm -s -r -L -i
