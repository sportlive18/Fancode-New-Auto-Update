#!/usr/bin/env python3

import sys
import json
import requests
from urllib.parse import urlparse

DEFAULT_JSON_URL = "https://allinonereborn2.online/fctest/json/fancode_latest.json"
DEFAULT_OUTPUT = "fancode4.m3u"

LANG_CODE = {
    "HINDI": "HIN",
    "PUNJABI": "PUN",
    "BHOJPURI": "BHO",
    "ENGLISH": "ENG",
}

REFERRER = "https://allinonereborn2.online"


def get_lang_code(lang):
    return LANG_CODE.get(lang.upper(), lang[:3].upper())


def convert_json_to_m3u(data, add_headers=False):
    lines = ["#EXTM3U"]
    for match in data.get("matches", []):
        if match.get("status") != "LIVE":
            continue
        match_id = match.get("match_id")
        title = match.get("title", "Unknown Match")
        logo = match.get("image", "")
        category = match.get("category", "Cricket")
        for stream in match.get("streams", []):
            lang = stream.get("language", "Unknown")
            url = stream.get("playlist_url", "")
            if not url:
                continue
            lang_code = get_lang_code(lang)
            display_title = f"{lang_code} | {title}"
            extinf = (
                f'#EXTINF:-1 tvg-id="{match_id}" '
                f'tvg-name="{title} ({lang})" '
                f'tvg-logo="{logo}" '
                f'tvg-language="{lang}" '
                f'group-title="{category}",{display_title}'
            )
            lines.append(extinf)
            if add_headers:
                lines.append(f"#EXTVLCOPT:http-referrer={REFERRER}")
            lines.append(url)
    return "\n".join(lines)


def load_json(source):
    parsed = urlparse(source)
    if parsed.scheme in ("http", "https"):
        resp = requests.get(source, timeout=10)
        resp.raise_for_status()
        return resp.json()
    else:
        with open(source, "r", encoding="utf-8") as f:
            return json.load(f)


def main():
    source = DEFAULT_JSON_URL
    output_file = DEFAULT_OUTPUT
    add_headers = False

    args = sys.argv[1:]
    if "--add-headers" in args:
        add_headers = True
        args.remove("--add-headers")
    if len(args) >= 1:
        source = args[0]
    if len(args) >= 2:
        output_file = args[1]

    data = load_json(source)
    m3u_content = convert_json_to_m3u(data, add_headers)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"Playlist written to {output_file}")


if __name__ == "__main__":
    main()
