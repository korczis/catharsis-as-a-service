#!/usr/bin/env python3
"""Static checks on the generated site.

Per page: duplicate ids, image alt text, empty links, in-page anchors, heading order,
title, description, lang and canonical. Site-wide: every first-party reference in HTML,
CSS, the sitemap and robots.txt resolves to a generated file (and anchor, when it has one).

usage: validate-html.py <public-dir> <base-url>
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITEMAP_ALTERNATE = re.compile(r"<xhtml:link[^>]*href=\"([^\"]+)\"")
PREVIEW_META = ("og:title", "og:description", "og:url", "og:image", "og:image:alt", "og:locale", "twitter:card")
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")
# Inline data URIs may contain url() of their own (an SVG filter reference); they are not files.
CSS_DATA_URI = re.compile(r"url\(\s*(['\"])data:.*?\1\s*\)|url\(\s*data:[^)]*\)", re.S)
SITEMAP_LOC = re.compile(r"<loc>([^<]+)</loc>")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.refs = []
        self.images = []
        self.links = []
        self.headings = []
        self.meta = {}
        self.canonical = None
        self.lang = None
        self.title = ""
        self._in_title = False
        self._open_links = []
        self.structured_data = []
        self._in_structured_data = False

    def handle_starttag(self, tag, attrs):
        a = {key: (value or "") for key, value in attrs}
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_structured_data = True
            self.structured_data.append("")
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = a.get("name") or a.get("property")
            if name:
                self.meta[name] = a.get("content", "")
            if a.get("property") in ("og:image", "og:url") or a.get("name") == "twitter:image":
                self.refs.append(a.get("content", ""))
        elif tag == "link":
            if a.get("rel") == "canonical":
                self.canonical = a.get("href")
            if a.get("href"):
                self.refs.append(a["href"])
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))
        if tag in ("script", "img", "source") and a.get("src"):
            self.refs.append(a["src"])
        if a.get("srcset"):
            self.refs.extend(part.strip().split(" ")[0] for part in a["srcset"].split(","))
        if tag == "img":
            self.images.append(a)
            for link in self._open_links:
                link["text"] += a.get("alt", "")
        if tag == "a":
            self._open_links.append({"attrs": a, "text": ""})
            if a.get("href"):
                self.refs.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            self._in_structured_data = False
        elif tag == "a" and self._open_links:
            self.links.append(self._open_links.pop())

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_structured_data:
            self.structured_data[-1] += data
        for link in self._open_links:
            link["text"] += data


def resolve(ref, base_url, public, origin_file):
    """Map a reference to (file, fragment) inside public/, or None for external references."""
    if not ref or ref.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return None
    if ref.startswith("#"):
        return origin_file, ref[1:]
    parts = urlsplit(ref)
    if parts.scheme or ref.startswith("//"):
        if not ref.startswith(base_url + "/") and ref != base_url:
            return None
        rel = ref[len(base_url):]
        rel = urlsplit(rel).path
        target = public / unquote(rel.lstrip("/"))
    else:
        target = (origin_file.parent / unquote(parts.path)).resolve()
    if target.is_dir() or str(target).endswith("/"):
        target = target / "index.html"
    return target, parts.fragment


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    public = Path(sys.argv[1]).resolve()
    base_url = sys.argv[2].rstrip("/")
    errors = []

    pages = {}
    for path in sorted(public.rglob("*.html")):
        parser = Page()
        parser.feed(path.read_text(encoding="utf-8"))
        pages[path] = parser

    anchors_checked = refs_checked = structured_nodes = 0
    for path, page in pages.items():
        rel = path.relative_to(public)
        is_404 = rel.name == "404.html" and rel.parent == Path(".")

        duplicates = sorted({i for i in page.ids if page.ids.count(i) > 1})
        if duplicates:
            errors.append(f"{rel}: duplicate ids {duplicates}")
        for img in page.images:
            if "alt" not in img:
                errors.append(f"{rel}: <img src={img.get('src')}> has no alt attribute")
        for link in page.links:
            attrs = link["attrs"]
            if not (link["text"].strip() or attrs.get("aria-label") or attrs.get("title")):
                errors.append(f"{rel}: empty link href={attrs.get('href')}")
        if page.headings.count(1) != 1:
            errors.append(f"{rel}: expected exactly one <h1>, found {page.headings.count(1)}")
        for previous, current in zip(page.headings, page.headings[1:]):
            if current > previous + 1:
                errors.append(f"{rel}: heading level jumps from h{previous} to h{current}")
        if not page.title.strip():
            errors.append(f"{rel}: empty <title>")
        if not page.meta.get("description", "").strip():
            errors.append(f"{rel}: empty meta description")
        if not page.lang:
            errors.append(f"{rel}: <html> has no lang")
        if not is_404 and not page.canonical:
            errors.append(f"{rel}: no canonical link")
        if not is_404:
            for name in PREVIEW_META:
                if not page.meta.get(name, "").strip():
                    errors.append(f"{rel}: link preview metadata '{name}' is missing or empty")
            if len(page.structured_data) != 1:
                errors.append(f"{rel}: expected one JSON-LD block, found {len(page.structured_data)}")
            for block in page.structured_data:
                try:
                    document = json.loads(block)
                except json.JSONDecodeError as error:
                    errors.append(f"{rel}: JSON-LD does not parse: {error}")
                    continue
                if document.get("@context") != "https://schema.org" or not document.get("@graph"):
                    errors.append(f"{rel}: JSON-LD needs @context https://schema.org and a non-empty @graph")
                    continue
                structured_nodes += len(document["@graph"])
                if "WebSite" not in {node.get("@type") for node in document["@graph"]}:
                    errors.append(f"{rel}: JSON-LD graph has no WebSite node")

        for ref in page.refs:
            resolved = resolve(ref, base_url, public, path)
            if resolved is None:
                continue
            target, fragment = resolved
            refs_checked += 1
            if not target.exists():
                errors.append(f"{rel}: broken reference {ref}")
                continue
            if fragment and target.suffix == ".html":
                anchors_checked += 1
                if fragment not in pages[target].ids:
                    errors.append(f"{rel}: {ref} points to a missing anchor")

    css_checked = 0
    for css in sorted(public.rglob("*.css")):
        for ref in CSS_URL.findall(CSS_DATA_URI.sub("", css.read_text(encoding="utf-8"))):
            if ref.startswith(("data:", "#", "http:", "https:")):
                continue
            css_checked += 1
            if not (css.parent / urlsplit(ref).path).resolve().exists():
                errors.append(f"{css.relative_to(public)}: broken url({ref})")

    sitemap = public / "sitemap.xml"
    robots = public / "robots.txt"
    locs = []
    if not sitemap.exists():
        errors.append("sitemap.xml was not generated")
    else:
        locs = SITEMAP_LOC.findall(sitemap.read_text(encoding="utf-8"))
        text = sitemap.read_text(encoding="utf-8")
        alternates = SITEMAP_ALTERNATE.findall(text)
        for loc in locs + alternates:
            resolved = resolve(loc, base_url, public, sitemap)
            if resolved is None or not resolved[0].exists():
                errors.append(f"sitemap.xml: {loc} is outside the site or missing")
        expected_alternates = len(locs) * (len(set(re.findall(r'hreflang="([^"]+)"', text))))
        if locs and len(alternates) != expected_alternates:
            errors.append(f"sitemap.xml: expected {expected_alternates} hreflang alternates, found {len(alternates)}")
    if not robots.exists():
        errors.append("robots.txt was not generated")
    elif f"{base_url}/sitemap.xml" not in robots.read_text(encoding="utf-8"):
        errors.append("robots.txt does not reference the sitemap under base_url")

    print("HTML")
    print("────────────────────")
    print(f"pages ............. {len(pages)}")
    print(f"references ........ {refs_checked}")
    print(f"anchors ........... {anchors_checked}")
    print(f"css urls .......... {css_checked}")
    print(f"sitemap urls ...... {len(locs)}")
    print(f"json-ld nodes ..... {structured_nodes}")
    for error in errors:
        print(f"error: {error}")
    print()
    print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
