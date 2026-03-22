import os
import re
import urllib.request
import urllib.parse
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(base_dir, 'index.html')

def search_youtube(query):
    try:
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query.encode('utf-8'))
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8')
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_\-]{11})"', html)
        if video_ids:
            return video_ids[0]
    except Exception as e:
        print(f"Error searching for {query}: {e}")
    return "jWk7N6-W4Yw"

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# For basicVerbs, basicPreps, phrasalVerbs, each item looks like:
# { name: "Make", nuance: "..."
# If it doesn't have videoId, add it.

# Let's find all occurrences of `{ name: "(.*?)", `
matches = re.finditer(r'\{\s*name:\s*"([^"]+)",', html)
for match in matches:
    name = match.group(1)
    # Check if this specific item block already has videoId
    # The block is from this match to the next ']' or next 'name:'
    # A safe way is to replace the exact matched string with one containing videoId if not present soon after.
    # Actually, we can just replace `{ name: "Make", ` with `{ name: "Make", videoId: "...", `
    
    # Let's check if the next 50 chars have videoId already
    start_idx = match.start()
    probe_area = html[start_idx:start_idx+150]
    
    # We only care about basic verbs, preps, phrasal verbs.
    # We'll skip adding if videoId is already there.
    if 'videoId:' not in probe_area:
        query = f"Learn English {name}"
        if len(name.split()) > 1: # Phrasal verb
            query = f"Learn English phrasal verb {name}"
        else: # basic prep or verb
            query = f"Learn English grammar {name}"
            
        print(f"Fetching for {name}...")
        vid = search_youtube(query)
        
        # Replace
        original_str = match.group(0) # e.g. { name: "Make",
        new_str = f'{{ name: "{name}", videoId: "{vid}",'
        html = html.replace(original_str, new_str, 1) # replace only this instance
        time.sleep(0.5)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("All missing videos added to tabs!")
