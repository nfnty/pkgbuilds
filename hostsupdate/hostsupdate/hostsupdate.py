#!/usr/bin/python3 -u
''' update domain blocking hosts '''

import requests
import os
import re
import time
import subprocess

DESTDIR = '/etc/hosts.d'
SOURCES = [
    ('malwaredomainlist_com', 'http://www.malwaredomainlist.com/hostslist/hosts.txt'),
    ('someonewhocares_org', 'http://someonewhocares.org/hosts/zero/hosts'),
    ('mvps_org', 'http://winhelp2002.mvps.org/hosts.txt'),
    ('pgl_yoyo_org', 'http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=1&mimetype=plaintext'),
    ('hosts-file_net_ad_servers', 'http://hosts-file.net/ad_servers.txt'),
    ('hosts-file_net_emd', 'http://hosts-file.net/emd.txt'),
    ('hosts-file_net_exp', 'http://hosts-file.net/exp.txt'),
    ('hosts-file_net_fsa', 'http://hosts-file.net/fsa.txt'),
    ('hosts-file_net_grm', 'http://hosts-file.net/grm.txt'),
    ('hosts-file_net_hfs', 'http://hosts-file.net/hfs.txt'),
    ('hosts-file_net_hjk', 'http://hosts-file.net/hjk.txt'),
    ('hosts-file_net_mmt', 'http://hosts-file.net/mmt.txt'),
    ('hosts-file_net_pha', 'http://hosts-file.net/pha.txt'),
    ('hosts-file_net_psh', 'http://hosts-file.net/psh.txt'),
    ('malwaredomains_com', 'http://mirror1.malwaredomains.com/files/justdomains'),
]

INVALID_DOMAINS = [
    'localhost.localdomain'
]

EXCLUDED_DOMAINS = [
]

def main():
    ''' main func '''

    domain_regex = re.compile(
        r'^' +
        r'(?:[A-Za-z0-9-_]{1,63}\.)*' +
        r'(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)' +
        r'(?:(?!-)[A-Za-z0-9-]{2,63}(?<!-))' +
        r'$'
    )

    while SOURCES:
        for source_name, source_url in list(SOURCES):
            print('### ' + source_name + ' ###')

            try:
                req = requests.get(source_url, timeout=30)
            except requests.exceptions.Timeout as error:
                print(error)
                continue

            lines = []
            for line in req.text.splitlines():
                line = line.partition('#')
                if line[0].strip():
                    lines.append(line[0].split())

            with open(os.path.join(DESTDIR, source_name), 'w') as hosts_file:
                for line in lines:
                    try:
                        domain_name = line[-1].encode('idna').decode('UTF-8')
                    except UnicodeError as error:
                        print('Error: ' + error)
                        print('Error: "' + line[-1] + '"')
                        continue
                    if line[-1] != domain_name:
                        print('Before: "' + line[-1] + '"')
                        print('After: "' + domain_name + '"')

                    if len(domain_name) > 253 \
                            or domain_name in INVALID_DOMAINS \
                            or not domain_regex.fullmatch(domain_name):
                        print('Invalid: "' + domain_name + '"')
                        continue

                    if domain_name in EXCLUDED_DOMAINS:
                        print('Excluded: "' + domain_name + '"')
                        continue

                    hosts_file.write('0.0.0.0 ' + domain_name + '\n')

            SOURCES.remove((source_name, source_url))

        subprocess.call([
            '/usr/bin/pkill',
            '--uid', 'dnsmasq',
            '--group', 'dnsmasq',
            '--exact',
            '--signal', 'SIGHUP',
            'dnsmasq',
        ])
        if SOURCES:
            print('Sleeping for 600 seconds due to timeout.')
            time.sleep(1800)

if __name__ == '__main__':
    main()
