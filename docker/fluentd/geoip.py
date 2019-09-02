from dns import resolver
import sys
import json
import geoip2.database

reader = geoip2.database.Reader('GeoLite2-City.mmdb')
resolv = resolver.Resolver()
resolv.nameservers = ['1.1.1.1']

while True:
    line = sys.stdin.readline()
    if len(line) < 1:
        continue
    source = json.loads(line)
    if None:
        pass
    elif source['record_type'] == 'A' or source['record_type'] == 'AAAA':
        ip = [x.address for x in resolv.query(source['host'])][0]
    elif source['record_type'] == 'PTR':
        ip = '.'.join(reversed(source['host'].split('.')[0:4]))

    geo = reader.city(ip)
    geo_raw = geo.raw
    location = geo_raw.pop('location')
    geo_raw.update({
        'location': {
            'lat': location['latitude'],
            'lon': location['longitude'],
        }
    })

    source.update(geo_raw)
    sys.stdout.write(json.dumps(source))
