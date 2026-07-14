import re

with open('master/data/month1.js', 'r') as f:
    content = f.read()

days = re.findall(r'"(\d+)": \{(.*?)\n  \},?\n', content, flags=re.DOTALL)

for day_num, day_content in days:
    core_match = re.search(r'"core": "(.*?)"', day_content)
    core = core_match.group(1) if core_match else "Unknown"
    
    nuances = re.findall(r'"n": "(.*?)"', day_content)
    print(f"Day {day_num} [{core}]: {', '.join(nuances)}")
