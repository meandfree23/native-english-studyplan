import os
import json
import re
import urllib.request
import urllib.parse
import time
import subprocess

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
index_path = os.path.join(base_dir, 'index.html')
build_script = os.path.join(base_dir, 'scripts', 'build_index.py')

def search_youtube(query):
    try:
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query.encode('utf-8'))
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8')
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_\-]{11})"', html)
        if video_ids:
            return video_ids[0]
    except Exception as e:
        print(f"Error searching for {query}: {e}")
    return "0I12mA0EejE"

# 1. Update JSON files (Day 31-90)
for month_file in ['month2_data.json', 'month3_data.json']:
    file_path = os.path.join(data_dir, month_file)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for day, content in data.items():
            title = content.get('title', f"Day {day}")
            query = f"Learn English {title}"
            vid = search_youtube(query)
            print(f"Day {day} -> {vid}")
            content['videoId'] = vid
            time.sleep(0.5)
            
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=6)

# 2. Update index.html (Day 1-30)
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Find Day 1 to 30 and replace videoId. 
for day_num in range(1, 31):
    # Match unquoted keys like: 1: { ... title: "..." }
    title_match = re.search(r'(?<![a-zA-Z0-9_\-])' + str(day_num) + r':\s*\{[^}]*?title:\s*"([^"]+)"', index_content)
    if title_match:
        title = title_match.group(1)
        query = f"Learn English {title}"
        vid = search_youtube(query)
        print(f"Day {day_num} -> {vid} (from HTML)")
        
        day_marker = f'{day_num}: {{'
        # Find exactly where this day marker starts
        match_idx = index_content.find(day_marker)
        if match_idx != -1:
            # isolate the block until the next day or closing brace
            parts = [index_content[:match_idx + len(day_marker)], index_content[match_idx + len(day_marker):]]
            block_end = parts[1].find('}')
            if block_end != -1:
                block = parts[1][:block_end]
                new_block = re.sub(r'videoId:\s*"[^"]+"', f'videoId: "{vid}"', block, count=1)
                parts[1] = new_block + parts[1][block_end:]
                index_content = "".join(parts)
        
        time.sleep(0.5)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_content)

print("Fetching complete! Rebuilding index...")
subprocess.run(['python3', build_script], cwd=base_dir)
