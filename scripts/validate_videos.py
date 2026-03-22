import os
import json
import re
import urllib.request
import urllib.error
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
index_path = os.path.join(base_dir, 'index.html')
build_script = os.path.join(base_dir, 'scripts', 'build_index.py')

FALLBACK_VID = 'aJSYRhj04NY' # Known reliable video

def is_video_valid(vid):
    """Check if video is valid and embeddable using YouTube oEmbed."""
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        urllib.request.urlopen(req)
        return True # 200 OK
    except urllib.error.HTTPError as e:
        # 401 = Unauthorized (Embedding disabled)
        # 404 = Not found (Deleted/Private)
        print(f"[{vid}] Failed with status: {e.code}")
        return False
    except Exception as e:
        print(f"[{vid}] Error checking: {e}")
        return False

print("Validating month2_data.json...")
m2_path = os.path.join(data_dir, 'month2_data.json')
if os.path.exists(m2_path):
    with open(m2_path, 'r', encoding='utf-8') as f:
        m2 = json.load(f)
    for k, v in m2.items():
        if 'videoId' in v:
            if not is_video_valid(v['videoId']):
                print(f"Replacing invalid video {v['videoId']} on Day {k}")
                v['videoId'] = FALLBACK_VID
            time.sleep(0.1)
    with open(m2_path, 'w', encoding='utf-8') as f:
        json.dump(m2, f, ensure_ascii=False, indent=6)

print("Validating month3_data.json...")
m3_path = os.path.join(data_dir, 'month3_data.json')
if os.path.exists(m3_path):
    with open(m3_path, 'r', encoding='utf-8') as f:
        m3 = json.load(f)
    for k, v in m3.items():
        if 'videoId' in v:
            if not is_video_valid(v['videoId']):
                print(f"Replacing invalid video {v['videoId']} on Day {k}")
                v['videoId'] = FALLBACK_VID
            time.sleep(0.1)
    with open(m3_path, 'w', encoding='utf-8') as f:
        json.dump(m3, f, ensure_ascii=False, indent=6)

print("Validating index.html...")
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Using regex to find all "videoId": "..." or videoId: "..." occurrences.
# Be careful not to replace placeholders like ${data.videoId}
all_vids = set(re.findall(r'videoId["\s:]+"([a-zA-Z0-9_\-]{11})"', html))
for vid in all_vids:
    if not is_video_valid(vid):
        print(f"Replacing invalid video {vid} in index.html")
        html = html.replace(vid, FALLBACK_VID)
    time.sleep(0.1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Validation complete. Rebuilding...")
os.system(f'python3 {build_script}')
