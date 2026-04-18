import urllib.request
import re
import json

def parse_m3u(content):
    channels = []
    # Split content by lines, handling both \n and \r\n
    lines = content.splitlines()
    
    current_channel = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('#EXTINF'):
            # Extract attributes using regex
            # Example: #EXTINF:-1 tvg-id="id" tvg-logo="logo" group-title="group",Title
            
            logo_match = re.search(r'tvg-logo="([^"]*)"', line)
            group_match = re.search(r'group-title="([^"]*)"', line)
            # Find the last comma which usually precedes the name
            name_match = re.search(r',(.*)$', line)
            
            current_channel = {
                "name": name_match.group(1).strip() if name_match else "Unknown",
                "logo": logo_match.group(1).strip() if logo_match else "",
                "group": group_match.group(1).strip() if group_match else "",
            }
        elif not line.startswith('#'):
            # This should be the URL
            if current_channel:
                current_channel["url"] = line
                channels.append(current_channel)
                current_channel = {}
                
    return channels

def main():
    url = "https://fcapi.amitbala1993.workers.dev/"
    print(f"Fetching M3U from {url}...")
    
    try:
        # User-Agent may be required by some workers
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        channels = parse_m3u(content)
        
        with open('sayan.json', 'w', encoding='utf-8') as f:
            json.dump(channels, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully converted {len(channels)} channels to sayan.json")
    except Exception as e:
        print(f"Error occurred: {e}")
        # Exit with error to notify GitHub Actions if it fails
        exit(1)

if __name__ == "__main__":
    main()
