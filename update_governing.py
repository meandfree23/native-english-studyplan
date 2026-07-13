import re

# Dictionary mapping day numbers (as strings) to their new insightful, easy-to-understand titles
new_titles = {
    "1": "결정, 시간, 공간: 내 몫을 가장 확실하게 챙기는 기본 감각",
    "2": "숨결부터 리스크까지: 눈에 보이지 않는 것들마저 내 안으로 거두어들이다",
    "3": "신체와 시선의 통제: 대상을 억지로 이동시키거나 타인의 시선을 꽉 붙잡는 적극성",
    "4": "말과 시간의 캡처: 속절없이 흘러가는 시간과 뱉어진 말을 내 것으로 낚아채다",
    "5": "에너지와 주도권: 남의 자원을 뺏거나 꼬여가는 상황의 주도권을 내 손아귀에 쥐다",
    "6": "분리와 획득: 붙어있는 것을 떼어내거나(Off), 우연히 스쳐가는 기회를 낚아채다",
    "7": "역할과 정보의 이식: 무거운 책임, 순서, 혹은 눈에 안 보이는 프라이드까지 내 안으로 흡수",
    
    "8": "물리적 공간과 인지 상태의 이동: 밖으로 나가거나, 늦어지거나, 깨달음이 머리에 들어오다",
    "9": "새로운 궤도에 진입: 일자리를 얻거나, 차에 타거나, 타인을 설득해 억지로 움직이게 만들다",
    "10": "중력과 감정의 토글: 누운 상태에서 일어나거나(Up), 궤도를 틀거나, 분노 스위치가 켜지다",
    "11": "목적지에 꽂히다: 쓸데없는 말은 빼고 핵심에 닿거나, 완전히 분실 상태로 전환되다",
    "12": "변화의 흐름 타기: 나이가 들거나, 뒤로 물리거나, 데이터와 휴식이라는 무형의 가치를 흡수하다",
    "13": "모이고 스치고 입다: 흩어진 것들이 한 곳에 모이거나, 옷을 몸에 두르거나, 좁은 틈을 간신히 통과하다",
    "14": "다시 내 손안으로: 잃어버린 통제력을 되찾거나, 결혼 같은 새로운 신분 스티커를 획득하다",
    "15": "선점과 전이: 남들보다 앞선 좌표를 차지하거나, 바이러스에 감염되듯 무언가가 내 몸에 닿다",
    
    "16": "자산과 책임의 보관: 아이디어를 뇌에 담거나, 가야 한다는 묵직한 의무를 등 뒤에 짊어지다",
    "17": "시간과 멘탈의 점유: 식사 일정을 내 시간표에 박아두거나, 눈에 안 보이는 단단한 멘탈을 쥐고 있다",
    "18": "내부 시스템에 머금기: 바이러스, 고통, 혹은 그녀의 단단한 논리적 뼈대를 내 시스템 안에 품고 있다",
    "19": "과거의 기록과 현재의 용량: 만남의 기록이 유지되거나, 내 두 손의 통제 용량이 꽉 차버린 상태",
    "20": "유지되는 서비스와 감정: 돈을 주고 정기 서비스를 지속하거나, 짧게 터지는 분노 모듈을 기본 탑재하다",
    "21": "견고한 실드와 통제망: 조급함을 누르는 방어막을 켜두거나, 모든 변수를 내 통제망 아래에 꽉 쥐고 있다",
    "22": "체질과 옵션의 한계: 내 선택지에 남은 옵션이 없거나, 특정한 체질 자체를 선천적으로 유지하고 있다",
    
    "23": "새로운 결과값의 조립: 무기력한 상태에서 치명적 버그를 만들거나, 억지로 얼굴 근육을 당겨 웃음을 빚어내다",
    "24": "파편의 융합과 맹세: 흩어진 정보 조각을 모아 완벽한 논리로 조립하거나, 굳게 결심을 다지다",
    "25": "환경과 자금의 파생: 막대한 자금 덩어리를 뭉쳐내거나, 막힌 길을 부수어 억지로 지나갈 틈을 만들어내다",
    "26": "땀방울과 자본의 생산: 멈춰있던 근육을 돌려 땀을 빚어내거나, 모자란 예산의 양 끝을 억지로 당겨 꿰매다",
    "27": "극한의 압축과 도출: 노이즈 속에서 의미를 빼내거나, 자본과 시간에서 효율을 극한까지 쥐어짜다",
    "28": "세팅과 어그러짐: 황당한 장면을 새롭게 세팅하거나, 멀쩡한 변수를 꼬아버려 엉망진창으로 만들어버리다",
    "29": "강제적 변환과 우회 트랙: 평범한 기질을 강사로 빚어내거나, 단 한 번의 예외 트랙을 시스템에 몰래 건설하다",
    "30": "확률의 빚어냄과 세팅: 비어있는 확률 공간에 새로운 가정을 세우거나, 단절된 양극단 사이에 억지로 다리를 놓다"
}

def update_month1():
    with open('master/data/month1.js', 'r', encoding='utf-8') as f:
        content = f.read()

    def replacer(match):
        day = match.group(1)
        core_info = match.group(2)
        old_title = match.group(3)
        
        if day in new_titles:
            new_title = new_titles[day]
            # Replace the old title with the new profoundly crafted title
            return f'"governing": "{new_title}"'
        return match.group(0)

    # Regex to capture "governing": "Day X: [Core] Description"
    pattern = r'"governing": "(Day (\d+): \[[^\]]+\] [^"]+)"'
    
    # Wait, the governing field right now is e.g. "governing": "Day 1: [Take] 외부의 대상을 내 의지로 거머쥐다"
    # I want to replace the whole string value with the new title.
    # The current value has "Day X: [Core] " prefix which my javascript regex `replace(/Day \d+: \[[^\]]+\] /, '')` removes.
    # Since my UI already relies on that prefix being stripped OR just shows whatever is there...
    # WAIT! If I completely replace it with "결정, 시간, 공간: 내 몫을 가장 확실하게 챙기는 기본 감각", 
    # my JS regex `data.governing.replace(/Day \d+: \[[^\]]+\] /, '')` will just not match, and return the string as is!
    # That is perfectly fine and backwards compatible!
    # BUT, wait! Does any other part of the app rely on `data.governing` having the `Day X: [Core] ` prefix?
    # Actually, in `test_puppeteer.js` or `index.html`?
    # It's cleaner if I just replace the string entirely! Let's do that.

    # Revised replacer:
    def replacer_v2(match):
        prefix_day_match = re.search(r'"(\d+)": \{', content[:match.start()][::-1])
        if prefix_day_match:
            day = prefix_day_match.group(1)[::-1]
            if day in new_titles:
                return f'"governing": "{new_titles[day]}"'
        return match.group(0)
    
    # Let's do it day by day safely
    days = re.split(r'("\d+": \{)', content)
    
    out = []
    current_day = None
    for chunk in days:
        m = re.match(r'"(\d+)": \{', chunk)
        if m:
            current_day = m.group(1)
            out.append(chunk)
        else:
            if current_day and current_day in new_titles:
                # Replace the governing field in this chunk
                chunk = re.sub(r'"governing": "[^"]+"', f'"governing": "{new_titles[current_day]}"', chunk, count=1)
            out.append(chunk)
            
    with open('master/data/month1.js', 'w', encoding='utf-8') as f:
        f.write("".join(out))
        
if __name__ == "__main__":
    update_month1()
