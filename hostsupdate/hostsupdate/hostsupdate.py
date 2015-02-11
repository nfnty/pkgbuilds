#!/usr/bin/python3 -u
''' update domain blocking hosts '''

import requests
import os
import re
import time
import subprocess
import json
import sys

DESTDIR = '/etc/hosts.d'
CONFDIR = '/etc/hostsupdate'

def load_conf(conf_file):
    ''' load json config file '''
    try:
        json_data = json.load(open(os.path.join(CONFDIR, conf_file)))
    except OSError as error:
        print('Error: ' + error)
        print('Error: ' + conf_file)
        sys.exit(1)
    except ValueError as error:
        print('Error: ' + error)
        print('Error: ' + conf_file)
        sys.exit(1)
    return json_data

def main():
    ''' main func '''

    sources = load_conf('sources.json')['sources']
    invalid_domains = load_conf('invalid.json')['domains']
    excluded_domains = load_conf('excluded.json')['domains']

    domain_regex = re.compile(
        r'^' +
        r'(?:[A-Za-z0-9-_]{1,63}\.)*' +
        r'(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)' +
        r'(?:(?!-)[A-Za-z0-9-]{2,63}(?<!-))' +
        r'$'
    )

    while sources:
        for source_name, source_url in list(sources):
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
                            or domain_name in invalid_domains \
                            or not domain_regex.fullmatch(domain_name):
                        print('Invalid: "' + domain_name + '"')
                        continue

                    if domain_name in excluded_domains:
                        print('Excluded: "' + domain_name + '"')
                        continue

                    hosts_file.write('0.0.0.0 ' + domain_name + '\n')

            sources.remove((source_name, source_url))

        subprocess.call([
            '/usr/bin/pkill',
            '--uid', 'dnsmasq',
            '--group', 'dnsmasq',
            '--exact',
            '--signal', 'SIGHUP',
            'dnsmasq',
        ])
        if sources:
            print('Sleeping for 600 seconds due to timeout.')
            time.sleep(1800)

if __name__ == '__main__':
    main()
