import json
import re

go_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Go</strong>는 단순히 '가다'라는 뜻이 아닙니다.<br/>
        원어민에게 go는 <strong>'현재 있는 중심점(나 혹은 상대방)에서 멀어지는 모든 움직임'</strong>을 의미합니다.
    </div>

    <h2 class="insight-h2">Go의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Go</strong>의 핵심은</p>
        <div class="quote-text">"멀어지다 (Moving Away)"</div>
        <p>물리적인 장소뿐만 아니라, 정상적인 상태에서 비정상적인 상태로 '이탈'할 때도 사용합니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">멀어짐의 멘탈 모델 (Go)</div>
        <pre>
 [ 현재의 위치/상태 ]   ───Go───▶   [ 다른 곳/상태 ]
  (나와 너가 있는 곳)                   (점점 멀어짐)
  (신선한 우유)                         (상한 우유)
        </pre>
    </div>

    <h2 class="insight-h2">① 장소의 이동 (Departure)</h2>
    <p class="insight-p">화자나 청자가 있는 곳을 떠나 다른 곳으로 향합니다.</p>
    <div class="example-group">
        <div class="ex-en">I have to go now.</div>
        <div class="ex-ko">나 이제 가야 돼. (이곳에서 멀어짐)</div>
        <div class="ex-en" style="margin-top:12px;">Let's go.</div>
        <div class="ex-ko">가자. (우리가 있는 곳을 떠남)</div>
    </div>

    <h2 class="insight-h2">② 부정적 상태로의 변화 (Deterioration)</h2>
    <p class="insight-p">좋은 상태(정상)에서 나쁜 상태(비정상)로 '멀어지는' 그림입니다. 그래서 안 좋은 변화에는 주로 Go를 씁니다.</p>
    <div class="example-group">
        <div class="ex-en">The milk went bad.</div>
        <div class="ex-ko">우유가 상했다. (정상 상태에서 이탈함)</div>
        <div class="ex-en" style="margin-top:12px;">Things went wrong.</div>
        <div class="ex-ko">일이 틀어졌다. (올바른 궤도에서 벗어남)</div>
    </div>

    <h2 class="insight-h2">③ 기능의 정지 (Stop working)</h2>
    <p class="insight-p">에너지나 시력이 멀어져서 사라지는 뉘앙스입니다.</p>
    <div class="example-group">
        <div class="ex-en">My vision is going.</div>
        <div class="ex-ko">시력이 점점 떨어지고 있어.</div>
    </div>
</div>
"""

come_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Come</strong>은 단순히 '오다'가 아닙니다.<br/>
        원어민에게 come은 <strong>'중심점(나, 상대방, 목적지)으로 가까워지는 모든 움직임'</strong>을 의미합니다.
    </div>

    <h2 class="insight-h2">Come의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Come</strong>의 핵심은</p>
        <div class="quote-text">"가까워지다 (Moving Towards)"</div>
        <p>상대방이 있는 곳으로 갈 때 한국어는 "나 갈게(Go)"라고 하지만, 영어는 상대방과 가까워지므로 "I'm coming(Come)"이라고 합니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">가까워짐의 멘탈 모델 (Come)</div>
        <pre>
 [ 출발지 ]   ───Come───▶   [ 도착지 (나/너/목표) ]
                            (점점 가까워짐)
                            (정상 상태로 돌아옴)
        </pre>
    </div>

    <h2 class="insight-h2">① 기준점으로의 이동 (Approach)</h2>
    <p class="insight-p">말하는 사람이나 듣는 사람의 위치로 다가가는 행위입니다.</p>
    <div class="example-group">
        <div class="ex-en">I'm coming.</div>
        <div class="ex-ko">지금 가요. (너와 내가 가까워지고 있으니 Come)</div>
        <div class="ex-en" style="margin-top:12px;">Come here.</div>
        <div class="ex-ko">이리로 와. (내 쪽으로 가까워짐)</div>
    </div>

    <h2 class="insight-h2">② 긍정적/정상적 상태로의 진입 (Improvement)</h2>
    <p class="insight-p">Go가 나쁜 상태로 벗어나는 것이라면, Come은 본래의 상태나 긍정적인 현실로 '다가오는' 그림입니다.</p>
    <div class="example-group">
        <div class="ex-en">My dream came true.</div>
        <div class="ex-ko">꿈이 이루어졌다. (꿈이 현실로 가까워짐)</div>
        <div class="ex-en" style="margin-top:12px;">It came to my mind.</div>
        <div class="ex-ko">생각이 떠올랐다. (내 머릿속으로 생각이 다가옴)</div>
    </div>

    <h2 class="insight-h2">Go와 Come 비교</h2>
    <div class="compare-grid">
        <div class="compare-col">
            <div class="c-title">Go (멀어짐)</div>
            <p><strong>He went crazy.</strong> (그는 미쳐버렸다)</p>
            <p>정상 상태에서 멀어짐 = 부정적 변화</p>
            <div class="c-tag">이탈, 악화</div>
        </div>
        <div class="compare-col">
            <div class="c-title">Come (가까워짐)</div>
            <p><strong>The dream came true.</strong> (꿈이 이루어졌다)</p>
            <p>목표 상태로 진입함 = 긍정적 변화</p>
            <div class="c-tag">접근, 실현</div>
        </div>
    </div>
</div>
"""

