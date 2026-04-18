import urllib.request
import json
import sys

def main():
    url = "https://fcapi.amitbala1993.workers.dev/"
    print(f"Fetching raw data from {url}...")
    
    try:
        # User-Agent headers to ensure the fetch works
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            source_data = json.loads(response.read().decode('utf-8'))
            
        # Save the entire JSON object to sayan.json with pretty-print formatting
        with open('sayan.json', 'w', encoding='utf-8') as f:
            json.dump(source_data, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully saved the entire JSON response to sayan.json")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
