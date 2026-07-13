import json
import re

def main():
    file_path = "index.html"
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update Typography & Padding (Density/Textbook look)
    if "letter-spacing: -0.02em;" not in html:
        html = html.replace("body {", "body {\n      letter-spacing: -0.02em;\n      line-height: 1.45;")
    html = html.replace("padding: 25px;", "padding: 16px 20px;")
    html = html.replace("margin-bottom: 15px;", "margin-bottom: 12px;")

    # 2. Extract and replace JS curriculum
    # The curriculum structure needs to match Lesson 1 to Lesson 12
    lesson_data = {
        "1": {
            "title": "Lesson 1: 핵심 시제와 문장 구조",
            "desc": "영어 문장의 주어와 동사, 그리고 기본 시제를 마스터합니다.",
            "topics": [
                {
                    "title": "주격대명사", "desc": "주인공 지정하기",
                    "essence": "문장의 중심이 되는 주인공(주체)을 명확하게 선언합니다.",
                    "neural": "나(I) / 너(You) / 우리(We) / 그들(They)",
                    "sentences": [
                        {"en": "I am fully prepared.", "ko": "나는 완벽히 준비되었다.", "nu": "나(I)를 문장의 주체로 내세우며 확신을 표현합니다."},
                        {"en": "You have a point.", "ko": "네 말이 맞아 (일리가 있어).", "nu": "상대방(You)을 주어로 두어 의견을 존중합니다."},
                        {"en": "They are arriving soon.", "ko": "그들이 곧 도착할 거야.", "nu": "나와 너를 제외한 제3자(They)의 상태를 지칭합니다."}
                    ]
                },
                {
                    "title": "be동사", "desc": "존재와 상태 표현",
                    "essence": "동작이 아닌, 주어의 신분, 위치, 상태라는 '존재' 자체를 나타냅니다.",
                    "neural": "상태(State) & 위치(Location)",
                    "sentences": [
                        {"en": "I am deeply grateful.", "ko": "정말 깊이 감사드립니다.", "nu": "내 마음의 상태가 '감사함'에 있음을 나타냅니다."},
                        {"en": "The meeting is at 3 PM.", "ko": "회의는 오후 3시입니다.", "nu": "회의라는 이벤트가 위치한 시간적 '존재'를 말합니다."},
                        {"en": "She is in charge here.", "ko": "이곳 책임자는 그녀입니다.", "nu": "그녀의 현재 신분이나 역할(상태)을 선언합니다."}
                    ]
                },
                {
                    "title": "be동사 현재시제", "desc": "지금의 팩트",
                    "essence": "과거나 미래가 아닌, 바로 지금 이 순간 유효한 사실을 전달합니다.",
                    "neural": "현재 시점의 확정적 상태",
                    "sentences": [
                        {"en": "It is quite cold today.", "ko": "오늘은 꽤 춥네요.", "nu": "현재 날씨 상태(It is)를 팩트로 전달합니다."},
                        {"en": "We are ready to start.", "ko": "시작할 준비가 되었습니다.", "nu": "우리의 현재 텐션(Are)이 준비된 상태임을 보여줍니다."}
                    ]
                },
                {
                    "title": "현재시제", "desc": "변하지 않는 일상",
                    "essence": "지금 진행 중인 동작이 아니라, 어제도 오늘도 내일도 반복되는 '루틴'이나 '진리'를 뜻합니다.",
                    "neural": "반복(Routine) & 영속성",
                    "sentences": [
                        {"en": "I usually drink coffee.", "ko": "난 주로 커피를 마셔.", "nu": "지금 마시고 있다는 뜻이 아니라 매일 반복되는 나의 '습관'입니다."},
                        {"en": "The sun rises in the east.", "ko": "해는 동쪽에서 뜬다.", "nu": "예외 없이 항상 일어나는 자연의 법칙(진리)입니다."}
                    ]
                },
                {
                    "title": "현재시제 3인칭 단수", "desc": "동사에 -s 붙이기",
                    "essence": "주인공이 '나'도 '너'도 아닌 '한 명'일 때 동사에 -s를 붙이는 강한 규칙입니다.",
                    "neural": "제3자 단수의 구별",
                    "sentences": [
                        {"en": "He works very hard.", "ko": "그는 정말 열심히 일해요.", "nu": "주어(He)가 3인칭 단수이므로 work 뒤에 s를 강하게 붙입니다."},
                        {"en": "She always forgets my name.", "ko": "그녀는 항상 내 이름을 깜빡해.", "nu": "그녀(She)의 반복되는 습관을 말할 때 동사(forgets)의 형태를 바꿉니다."}
                    ]
                },
                {
                    "title": "be동사 과거시제", "desc": "과거의 상태",
                    "essence": "지금은 아닐 수 있지만, 과거 어느 시점에는 '존재'했던 상태를 묘사합니다.",
                    "neural": "과거로의 시선 이동 (was/were)",
                    "sentences": [
                        {"en": "I was totally exhausted.", "ko": "나 완전 기진맥진했었어.", "nu": "과거 그 순간의 나의 극심한 피로 상태(was)를 말합니다."},
                        {"en": "They were at the library.", "ko": "그들은 도서관에 있었어.", "nu": "그들이 과거 특정 시점에 존재했던 장소(were)를 나타냅니다."}
                    ]
                },
                {
                    "title": "과거시제", "desc": "이미 끝난 동작",
                    "essence": "현재와는 아무런 연관 없이, 과거에 이미 완벽하게 종료된 사건을 말합니다.",
                    "neural": "단절된 과거의 팩트",
                    "sentences": [
                        {"en": "I finished the project yesterday.", "ko": "나 어제 그 프로젝트 끝냈어.", "nu": "어제(yesterday)라는 명확한 과거 시점에 행동이 완료되었음을 선언합니다."},
                        {"en": "We met 10 years ago.", "ko": "우린 10년 전에 만났어.", "nu": "현재와 상관없이 10년 전이라는 시점에 일어났던 사실입니다."}
                    ]
                },
                {
                    "title": "의문사", "desc": "구체적인 정보 묻기",
                    "essence": "단순히 Yes/No 대답이 아니라 누가, 언제, 어디서 등 구체적이고 디테일한 정보를 캐물을 때 씁니다.",
                    "neural": "정보 요구 (Who, What, Where...)",
                    "sentences": [
                        {"en": "Where did you find this?", "ko": "이거 어디서 찾았어?", "nu": "가장 궁금한 정보인 '장소(Where)'를 문장 맨 앞에 두어 강하게 묻습니다."},
                        {"en": "How can I help you?", "ko": "어떻게 도와드릴까요?", "nu": "돕는 방법(How)을 묻는 가장 정중하고 흔한 패턴입니다."}
                    ]
                },
                {
                    "title": "문장의 순서", "desc": "영어의 어순 감각",
                    "essence": "누가 ➔ 무엇을 했다 ➔ 누구에게 ➔ 어디서 ➔ 언제 순으로 에너지가 뻗어 나가는 원리입니다.",
                    "neural": "주체 ➔ 행동 ➔ 대상 ➔ 배경",
                    "sentences": [
                        {"en": "I sent him an email this morning.", "ko": "오늘 아침에 그에게 이메일을 보냈어.", "nu": "나(I) ➔ 보냈다(sent) ➔ 그에게(him) ➔ 이메일을 ➔ 언제 순으로 흐름이 이어집니다."}
                    ]
                },
                {
                    "title": "명령문", "desc": "행동 촉구하기",
                    "essence": "주어를 생략하고 동사부터 던져서 상대방에게 빠르고 직접적으로 행동을 요청하거나 지시합니다.",
                    "neural": "주어 생략 ➔ 즉각적 액션",
                    "sentences": [
                        {"en": "Please let me know.", "ko": "제게 알려주세요.", "nu": "You를 생략하고 Let으로 바로 시작하여 행동을 유도하되, Please로 정중함을 더합니다."},
                        {"en": "Don't worry about it.", "ko": "그거 걱정하지 마.", "nu": "부정 명령(Don't)으로 상대방의 불필요한 감정 소모를 즉시 차단합니다."}
                    ]
                }
            ]
        },
        "2": {
            "title": "Lesson 2: 명사와 소유",
            "desc": "물건의 주인을 명확히 하고 명사를 셀 수 있는지 구별합니다.",
            "topics": [
                {
                    "title": "소유격 대명사·형용사", "desc": "나의 것, 너의 것",
                    "essence": "이 대상이 누구의 소유인지(my, your, his 등)를 직관적으로 밝힙니다.",
                    "neural": "소유의 경계 설정",
                    "sentences": [
                        {"en": "That is my final offer.", "ko": "그게 제 최종 제안입니다.", "nu": "이 제안이 '나의(my)' 것임을 강조합니다."},
                        {"en": "Is this your belongings?", "ko": "이거 당신 소지품인가요?", "nu": "대상(belongings)의 주인이 '당신(your)'인지 확인합니다."}
                    ]
                },
                {
                    "title": "소유격 (Nouns + 's)", "desc": "명사의 소유",
                    "essence": "특정 인물이나 명사 뒤에 's를 붙여 그 대상이 소유하고 있음을 명확히 합니다.",
                    "neural": "구체적인 소유주 지목",
                    "sentences": [
                        {"en": "This is John's responsibility.", "ko": "이건 존의 책임입니다.", "nu": "책임의 소재가 정확히 John에게 있음을 's로 표시합니다."}
                    ]
                },
                {
                    "title": "복수형 (Plurals)", "desc": "여럿일 때 -s 붙이기",
                    "essence": "대상이 두 개 이상일 때 명사 끝에 -s를 붙여 집단을 표현합니다.",
                    "neural": "수량의 확장",
                    "sentences": [
                        {"en": "I need three tickets.", "ko": "티켓 세 장이 필요합니다.", "nu": "티켓이 한 장이 아님을 분명히 밝힙니다."}
                    ]
                }
            ]
        },
        "3": { "title": "Lesson 3: 다양한 시제", "desc": "현재, 과거, 미래와 완료 시제까지 시간을 자유롭게 다룹니다.", "topics": [
            {"title": "현재진행시제", "desc": "지금 이 순간", "essence": "말하는 바로 지금 이 순간 동작이 진행되고 있음을 나타냅니다.", "neural": "역동적인 현재", "sentences": [{"en": "I am working right now.", "ko": "저 지금 일하는 중이에요.", "nu": "현재 행위에 완전히 몰입해 있음을 표현합니다."}]}
        ]},
        "4": { "title": "Lesson 4: 형용사와 비교", "desc": "대상을 꾸며주고 다른 것과 비교하여 차이를 드러냅니다.", "topics": [
            {"title": "형용사", "desc": "명사 화장하기", "essence": "명사의 상태, 성질, 크기 등을 디테일하게 설명해 줍니다.", "neural": "디테일 추가", "sentences": [{"en": "It was a brilliant idea.", "ko": "정말 기발한 아이디어였어.", "nu": "아이디어에 '기발함'이라는 색깔을 입힙니다."}]}
        ]},
        "5": { "title": "Lesson 5: 부사와 전치사", "desc": "장소, 시간, 방법 등 구체적인 배경을 설명합니다.", "topics": [
            {"title": "장소 전치사", "desc": "위치 감각", "essence": "in, on, at 등을 통해 대상이 공간 안에서 어디에 위치하는지 그립니다.", "neural": "공간 맵핑", "sentences": [{"en": "I left it on the desk.", "ko": "책상 위에 뒀어.", "nu": "표면에 접촉해 있는 'on'의 뉘앙스를 살립니다."}]}
        ]},
        "6": { "title": "Lesson 6: 부정사와 동명사", "desc": "동사를 변형하여 문장 안에서 명사처럼 자유롭게 활용합니다.", "topics": [
            {"title": "동명사", "desc": "동사를 명사로", "essence": "동사에 -ing를 붙여 '~하는 것'이라는 과거/현재 지향적 느낌을 줍니다.", "neural": "경험적 사실", "sentences": [{"en": "I enjoy playing tennis.", "ko": "나는 테니스 치는 것을 즐겨.", "nu": "이미 해본 경험(playing)을 즐긴다는 뉘앙스입니다."}]}
        ]},
        "7": { "title": "Lesson 7: 조동사", "desc": "동사에 뉘앙스를 입혀 감정과 태도를 전달합니다.", "topics": [
            {"title": "Modals", "desc": "능력, 추측, 의무", "essence": "단순한 팩트가 아니라 말하는 사람의 의도나 확률을 동사에 덧입힙니다.", "neural": "화자의 태도", "sentences": [{"en": "You must be tired.", "ko": "너 분명 피곤할 거야.", "nu": "강한 확신(must)을 담아 상대의 상태를 추측합니다."}]}
        ]},
        "8": { "title": "Lesson 8: 조건문", "desc": "만약 ~라면, 상황을 가정하여 결과를 예측합니다.", "topics": [
            {"title": "Conditionals", "desc": "가정과 상상", "essence": "If를 사용해 실제 일어나지 않은 일이나 미래의 가능성을 시뮬레이션합니다.", "neural": "가상 현실 세팅", "sentences": [{"en": "If I were you, I wouldn't do it.", "ko": "내가 너라면 안 그럴 텐데.", "nu": "현재 사실과 반대되는 가정을 세워 조언합니다."}]}
        ]},
        "9": { "title": "Lesson 9: 시간과 날짜", "desc": "정확한 시간, 요일, 날짜를 말하는 감각을 익힙니다.", "topics": [
            {"title": "시간과 날짜 표현", "desc": "정확한 타이밍", "essence": "시간 앞에는 at, 요일 앞에는 on, 달 앞에는 in을 쓰는 감각을 체화합니다.", "neural": "시간의 단위 확장", "sentences": [{"en": "Let's meet on Monday.", "ko": "월요일에 만나자.", "nu": "하루 단위의 시간 앞에는 on을 붙입니다."}]}
        ]},
        "10": { "title": "Lesson 10: 일상 어휘", "desc": "가족, 직업, 감각 등 우리 주변의 필수 단어들입니다.", "topics": [
            {"title": "The 5 Senses", "desc": "오감 표현", "essence": "시각, 청각, 후각, 미각, 촉각을 통해 세상을 인지하는 동사들입니다.", "neural": "감각의 수용", "sentences": [{"en": "It sounds great.", "ko": "그거 좋게 들리네.", "nu": "귀로 들어온 정보가 긍정적임을 표현합니다."}]}
        ]},
        "11": { "title": "Lesson 11: 동사 심화", "desc": "구동사를 활용해 네이티브처럼 입체적으로 말하는 법입니다.", "topics": [
            {"title": "구동사 (Phrasal Verbs)", "desc": "동사 + 전치사", "essence": "기본동사에 전치사의 방향성이 더해져 수학처럼 뜻이 확장되는 원리입니다.", "neural": "이미지의 융합", "sentences": [{"en": "Don't give up.", "ko": "포기하지 마.", "nu": "내어주고(give) 손을 위로(up) 드는 포기의 이미지입니다."}]}
        ]},
        "12": { "title": "Lesson 12: 실전 관용구", "desc": "직역하면 안 되는 관용 표현과 이음말을 익힙니다.", "topics": [
            {"title": "Idioms", "desc": "원어민식 이디엄", "essence": "문자 그대로의 뜻이 아니라 문화적 맥락이 담긴 비유적 표현입니다.", "neural": "문화적 메타포", "sentences": [{"en": "It's a piece of cake.", "ko": "식은 죽 먹기야.", "nu": "케이크 한 조각 먹는 것만큼 아주 쉽다는 뜻입니다."}]}
        ]}
    }
    
    js_data = "const lessonData = " + json.dumps(lesson_data, ensure_ascii=False, indent=2) + ";\n"

    new_js = """
// --- MASTER DASHBOARD JS ---
let currentLesson = 1;
let currentTopic = 0;

function masterInit() {
    renderMonthList();
    renderDaySelector();
    masterLoadDay(currentLesson, currentTopic);
}

function renderMonthList() {
    const list = document.getElementById('month-list');
    if(!list) return;
    list.innerHTML = '';
    
    for(let i=1; i<=12; i++) {
        if(!lessonData[i]) continue;
        const el = document.createElement('div');
        el.className = `month-item ${i === currentLesson ? 'active' : ''}`;
        el.innerHTML = `<span>Lesson ${i}</span>`;
        el.onclick = () => {
            currentLesson = i;
            currentTopic = 0;
            renderMonthList();
            renderDaySelector();
            masterLoadDay(currentLesson, currentTopic);
        };
        list.appendChild(el);
    }
}

function renderDaySelector() {
    const sel = document.getElementById('day-selector');
    if(!sel) return;
    sel.innerHTML = '';
    
    const topics = lessonData[currentLesson].topics;
    topics.forEach((t, idx) => {
        const btn = document.createElement('div');
        btn.className = `day-btn ${idx === currentTopic ? 'active' : ''}`;
        
        // Custom UI for the Pill (Top Tab) as requested
        btn.style.display = 'flex';
        btn.style.flexDirection = 'column';
        btn.style.alignItems = 'center';
        btn.style.padding = '8px 16px';
        btn.style.height = 'auto';
        btn.style.minWidth = '120px';
        btn.style.lineHeight = '1.3';
        
        btn.innerHTML = `<span style="font-size:14px; font-weight:800; color:var(--text);">${t.title}</span><span style="font-size:10px; color:var(--text-dim); margin-top:4px;">${t.desc}</span>`;
        
        btn.onclick = () => {
            currentTopic = idx;
            renderDaySelector();
            masterLoadDay(currentLesson, currentTopic);
        };
        sel.appendChild(btn);
    });
}

function masterLoadDay(lessonIdx, topicIdx) {
    const data = lessonData[lessonIdx];
    const topic = data.topics[topicIdx];
    if(!topic) return;

    // Update Header
    document.getElementById('current-month-name').textContent = data.title;
    document.getElementById('current-day-num').textContent = data.desc;

    // Update Essence Box
    document.getElementById('core-verb-label').textContent = topic.title;
    document.getElementById('mastery-title').textContent = "핵심 개념 (Essence)";
    document.getElementById('governing-phrase').textContent = topic.essence;
    document.getElementById('mastery-desc').textContent = "인지 맵핑: " + topic.neural;

    // Render Sentences
    const container = document.getElementById('master-sentence-container');
    if(!container) return;
    
    container.innerHTML = topic.sentences.map((s, i) => `
        <div class="sentence-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
                <div class="sentence-en">${s.en}</div>
                <div style="font-size:11px; font-weight:700; color:var(--accent); opacity:0.8;">Example 0${i+1}</div>
            </div>
            <div class="sentence-kr">${s.ko}</div>
            <div class="sentence-nuance" style="margin-top:10px; border-top: 1px dashed var(--border); padding-top:10px;">
                💡 <b>상세 설명:</b> ${s.nu}
            </div>
            <button class="voice-btn" style="position: absolute; top: 12px; right: 15px; background:none; border:none; font-size:18px; cursor:pointer; opacity:0.6;" onclick="event.stopPropagation(); speakText('${s.en.replace(/'/g, "\\'")}')" title="듣기">🔊</button>
        </div>
    `).join('');
}
"""

    # We inject `lessonData` and replace `masterInit`, `renderMonthList`, `renderDaySelector`, `masterLoadDay`, `masterShowBriefing`.
    start_str = "// --- MASTER DASHBOARD JS ---"
    end_str = "window.onload = () => {"
    
    idx_start = html.find(start_str)
    idx_end = html.find(end_str)
    
    if idx_start != -1 and idx_end != -1:
        html = html[:idx_start] + js_data + new_js + "\n  " + html[idx_end:]

    # Remove videos HTML
    html = re.sub(r'<div id="master-video-area".*?</div>', '', html, flags=re.DOTALL)
    
    # Also change the nav text
    html = html.replace("💎 Master Dashboard", "📘 365 스터디 코스")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Curriculum successfully rebuilt.")

if __name__ == "__main__":
    main()
