import urllib.request
import json
import sys

def main():
    url = "https://fcapi.amitbala1993.workers.dev/"
    print(f"Fetching data from {url}...")
    
    try:
        # User-Agent may be required by some workers
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            source_data = json.loads(response.read().decode('utf-8'))
            
        channels = []
        
        # Process live matches
        matches = source_data.get('matches', [])
        if not matches:
            print("No live matches found in 'matches' key.")
        
        for match in matches:
            channel_name = f"{match.get('tournament', '')} - {match.get('match', '')}".strip()
            if not channel_name:
                channel_name = "Unknown Live Match"
                
            channel = {
                "name": channel_name,
                "logo": match.get('image', ''),
                "group": match.get('category', 'Live'),
                "url": match.get('stream_url', '')
            }
            
            # Fallback to resolutions if stream_url is missing
            if not channel["url"] and match.get('all_resolutions'):
                res = match.get('all_resolutions')
                # Prioritize 1080p, then 720p, then any
                channel["url"] = res.get('1080p') or res.get('720p') or next(iter(res.values()), '')
            
            if channel["url"]:
                channels.append(channel)

        # Process upcoming matches (optional)
        upcoming = source_data.get('upcoming_matches', [])
        for match in upcoming:
            # Upcoming matches usually don't have stream_url yet
            if match.get('stream_url'):
                channel_name = f"{match.get('tournament', '')} - {match.get('match', '')}".strip()
                channels.append({
                    "name": channel_name or "Upcoming Match",
                    "logo": match.get('image', ''),
                    "group": match.get('category', 'Upcoming'),
                    "url": match.get('stream_url', '')
                })

        # Save to sayan.json
        with open('sayan.json', 'w', encoding='utf-8') as f:
            json.dump(channels, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully converted {len(channels)} channels to sayan.json")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