put_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Put</strong>은 물리적인 공간에 물건을 내려놓는 것뿐만 아니라,<br/>
        특정 상태나 상황에 사람이나 사물을 <strong>'처하게 만드는'</strong> 가장 보편적인 배치 동사입니다.
    </div>

    <h2 class="insight-h2">Put의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Put</strong>의 핵심은</p>
        <div class="quote-text">"무언가를 특정 장소나 상태에 이동시켜 두다."</div>
        <p>물건을 책상 위에 두는 것도 Put, 내 생각을 글에 담는 것도 Put, 누군가를 난처한 상황에 몰아넣는 것도 Put입니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">이동 후 배치 (Put)</div>
        <pre>
  [ 대상 ]  ───이동───▶  [ 특정 장소/상태 ]
  (열쇠)                 (책상 위)
  (생각)                 (말/글)
  (너)                   (위험한 상황)
        </pre>
    </div>

    <h2 class="insight-h2">① 물리적 배치 (Placement)</h2>
    <p class="insight-p">물건을 특정한 공간에 내려놓는 가장 기본적인 의미입니다.</p>
    <div class="example-group">
        <div class="ex-en">Put it on the table.</div>
        <div class="ex-ko">테이블 위에 둬.</div>
    </div>

    <h2 class="insight-h2">② 추상적 상태의 부여 (Condition)</h2>
    <p class="insight-p">사람이나 사물을 특정한 상황(Condition) 속에 밀어 넣을 때 사용합니다.</p>
    <div class="example-group">
        <div class="ex-en">Don't put me in this position.</div>
        <div class="ex-ko">나를 이런 난처한 입장에 처하게 하지 마.</div>
        <div class="ex-en" style="margin-top:12px;">You put me at ease.</div>
        <div class="ex-ko">네가 나를 편안하게 해 주었어. (나를 편안한 상태에 둠)</div>
    </div>

    <h2 class="insight-h2">③ 생각의 표현 (Expression)</h2>
    <p class="insight-p">머릿속에 둥둥 떠다니는 생각(대상)을 언어라는 그릇(장소)에 옮겨 담는(Put) 행위입니다.</p>
    <div class="example-group">
        <div class="ex-en">Let me put it this way.</div>
        <div class="ex-ko">내가 이렇게 표현해 볼게. (내 생각을 이런 방식으로 담아볼게)</div>
    </div>
