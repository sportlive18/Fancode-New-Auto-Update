import urllib.request
import json
import sys

def parse_fancode_json(content):
    try:
        data = json.loads(content)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return []

    channels = []
    
    # We take the live matches that have a stream_url
    # The source structure is {"matches": [...], ...}
    matches = data.get("matches", [])
    
    for item in matches:
        stream_url = item.get("stream_url")
        if stream_url:
            channels.append({
                "name": item.get("match", "Unknown"),
                "logo": item.get("image", ""),
                "group": item.get("tournament", ""),
                "url": stream_url
            })
                
    return channels

def main():
    url = "https://fcapi.amitbala1993.workers.dev/"
    print(f"Fetching Fancode JSON from {url}...")
    
    try:
        # User-Agent may be required by some workers
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        channels = parse_fancode_json(content)
        
        with open('sayan.json', 'w', encoding='utf-8') as f:
            json.dump(channels, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully converted {len(channels)} channels to sayan.json")
    except Exception as e:
        print(f"Error occurred: {e}")
        # Exit with error to notify GitHub Actions if it fails
        sys.exit(1)

if __name__ == "__main__":
    main()
