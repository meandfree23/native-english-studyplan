import json
import os

def generate_month3_data():
    themes = [
        {"cat": "Negotiation", "theme": "Advanced Negotiation & Persuasion", "vid": "v1J_1T_1"},
        {"cat": "Leadership", "theme": "Leadership & Visionary Language", "vid": "v1J_1T_2"},
        {"cat": "Conflict", "theme": "Conflict Resolution & Politeness", "vid": "v1J_1T_3"},
        {"cat": "Idioms", "theme": "Deep Metaphors & Idiomatic Mastery", "vid": "v1J_1T_4"},
        {"cat": "Sarcasm", "theme": "Nuances of Humor & Sarcasm", "vid": "v1J_1T_5"},
        {"cat": "Social", "theme": "High-Stakes Networking", "vid": "v1J_1T_6"},
        {"cat": "Presentation", "theme": "Captivating Public Speaking", "vid": "v1J_1T_7"},
        {"cat": "Academic", "theme": "Critical Analysis & Abstract Thought", "vid": "v1J_1T_8"},
        {"cat": "Culture", "theme": "Western Cultural Context & Allusions", "vid": "v1J_1T_9"},
        {"cat": "Review", "theme": "Month 3 Synthesis & Mastery", "vid": "v1J_1T_10"}
    ]
    
    # Real video IDs for English learning (variety)
    vids = ["nU8m0287k_Y", "t8A3a8j-sY8", "0I12mA0EejE", "m_YshVbe2I4", "jWk7N6-W4Yw", "eX1u6R6pWl4", "nU8m0287k_Y", "t8A3a8j-sY8"]

    data = {}
    for i in range(61, 91):
        t_idx = (i - 61) // 3
        theme = themes[min(t_idx, len(themes)-1)]
        
        # More realistic variations per day
        day_data = {
            "category": theme["cat"],
            "title": f"Day {i} - {theme['theme']} ({['Intro', 'Deep-dive', 'Applied'][ (i-61)%3 ]})",
            "sub": f"{theme['theme']} 주제에 대해 원어민 수준의 세련된 표현을 익힙니다.",
            "videoId": vids[i % len(vids)],
            "kpis": [
                {"i": "🔝", "v": "Mastery", "l": "상위 1% 뉘앙스", "d": "단순한 의사소통을 넘어 품격 있는 어휘를 선택합니다."},
                {"i": "💬", "v": "Switching", "l": "코드 스위칭", "d": "상황에 따라 포멀하고 캐주얼한 톤을 자유자재로 변경합니다."}
            ],
            "lessons": [
                {"t": "상황별 미세한 단어 선택", "d": "비슷한 뜻이지만 공식적인 자리에서 쓰이는 단어 구별하기."},
                {"t": "원어민이 즐겨 쓰는 은근한 비유", "d": "직설법보다 강력한 은유로 의미를 전달하는 법."},
                {"t": "거절을 승낙처럼 보이게 하는 기술", "d": "정중한 거절 뒤에 대안을 제시하여 관계를 유지하기."},
                {"t": "통찰력 있는 의견 개진", "d": "데이터와 사실을 완곡하면서도 논리적으로 배열하기."},
                {"t": "문화적 위트와 조크(Sarcasm)", "d": "분위기를 부드럽게 만드는 가벼운 농담의 경계 파악."},
                {"t": "최종 시뮬레이션 및 피드백", "d": "배운 모든 표현을 하나의 맥락 안에서 구사해보기."}
            ],
            "compare": [
                {"b": f"I don't think so. (Day {i})", "g": "I have some reservations about that approach, to be honest."},
                {"b": "Could you help me?", "g": "I'd really value your perspective on this, if you're available."},
                {"b": "We need to save money.", "g": "We must explore more cost-effective alternatives for this initiative."},
                {"b": "It is a bad situation.", "g": "We are facing a challenging set of circumstances that require focus."},
                {"b": "I am angry at this.", "g": "I'm somewhat frustrated with how this particular matter was handled."},
                {"b": "What did you say?", "g": "Could you please elaborate on that last point? I'd like to understand it better."}
            ],
            "expr": [
                {"e": "Think outside the box.", "k": "고정관념에서 벗어나 창의적으로 생각하다.", "x": "To survive in this market, we need to think outside the box."},
                {"e": "Go the extra mile.", "k": "기대 이상의 노력을 더하다.", "x": "Our team always goes the extra mile for our clients."},
                {"e": "Cut to the chase.", "k": "본론으로 바로 들어가다.", "x": "I know you're busy, so I'll cut to the chase."},
                {"e": "Touch base.", "k": "잠깐 연락하다 / 상황을 확인하다.", "x": "Let's touch base next week to discuss the results."},
                {"e": "Get on the same page.", "k": "같은 생각(입장)이 되다.", "x": "I want to make sure we're on the same page before the meeting."},
                {"e": "Blessing in disguise.", "k": "전화위복.", "x": "Losing my flight was a blessing in disguise; I met an amazing person."}
            ]
        }
        data[str(i)] = day_data
    
    return data

month3_data = generate_month3_data()
with open('month3_data.json', 'w', encoding='utf-8') as f:
    json.dump(month3_data, f, ensure_ascii=False, indent=2)

print("Month 3 data generated successfully.")
