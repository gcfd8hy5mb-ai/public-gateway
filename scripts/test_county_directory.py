import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'records.html').read_text()
DATA=json.loads((ROOT/'data/texas-counties.json').read_text())
TAX=json.loads(re.search(r'const taxonomy=(\{.*?\}),groupFor=',HTML,re.S)[1])
class Coverage(unittest.TestCase):
    def test_counties(self):
        self.assertEqual(len(DATA),254)
    def test_unique_urls(self):
        for name,entries in DATA.items():
            self.assertEqual(len(entries),len({e['url'] for e in entries}),name)
    def test_lamar_judicial_portal(self):
        rows=[e for e in DATA['Lamar'] if 'portal-txlamar' in e['url']]
        self.assertEqual(len(rows),1)
        self.assertTrue({'Criminal Records','Arrest Records','Court Calendars','Jail Bond Records','Probate Records'}.issubset(rows[0]['recordTypes']))
    def test_lamar_property_portal(self):
        rows=[e for e in DATA['Lamar'] if 'esearch.lamarcad.org' in e['url']]
        self.assertEqual(len(rows),1)
        self.assertIn('Property Ownership',rows[0]['recordTypes'])
    def test_vital_order_not_direct_search(self):
        row=next(e for e in DATA['Lamar'] if 'permitium' in e['url'])
        self.assertEqual(row['destinationTier'],3)
    def test_lamar_taxonomy(self):
        types={t for group in TAX.values() for t in group}
        for e in DATA['Lamar']:
            self.assertTrue(set(e.get('recordTypes',[]))<=types,e['label'])
    def test_inheritance_integration_markers(self):
        for marker in ['inherited.push(a)','for(const a of inherited)','seen.has(anchor.href)','Federal source — not a county-specific search']:
            self.assertIn(marker,HTML)
if __name__=='__main__': unittest.main()
