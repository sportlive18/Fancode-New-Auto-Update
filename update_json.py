import urllib.request
import json
import sys

def generate_m3u(data):
    """Generates M3U playlist content from the API data."""
    m3u_lines = ["#EXTM3U"]
    headers = data.get("headers", {})
    user_agent = headers.get("User-Agent", "")
    referer = headers.get("Referer", "")

    for match in data.get("matches", []):
        # Filter: only LIVE/STARTED matches with a valid stream URL
        status = match.get("status", "")
        streaming_status = match.get("streamingStatus", "")
        cdn = match.get("STREAMING_CDN", {})
        stream_url = cdn.get("Primary_Playback_URL") if cdn else None

        if status != "LIVE" or streaming_status != "STARTED" or not stream_url:
            continue

        name = match.get("title", "Unknown Match")
        tournament = match.get("tournament", "")
        category = match.get("category", "")
        language = match.get("language", "")
        logo = match.get("image", "")
        match_id = match.get("match_id", "")
        is_drm = cdn.get("is_drm", False)

        # Label DRM streams so users know
        drm_tag = " [DRM]" if is_drm else ""
        label = f"{tournament}: {name} ({language}){drm_tag}"

        inf_line = f'#EXTINF:-1 tvg-id="{match_id}" tvg-logo="{logo}" group-title="{category}", {label}'
        m3u_lines.append(inf_line)

        if user_agent:
            m3u_lines.append(f'#EXTVLCOPT:http-user-agent={user_agent}')
        if referer:
            m3u_lines.append(f'#EXTVLCOPT:http-referrer={referer}')

        m3u_lines.append(stream_url)

    return "\n".join(m3u_lines)

def main():
    url = "https://raw.githubusercontent.com/doctor-8trange/zyphx8/refs/heads/main/data/fancode.json"
    print(f"Fetching Fancode JSON from {url}...")

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            data = json.loads(content)

        with open('sayan.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Saved full JSON to sayan.json")

        m3u_content = generate_m3u(data)
        with open('fancode.m3u', 'w', encoding='utf-8') as f:
            f.write(m3u_content)
        print("Saved M3U playlist to fancode.m3u")

    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
