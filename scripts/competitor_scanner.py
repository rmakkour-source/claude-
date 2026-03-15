#!/usr/bin/env python3
"""
BingeBear Competitor Radar
Scans rival IPTVs and traditional TV giants (Sky/Virgin) to find their pricing
and weak points (contracts, no guarantees) so we can exploit them in our FB ads.
"""
import sys
import json
import re
import urllib.request
import ssl
from html.parser import HTMLParser

class CompetitorScanner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pricing_found =[]
        self.weaknesses_detected = []
        self._all_text =[]

    def handle_data(self, data):
        text = data.strip().lower()
        if not text: return
        self._all_text.append(text)
        
        # Look for competitor pricing patterns
        if re.search(r'(£|€|\$)\d+(/mo| per month|/month)', text):
            self.pricing_found.append(data.strip())
            
        # Look for competitor weaknesses (Contracts, hardware)
        weakness_keywords =["18-month contract", "12-month contract", "satellite dish", "installation fee", "no refunds"]
        for w in weakness_keywords:
            if w in text: self.weaknesses_detected.append(w.title())

def scan_competitor(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    try:
        html = urllib.request.urlopen(req, timeout=15, context=ctx).read().decode("utf-8")
        parser = CompetitorScanner()
        parser.feed(html)
        return {
            "target_competitor": url,
            "expensive_pricing_found": list(set(parser.pricing_found))[:5],
            "competitor_weaknesses_to_exploit": list(set(parser.weaknesses_detected)),
            "attack_angle": "Compare their £100/mo lock-in contract to our €250 Lifetime One-Off payment."
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"usage": "python3 competitor_scanner.py <competitor_url>"}, indent=2))
    else:
        url = sys.argv[1] if sys.argv[1].startswith("http") else "https://" + sys.argv[1]
        print(json.dumps(scan_competitor(url), indent=2))
