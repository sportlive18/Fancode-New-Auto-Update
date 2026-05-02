import urllib.request
import json
import sys
import os

def generate_m3u(data):
    """Generates M3U playlist content from the API data."""
    m3u_lines = ["#EXTM3U"]
    headers = data.get("headers", {})
    user_agent = headers.get("User-Agent", "")
    referer = headers.get("Referer", "")
    
    for match in data.get("matches", []):
        if match.get("type") == "live" and match.get("stream_url"):
            name = match.get("match", "Unknown Match")
            tournament = match.get("tournament", "")
            category = match.get("category", "")
            logo = match.get("image", "")
            url = match.get("stream_url")
            match_id = match.get("match_id", "")
            
            inf_line = f'#EXTINF:-1 tvg-id="{match_id}" tvg-logo="{logo}" group-title="{category}", {tournament}: {name}'
            m3u_lines.append(inf_line)
            
            if user_agent:
                m3u_lines.append(f'#EXTVLCOPT:http-user-agent={user_agent}')
            if referer:
                m3u_lines.append(f'#EXTVLCOPT:http-referrer={referer}')
                
            m3u_lines.append(url)
            
    return "\n".join(m3u_lines)

def main():
    url = "https://raw.githubusercontent.com/doctor-8trange/zyphx8/refs/heads/main/data/fancode.json"
    print(f"Fetching full Fancode JSON from {url}...")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')  # ✅ Fixed here
            data = json.loads(content)
            
        with open('sayan.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Successfully saved full JSON to sayan.json")

        m3u_content = generate_m3u(data)
        with open('fancode.m3u', 'w', encoding='utf-8') as f:
            f.write(m3u_content)
        print("Successfully saved M3U playlist to fancode.m3u")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
