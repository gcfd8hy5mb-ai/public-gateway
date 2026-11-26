#!/usr/bin/env python3
"""Structural audit only: does not verify live endpoints or legal access."""
import json
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/texas-counties.json').read_text())
assert len(data)==254, 'Expected 254 counties'
for county, entries in data.items():
    seen=set()
    for e in entries:
        url=e['url']
        assert urlsplit(url).scheme=='https' or urlsplit(url).scheme=='http', (county,url)
        assert url not in seen, (county,'duplicate URL',url)
        seen.add(url)
        if 'destinationTier' in e:
            assert e['destinationTier'] in (1,2,3,4), (county,url)
        if e.get('destinationTier') in (1,2,3):
            assert e.get('recordTypes') and e.get('source'), (county,url)
    direct=sum(e.get('destinationTier') in (1,2) for e in entries)
    print(f'{county}: {len(entries)} listings; {direct} tagged direct/portal destinations; completion not inferred')
