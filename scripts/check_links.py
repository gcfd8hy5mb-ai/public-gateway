"""Check public directory URLs without collecting records or personal data."""
import json, re, time
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlsplit
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent.parent
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls=set()
    def handle_starttag(self,tag,attrs):
        url=dict(attrs).get('href','')
        if tag=='a' and url.startswith(('http://','https://')):
            self.urls.add(url)
parser=Links()
parser.feed((ROOT/'records.html').read_text(encoding='utf-8'))
data=json.loads((ROOT/'data/texas-counties.json').read_text(encoding='utf-8'))
urls=sorted(parser.urls | {x['url'] for rows in data.values() for x in rows})
def check(url):
    try:
        req=Request(url,headers={'User-Agent':'PublicGateway-LinkAudit/1.0'},method='HEAD')
        try:
            response=urlopen(req,timeout=15)
        except HTTPError as e:
            if e.code not in (403,405,501): raise
            response=urlopen(Request(url,headers={'User-Agent':'PublicGateway-LinkAudit/1.0','Range':'bytes=0-1023'}),timeout=15)
        with response as r:
            final=r.geturl()
            return {'url':url,'http':r.status,'final_url':final,'status':'redirect_review' if final!=url else 'reachable'}
    except HTTPError as e:
        return {'url':url,'http':e.code,'status':'manual_review' if e.code in (401,403,429) else 'http_error'}
    except Exception as e:
        return {'url':url,'status':'connection_review','error':type(e).__name__}
    finally:
        time.sleep(0.4)
with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(check,urls))
report={'checked_at':datetime.now(timezone.utc).isoformat(),'unique_urls':len(urls),'results':results}
out=ROOT/'reports'
out.mkdir(exist_ok=True)
(out/'link-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
from collections import Counter
print(json.dumps(dict(Counter(r['status'] for r in results)),indent=2))
print('Reachability is not verification of ownership, content, access or accuracy.')
