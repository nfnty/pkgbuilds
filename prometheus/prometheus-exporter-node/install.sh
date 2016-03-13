post_install() {
    groupadd --gid 535 prometheus-exporter >/dev/null
    useradd --uid 535 --gid prometheus-exporter --home-dir / --shell /usr/bin/false prometheus-exporter >/dev/null
}

post_remove() {
    userdel prometheus-exporter >/dev/null
}
