#!/usr/bin/env bash

rm '/data/software/packages/cache/src/rust-nightly-x86_64-unknown-linux-gnu.tar.gz'
rm '/data/software/packages/cache/src/cargo-nightly-x86_64-unknown-linux-gnu.tar.gz'

DATE=$(date --iso-8601 | sed 's/-/./g')

sed -i "s/^pkgver=.*$/pkgver=0.13.0_$DATE/" 'rust-nightly-bin/PKGBUILD'
sed -i "s/^pkgver=.*$/pkgver=0.0.1_$DATE/" 'cargo-nightly-bin/PKGBUILD'

unset DATE

cd '/data/software/packages/AUR/rust/rust-nightly-bin'
makepkg --noconfirm --log --syncdeps --rmdeps --install
cd '/data/software/packages/AUR/rust/cargo-nightly-bin'
makepkg --noconfirm --log --syncdeps --rmdeps --install
