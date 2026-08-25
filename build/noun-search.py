#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Search the Noun Project and list the icons we are allowed to use.

    python3 build/noun-search.py caliper multimeter "technical drawing"

Only CC BY and public domain results are printed. Everything else on that site
is licensed per download and is not usable here.
"""
import json, re, sys, urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
OPEN = ("License.CREATIVECOMMONS", "License.PUBLICDOMAIN")


def search(term, limit=40):
    url = "https://thenounproject.com/search/icons/?q=" + urllib.parse.quote(term)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S)
    if not m:
        return []
    def walk(o):
        if isinstance(o, dict):
            if "license" in o and "thumbnails" in o:
                yield o
            for v in o.values():
                yield from walk(v)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v)
    out, seen = [], set()
    for it in walk(json.loads(m.group(1))):
        if it["license"] not in OPEN or it["id"] in seen:
            continue
        seen.add(it["id"])
        out.append({
            "id": it["id"],
            "title": it.get("title", ""),
            "creator": (it.get("creator") or {}).get("name", ""),
            "license": "CC BY 3.0" if it["license"] == "License.CREATIVECOMMONS" else "Public domain",
            "png512": (it.get("thumbnails") or {}).get("thumbnail512", ""),
            "page": "https://thenounproject.com" + it.get("url", ""),
        })
        if len(out) >= limit:
            break
    return out


if __name__ == "__main__":
    import urllib.parse
    for term in sys.argv[1:]:
        print("== %s ==" % term)
        for r in search(term, 14):
            print("  %-9s %-28s %-24s %s" % (r["id"], r["title"][:28], r["creator"][:24], r["license"]))
