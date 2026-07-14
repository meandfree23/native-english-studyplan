import os
import re
import time
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

topics = {
    9: "Advanced Particles (전치사/부사 심화)",
    10: "Business & Professional (비즈니스 및 전문 뉘앙스)",
    11: "Emotional Intelligence (감성 및 부드러운 화법)",
    12: "Native Collocations (원어민식 구동사 덩어리)"
}

def generate_curriculum_chunk(month, start, end):
    print(f"Generating curriculum chunk for Month {month}, Days {start}-{end}...")
    prompt = f"""
    You are an expert English teacher designing a curriculum for "Month {month}" focusing on: {topics[month]}.
    Generate a JSON object containing EXACTLY days {start} to {end}.
    For each day, provide the following structure EXACTLY:
    "{start}": {{
        "v": "💡",
        "vT": "(English Title)",
        "vD": "(Korean description)",
        "governing": "(Korean governing idea)",
        "core": "(The target expression/word)",
        "sentences": [
          {{
            "txt": "(English sentence)",
            "t": "(Korean translation)",
            "n": "(Nuance explanation)",
            "s": "(Situation)",
            "g": "M or F",
            "eT": "(Sub title)",
            "eD": "(Sub description)"
          }}
          // Generate EXACTLY 5 sentences per day covering different nuances of the core word.
        ],
        "category": "{topics[month]}",
        "title": "Day {start}. (Korean Title)",
        "sub": "(Korean Subtitle)"
    }}
    
    Output ONLY valid JSON format. Start with {{ and end with }}. Do NOT wrap in ```json or ```. Keep descriptions concise to save tokens.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4000
        )
        json_str = response.choices[0].message.content.strip()
        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]
        return json.loads(json_str)
    except Exception as e:
        print(f"Error generating chunk {start}-{end}: {e}")
        # Retry once
        time.sleep(2)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4000
        )
        json_str = response.choices[0].message.content.strip()
        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]
        return json.loads(json_str)

def generate_curriculum(month, start_day, end_day):
    full_data = {}
    for chunk_start in range(start_day, end_day + 1, 3):
        chunk_end = min(chunk_start + 2, end_day)
        chunk_data = generate_curriculum_chunk(month, chunk_start, chunk_end)
        full_data.update(chunk_data)
        time.sleep(1)
    return full_data

def generate_insights_for_month(month, data):
    print(f"Generating insights for Month {month}...")
    
    prompt_template = """
You are an expert English teacher. I need you to generate a deep-dive "Core Insight" article in HTML format for the English expression: "{expr}".
It MUST follow this exact HTML structure and class names.
DO NOT use Markdown block ticks. Output RAW HTML only.

Format:
<div class="insight-article">
    <div class="insight-intro">
        <strong>{expr}</strong>은 단순히 번역되는 뜻이 아닙니다.<br/>
        원어민에게 {expr}은 <strong>'이 표현의 가장 핵심적인 원어민 뉘앙스 요약'</strong>을 의미합니다.
    </div>

    <h2 class="insight-h2">{expr}의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>{expr}</strong>의 핵심은</p>
        <div class="quote-text">"가장 짧고 강렬한 본질적 의미"</div>
        <p>입니다. (여기에 짧은 추가 설명 1문장 추가)</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">핵심 뉘앙스 구조도 ({expr})</div>
        <pre>
 (여기에 이 표현의 뉘앙스를 보여주는 직관적이고 심플한 ASCII ART를 그려주세요. 5줄 이내)
        </pre>
        <div class="ascii-footer">(ASCII 아트 하단 설명 1줄)</div>
    </div>

    <h2 class="insight-h2">① (첫번째 구체적 뉘앙스 제목 한글+영어)</h2>
    <p class="insight-p">(첫번째 뉘앙스에 대한 설명 1문장)</p>
    <div class="example-group">
        <div class="ex-en">(예문 영어)</div>
        <div class="ex-ko">(예문 해석 + 괄호 안에 왜 이 표현이 쓰였는지 뉘앙스 해석)</div>
        <div class="ex-en" style="margin-top:12px;">(두번째 예문 영어)</div>
        <div class="ex-ko">(두번째 예문 해석 + 괄호 안 뉘앙스 해석)</div>
    </div>

    <h2 class="insight-h2">② (두번째 구체적 뉘앙스 제목 한글+영어)</h2>
    <p class="insight-p">(두번째 뉘앙스에 대한 설명 1문장)</p>
    <div class="example-group">
        <div class="ex-en">(예문 영어)</div>
        <div class="ex-ko">(예문 해석 + 괄호 안 뉘앙스 해석)</div>
        <div class="ex-en" style="margin-top:12px;">(두번째 예문 영어)</div>
        <div class="ex-ko">(두번째 예문 해석 + 괄호 안 뉘앙스 해석)</div>
    </div>

    <h2 class="insight-h2">③ (세번째 구체적 뉘앙스 제목 한글+영어)</h2>
    <p class="insight-p">(세번째 뉘앙스에 대한 설명 1문장)</p>
    <div class="example-group">
        <div class="ex-en">(예문 영어)</div>
        <div class="ex-ko">(예문 해석 + 괄호 안 뉘앙스 해석)</div>
        <div class="ex-en" style="margin-top:12px;">(두번째 예문 영어)</div>
        <div class="ex-ko">(두번째 예문 해석 + 괄호 안 뉘앙스 해석)</div>
    </div>
</div>

Constraints:
1. ONLY return the HTML code. Do not wrap in ```html or ```. 
2. The ASCII art must be plain text.
3. Keep explanations natural.
"""
    results = {}
    for day, day_data in data.items():
        expr = day_data['core']
        print(f"Generating insight for Day {day}: {expr}...")
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt_template.format(expr=expr)}],
                temperature=0.7,
                max_tokens=1500
            )
            html_content = response.choices[0].message.content.strip()
            if html_content.startswith("```html"):
                html_content = html_content[7:]
            if html_content.endswith("```"):
                html_content = html_content[:-3]
            
            results[expr] = html_content
            day_data['core_insight'] = expr
            time.sleep(1)
        except Exception as e:
            print(f"Error on {expr}: {e}")
            
    return results

def save_month(month, data):
    js_content = f"window.dayData = Object.assign(window.dayData || {{}}, {json.dumps(data, ensure_ascii=False, indent=2)});\n"
    with open(f'master/data/month{month}.js', 'w', encoding='utf-8') as f:
        f.write(js_content)

def append_insights(insights):
    with open('master/data/core_insights.js', 'r', encoding='utf-8') as f:
        core_insights = f.read()
    
    new_insights = ",\n"
    for expr, html in insights.items():
        escaped_html = html.replace('`', '\\`')
        new_insights += f'    "{expr}": `\n{escaped_html}\n`,\n'
    new_insights = new_insights.rstrip(',\n') + '\n};'
    
    core_insights = core_insights.replace('\n};', new_insights)
    with open('master/data/core_insights.js', 'w', encoding='utf-8') as f:
        f.write(core_insights)

months_config = [
    (9, 241, 270),
    (10, 271, 300),
    (11, 301, 330),
    (12, 331, 360)
]

for month, start, end in months_config:
    if os.path.exists(f'master/data/month{month}.js'):
        print(f"Month {month} already exists, skipping.")
        continue
    data = generate_curriculum(month, start, end)
    insights = generate_insights_for_month(month, data)
    save_month(month, data)
    append_insights(insights)

print("Finished ALL expressions for Months 9-12!")
