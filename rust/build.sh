#!/usr/bin/env bash

rm '/data/software/packages/cache/src/rust-nightly-x86_64-unknown-linux-gnu.tar.gz'

DATE=$(date --iso-8601 | sed 's/-/./g')

sed -i "s/^pkgver=.*$/pkgver=1.0.0_$DATE/" 'rust-nightly-bin/PKGBUILD'

unset DATE

cd '/data/software/packages/builds/rust/rust-nightly-bin'
makepkg --noconfirm --log --syncdeps --rmdeps --install --cleanbuild
