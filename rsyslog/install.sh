post_install() {
    groupadd --gid 534 rsyslog >/dev/null
    useradd --uid 534 --gid rsyslog --home-dir / --shell /usr/bin/false rsyslog >/dev/null
}

post_remove() {
    userdel rsyslog >/dev/null
}