</div>
"""

set_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Set</strong>은 Put과 달리 아주 섬세한 동사입니다.<br/>
        원어민에게 set은 무언가를 그저 '두는(Put)' 것이 아니라, <strong>'목적을 가지고 흔들리지 않게 고정시키는'</strong> 행위를 의미합니다.
    </div>

    <h2 class="insight-h2">Set의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Set</strong>의 핵심은</p>
        <div class="quote-text">"목적을 위해 고정시키고 세팅하다."</div>
        <p>알람을 맞추고, 목표를 정하고, 젤리가 굳고, 해가 저무는(고정되는) 모든 현상이 Set입니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">고정과 준비 (Set)</div>
        <pre>
  [ 대상 ]  ───조정/고정───▶  [ 흔들리지 않는 상태 ]
                            (알람 시간 고정)
                            (규칙 확립)
                            (단단하게 굳음)
        </pre>
    </div>

    <h2 class="insight-h2">① 기계나 시스템의 설정 (Configuration)</h2>
    <p class="insight-p">작동을 위해 기계를 특정한 값에 고정시켜 두는 행위입니다.</p>
    <div class="example-group">
        <div class="ex-en">Set the alarm for 6 AM.</div>
        <div class="ex-ko">알람을 아침 6시로 맞춰 줘. (6시라는 값에 고정함)</div>
    </div>

    <h2 class="insight-h2">② 기준과 규칙의 확립 (Establishment)</h2>
    <p class="insight-p">목표나 규칙을 흔들리지 않게 단단히 박아두는 느낌입니다.</p>
    <div class="example-group">
        <div class="ex-en">Set a goal.</div>
        <div class="ex-ko">목표를 세워라. (목표를 고정시킴)</div>
        <div class="ex-en" style="margin-top:12px;">Set the rules.</div>
        <div class="ex-ko">규칙을 정하다.</div>
    </div>

    <h2 class="insight-h2">③ 자연현상과 굳어짐 (Solidify)</h2>
    <p class="insight-p">액체가 단단하게 굳거나, 해가 지평선 아래로 내려가 자리를 잡는 것도 Set입니다.</p>
    <div class="example-group">
        <div class="ex-en">The sun sets in the west.</div>
        <div class="ex-ko">해는 서쪽으로 진다. (자리를 잡고 고정됨)</div>
    </div>

    <h2 class="insight-h2">Put과 Set 비교</h2>
    <div class="compare-grid">
        <div class="compare-col">
            <div class="c-title">Put (단순한 이동)</div>
            <p><strong>Put the cup on the table.</strong></p>
            <p>단순히 컵을 테이블로 옮겨 두다.</p>
            <div class="c-tag">일반적, 우발적 가능</div>
        </div>
        <div class="compare-col">
            <div class="c-title">Set (목적과 고정)</div>
            <p><strong>Set the table.</strong></p>
            <p>식사를 위해 숟가락과 그릇을 '세팅'하다.</p>
            <div class="c-tag">목적성, 정교함, 고정</div>
        </div>
    </div>
</div>
"""

bring_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Bring</strong>은 단순히 '가져오다'가 아닙니다.<br/>
        원어민에게 bring은 <strong>'대상을 나와 함께(또는 청자 쪽으로) 동반하여 이동시키는'</strong> 움직임입니다.
    </div>

    <h2 class="insight-h2">Bring의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Bring</strong>의 핵심은</p>
        <div class="quote-text">"나와 함께 동반하여 다가오다."</div>
        <p>무언가를 손에 쥐고 오거나, 특정 이슈를 대화의 장으로 끌고 들어오는 뉘앙스입니다. (Come과 결이 같습니다)</p>
    </div>

    <h2 class="insight-h2">① 물리적 동반 이동 (Accompany)</h2>
    <p class="insight-p">나, 혹은 네가 있는 곳으로 물건이나 사람을 함께 데려오는 행위입니다.</p>
    <div class="example-group">
        <div class="ex-en">Did you bring the umbrella?</div>
        <div class="ex-ko">우산 가져왔어? (이곳으로 올 때 동반했는가)</div>
        <div class="ex-en" style="margin-top:12px;">I'll bring my friend.</div>
        <div class="ex-ko">친구를 데려갈게.</div>
    </div>

    <h2 class="insight-h2">② 추상적 결과의 수반 (Result)</h2>
    <p class="insight-p">어떤 원인이 특정한 결과나 변화를 끌고 들어옵니다.</p>
    <div class="example-group">
        <div class="ex-en">Spring brings warm weather.</div>
        <div class="ex-ko">봄은 따뜻한 날씨를 가져온다. (봄이라는 현상이 따뜻함을 수반함)</div>
    </div>
    
    <h2 class="insight-h2">③ 주제의 환기 (Bring up)</h2>
    <p class="insight-p">대화 중 숨어있던 주제를 표면 위(up)로 동반하여 끌어올립니다.</p>
    <div class="example-group">
        <div class="ex-en">Don't bring that up.</div>
        <div class="ex-ko">그 얘기 꺼내지 마. (그 이슈를 이 대화로 끌고 오지 마)</div>
    </div>
