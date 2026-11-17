#!/usr/bin/env python3
"""Generate a Shields endpoint without discarding a last known citation count."""

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.request import urlopen


AUTHOR_ID = "xtnpJe4AAAAJ"
CACHE_URL = "https://jonahjia.github.io/assets/data/scholar.json"


class ScholarTableParser(HTMLParser):
    """Read only Google's citation summary table, preserving column order."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.table_depth = 0
        self.rows = []
        self.row = []
        self.cell = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "table":
            if self.table_depth:
                self.table_depth += 1
            elif attrs.get("id") == "gsc_rsb_st":
                self.table_depth = 1
            return
        if self.table_depth != 1:
            return
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = {"classes": attrs.get("class", "").split(), "text": []}

    def handle_data(self, data):
        if self.table_depth == 1 and self.cell is not None:
            self.cell["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "table" and self.table_depth:
            self.table_depth -= 1
            return
        if self.table_depth != 1:
            return
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(self.cell)
            self.cell = None
        elif tag == "tr":
            self.rows.append(self.row)
            self.row = []


def parse_citations(html):
    parser = ScholarTableParser()
    parser.feed(html)
    for row in parser.rows:
        counts = [cell for cell in row if "gsc_rsb_std" in cell["classes"]]
        if counts:
            # The first data row is Citations; the first count is All, not Since.
            raw = "".join(counts[0]["text"])
            normalized = re.sub(r"[\s,]", "", raw)
            if not re.fullmatch(r"[0-9]+", normalized):
                raise ValueError("Scholar's all-time citation count is not an integer")
            return int(normalized)
    raise ValueError("Scholar's citation summary table is unavailable")


def valid_saved_count(payload, author_id):
    if not isinstance(payload, dict) or payload.get("author_id") != author_id:
        return None
    count = payload.get("citations")
    # bool is an int subclass; accepting True here would display a false count.
    if type(count) is not int or count < 0:
        return None
    checked_at = payload.get("checked_at")
    return count, checked_at if isinstance(checked_at, str) else None


def verification_time(value):
    """Normalize ISO verification dates for comparing cached and manual data."""
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    # Date-only or naive ISO values are interpreted consistently as UTC.
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def make_badge(author_id, count, checked_at, attempted_at, status):
    return {
        "schemaVersion": 1,
        "label": "Citations",
        "message": str(count) if count is not None else "—",
        "color": "9cf",
        "labelColor": "f6f6f6",
        "author_id": author_id,
        "citations": count,
        "checked_at": checked_at,
        "last_attempt_at": attempted_at,
        "status": status,
    }


def resolve_stats(author_id, profile_loader, cache_loader, seed, now):
    """Try Scholar once, then the site's saved value, then the explicit seed."""
    warnings = []
    try:
        count = parse_citations(profile_loader())
        return make_badge(author_id, count, now, now, "current"), warnings
    except (OSError, ValueError) as exc:
        warnings.append(f"Scholar unavailable: {type(exc).__name__}")

    cached = None
    try:
        cached = valid_saved_count(json.loads(cache_loader()), author_id)
        if cached is None:
            warnings.append("Published citation cache has no valid count for this author")
    except (OSError, ValueError) as exc:
        warnings.append(f"Published citation cache unavailable: {type(exc).__name__}")

    seeded = valid_saved_count(seed, author_id)
    if cached is not None:
        cached_time = verification_time(cached[1])
        seeded_time = verification_time(seeded[1]) if seeded is not None else None
        if cached_time is not None and seeded_time is not None and seeded_time > cached_time:
            count, checked_at = seeded
            return make_badge(author_id, count, checked_at, now, "seeded"), warnings
        count, checked_at = cached
        return make_badge(author_id, count, checked_at, now, "cached"), warnings
    if seeded is not None:
        count, checked_at = seeded
        return make_badge(author_id, count, checked_at, now, "seeded"), warnings
    warnings.append("No verified citation count is available; displaying an em dash")
    return make_badge(author_id, None, None, now, "unavailable"), warnings


def fetch_text(url, timeout):
    # No proxies, retries, CAPTCHA handling, credentials, or fingerprint changes.
    with urlopen(url, timeout=timeout) as response:
        data = response.read(2 * 1024 * 1024 + 1)
        if len(data) > 2 * 1024 * 1024:
            raise ValueError("Response exceeds the size limit")
        return data.decode(response.headers.get_content_charset() or "utf-8")


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--output", type=Path, default=Path("_site/assets/data/scholar.json"))
    cli.add_argument("--seed", type=Path, default=Path("_data/metrics.yml"),
                     help="JSON-compatible metrics file containing author_id and citations")
    cli.add_argument("--timeout", type=float, default=10,
                     help="Timeout per request in seconds, from 1 to 30 (default: 10)")
    args = cli.parse_args()
    if not 1 <= args.timeout <= 30:
        cli.error("--timeout must be between 1 and 30 seconds")

    try:
        seed = json.loads(args.seed.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        seed = None
        print("Citation seed is absent or invalid", file=sys.stderr)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    result, warnings = resolve_stats(
        AUTHOR_ID,
        lambda: fetch_text(f"https://scholar.google.com/citations?user={AUTHOR_ID}&hl=en", args.timeout),
        lambda: fetch_text(CACHE_URL, args.timeout),
        seed,
        now,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for warning in warnings:
        print(warning, file=sys.stderr)
    print(f"Citation badge written: {result['status']} ({result['message']})")


if __name__ == "__main__":
    main()
