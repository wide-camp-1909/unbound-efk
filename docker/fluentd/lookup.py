from dns import resolver
import sys
import json

resolv = resolver.Resolver()
resolv.nameservers = ['1.1.1.1']

while True:
    line = sys.stdin.readline()
    if len(line) < 1:
        continue

    event = json.loads(line)
    if event is None:
        continue

    record_type = event['record_type']
    host = event['host']
    if record_type == 'A' or record_type == 'AAAA':
        ip = [x.address for x in resolv.query(host)][0]
    if record_type == 'PTR':
        ip = '.'.join(reversed(host.split('.')[0:4]))

    event['ip'] = ip
    sys.stdout.write(json.dumps(event))
