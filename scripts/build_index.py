"""
index.html을 깔끔하게 재구성:
1. curriculum 객체 내부에 Month 2 (31-60) + Month 3 (61-90) 데이터를 삽입
2. 기존에 하드코딩된 Day 31 이후의 데이터나 외부에 주입된 블록을 제거
"""
import json
import re

import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
index_path = os.path.join(base_dir, 'index.html')

with open(os.path.join(data_dir, 'month2_data.json'), 'r', encoding='utf-8') as f:
    m2 = json.load(f)
with open(os.path.join(data_dir, 'month3_data.json'), 'r', encoding='utf-8') as f:
    m3 = json.load(f)

with open(index_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for_loop_line = -1
for i, line in enumerate(lines):
    if 'for(let i=9; i<=365; i++)' in line:
        for_loop_line = i
        break

assert for_loop_line != -1, "Could not find for loop"

curriculum_close_line = -1
for i in range(for_loop_line - 1, -1, -1):
    if lines[i].strip() == '};':
        curriculum_close_line = i
        break

assert curriculum_close_line != -1, "Could not find curriculum close line"

day_31_start = -1
for i in range(curriculum_close_line):
    if re.search(r',\s*31\s*:\s*\{', lines[i]) or lines[i].strip().startswith("31:"):
        day_31_start = i
        break

if day_31_start != -1:
    keep_before = lines[:day_31_start]
else:
    keep_before = lines[:curriculum_close_line]

def dict_to_js_entry(day_num, data):
    inner = json.dumps(data, ensure_ascii=False, indent=6)
    return f"    ,{day_num}: {inner}"

new_entries = []
for day_str in sorted(m2.keys(), key=int):
    new_entries.append(dict_to_js_entry(day_str, m2[day_str]))
for day_str in sorted(m3.keys(), key=int):
    new_entries.append(dict_to_js_entry(day_str, m3[day_str]))

insertion_block = "\n".join(new_entries) + "\n"

close_line = lines[curriculum_close_line]

keep_after_start = for_loop_line
while keep_after_start - 1 > curriculum_close_line and lines[keep_after_start - 1].strip() == '':
    keep_after_start -= 1

keep_after = lines[keep_after_start:]

new_lines = keep_before + [insertion_block] + [close_line, "\n"] + keep_after

with open(index_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\nSUCCESS: index.html rebuilt.")
print(f"  Total lines: {len(new_lines)}")
