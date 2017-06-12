#!/usr/bin/env python3
import json
import os
import subprocess
import re
import datetime

CERT_PATH = '/var/lib/lego/certificates'
date_format = '%b %d %H:%M:%S %Y GMT'

alt_name_pattern = r'DNS:([\w.-]+)'
alt_name_re = re.compile(alt_name_pattern)

expires_pattern = r'notAfter=(.+)'
expires_re = re.compile(expires_pattern)

valid_from_pattern = r'notBefore=(.+)'
valid_from_re = re.compile(valid_from_pattern)

data = {'letsencrypt_certificates': {}}

for root, dirs, files in os.walk(CERT_PATH):
    for f in files:
        if f.endswith('.crt') and not f.endswith('.issuer.crt'):
            cmd = ['/usr/bin/openssl', 'x509',
                   '-in', '{cert_file}'.format(cert_file=os.path.join(root, f)),
                   '-noout', '-text', '-dates']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            stdout, _ = p.communicate()
            if p.returncode != 0:
                continue

            stdout = stdout.decode('utf-8')

            subject_alt_names = alt_name_re.findall(stdout)
            expires = expires_re.findall(stdout)[0]

            valid_from = valid_from_re.findall(stdout)[0]

            data['letsencrypt_certificates'][f.rstrip('.crt')] = {
                'domains': sorted(subject_alt_names),
                'expires': datetime.datetime.strptime(expires, date_format).isoformat() + '+00:00',
                'valid_from': datetime.datetime.strptime(valid_from, date_format).isoformat() + '+00:00',
            }

print(json.dumps(data))
