import urllib.request
import json
import sys

def main():
    url = "https://fcapi.amitbala1993.workers.dev/"
    print(f"Fetching full Fancode JSON from {url}...")
    
    try:
        # User-Agent may be required by some workers
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            data = json.loads(content)
            
        with open('sayan.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully saved full JSON to sayan.json")
    except Exception as e:
        print(f"Error occurred: {e}")
        # Exit with error to notify GitHub Actions if it fails
        sys.exit(1)

if __name__ == "__main__":
    main()
