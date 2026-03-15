#!/usr/bin/env python3
"""
BingeBear Funnel Auditor - Mind-Blowing Landing Page Scanner
Scrapes any URL to check for BingeBear's critical conversion elements:
WhatsApp mentions, Risk Reversals, Sky TV price anchoring, and FB Pixels.
"""

import sys
import json
import urllib.request
import ssl
from html.parser import HTMLParser
from urllib.parse import urlparse

class BingeBearParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content =[]
        self.tracking_scripts = []
        self.ctas =[]
        self.bingebear_metrics = {
            "mentions_whatsapp": 0,
            "mentions_lifetime": 0,
            "mentions_guarantee": 0,
            "mentions_sky_or_virgin": 0,
            "mentions_buffering": 0
        }
        self._in_a = False
        self._current_text = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a":
            self._in_a = True
            self._current_text = ""
        elif tag == "script":
            src = attrs_dict.get("src", "").lower()
            if "fbevents" in src or "facebook" in src:
                self.tracking_scripts.append("Meta Pixel")
            elif "gtag" in src or "google-analytics" in src:
                self.tracking_scripts.append("Google Analytics")

    def handle_endtag(self, tag):
        if tag == "a" and self._in_a:
            self._in_a = False
            text = self._current_text.strip()
            if text:
                self.ctas.append(text)

    def handle_data(self, data):
        if self._in_a:
            self._current_text += data
        
        text_lower = data.lower()
        if "whatsapp" in text_lower: self.bingebear_metrics["mentions_whatsapp"] += 1
        if "lifetime" in text_lower or "€250" in text_lower: self.bingebear_metrics["mentions_lifetime"] += 1
        if "90-day" in text_lower or "guarantee" in text_lower: self.bingebear_metrics["mentions_guarantee"] += 1
        if "sky" in text_lower or "virgin" in text_lower: self.bingebear_metrics["mentions_sky_or_virgin"] += 1
        if "buffer" in text_lower or "freez" in text_lower: self.bingebear_metrics["mentions_buffering"] += 1

def analyze(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    try:
        html = urllib.request.urlopen(req, timeout=15, context=ctx).read().decode("utf-8")
        parser = BingeBearParser()
        parser.feed(html)
        
        return {
            "url": url,
            "status": "Success",
            "critical_tracking_found": list(set(parser.tracking_scripts)),
            "bingebear_copy_score": parser.bingebear_metrics,
            "cta_buttons_found": list(set(parser.ctas))[:5],
            "cmo_verdict": "CRITICAL RISK: You are missing WhatsApp setup mentions!" if parser.bingebear_metrics["mentions_whatsapp"] == 0 else "Copy looks primed for older UK/IE demographics."
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"usage": "python3 analyze_page.py <url>"}, indent=2))
    else:
        url = sys.argv[1] if sys.argv[1].startswith("http") else "https://" + sys.argv[1]
        print(json.dumps(analyze(url), indent=2))