</div>
"""

carry_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Carry</strong>는 그저 들고 다니는 것이 아닙니다.<br/>
        원어민에게 carry는 <strong>'중력이나 하중(무게)을 버티며 감당하는'</strong> 행위입니다.
    </div>

    <h2 class="insight-h2">Carry의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Carry</strong>의 핵심은</p>
        <div class="quote-text">"무게나 책임을 짊어지고 지탱하다."</div>
        <p>무거운 가방을 들 때뿐만 아니라, 가족의 생계, 임신, 질병의 보균 등 무거운 것을 감당할 때 모두 쓰입니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">하중의 지탱 (Carry)</div>
        <pre>
   [ 무거운 짐 / 책임 / 아기 / 바이러스 ]
         ▲
         │ (지탱하며 이동)
   [ 주 체 (나) ]
        </pre>
    </div>

    <h2 class="insight-h2">① 물리적 하중 지탱 (Supporting weight)</h2>
    <p class="insight-p">무거운 것을 몸의 근력을 이용해 지탱하며 옮깁니다.</p>
    <div class="example-group">
        <div class="ex-en">Can you carry this bag?</div>
        <div class="ex-ko">이 가방 좀 들어줄래? (하중을 지탱해줄래)</div>
    </div>

    <h2 class="insight-h2">② 추상적 책임의 감당 (Responsibility)</h2>
    <p class="insight-p">팀의 운명이나 프로젝트의 무거운 책임을 짊어지는 느낌입니다. (게임에서 버스 기사를 '캐리'한다고 하죠)</p>
    <div class="example-group">
        <div class="ex-en">She carries the whole team.</div>
        <div class="ex-ko">그녀가 팀 전체를 이끌어간다. (팀의 무게를 혼자 지탱함)</div>
    </div>

    <h2 class="insight-h2">③ 생물학적 품음 (Bearing)</h2>
    <p class="insight-p">생명이나 질병을 몸 안에 '지탱하여' 품고 있는 상태입니다.</p>
    <div class="example-group">
        <div class="ex-en">She is carrying a child.</div>
        <div class="ex-ko">그녀는 임신 중이다. (아이를 품고 지탱하고 있다)</div>
        <div class="ex-en" style="margin-top:12px;">Mosquitoes carry diseases.</div>
        <div class="ex-ko">모기는 질병을 옮긴다. (균을 짊어지고 다님)</div>
    </div>
</div>
"""

def append_insights():
    with open('master/data/core_insights.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to insert the new HTML properties into the window.coreInsights object.
    # The existing file ends with:
    #     "Make": `...`
    # };
    
    # Let's remove the last closing brace and append the new ones.
    # Find the last `}`
    last_brace_idx = content.rfind('}')
    if last_brace_idx != -1:
        prefix = content[:last_brace_idx].rstrip()
        
        # Ensure we have a comma after Make
        if not prefix.endswith(','):
            prefix += ','
            
        new_content = prefix + f"""
    "Go": `{go_html}`,
    "Come": `{come_html}`,
    "Put": `{put_html}`,
    "Set": `{set_html}`,
    "Bring": `{bring_html}`,
    "Carry": `{carry_html}`
}};
"""
        with open('master/data/core_insights.js', 'w', encoding='utf-8') as f:
            f.write(new_content)

if __name__ == "__main__":
    append_insights()
