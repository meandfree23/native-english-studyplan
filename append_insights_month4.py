import json
import re

# 1. Update month4.js to add core_insight keys
def update_month4():
    with open('master/data/month4.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to add core_insight only to the first day of each preposition block.
    # In: Day 91, Out: Day 96, On: Day 101, Off: Day 106, Up: Day 111, Down: Day 116
    
    replacements = {
        '"91": {': '"91": {\n    "core_insight": "In",',
        '"96": {': '"96": {\n    "core_insight": "Out",',
        '"101": {': '"101": {\n    "core_insight": "On",',
        '"106": {': '"106": {\n    "core_insight": "Off",',
        '"111": {': '"111": {\n    "core_insight": "Up",',
        '"116": {': '"116": {\n    "core_insight": "Down",'
    }
    
    for key, val in replacements.items():
        if val not in content:
            content = content.replace(key, val)
            
    with open('master/data/month4.js', 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Append HTML strings to core_insights.js
def update_core_insights():
    with open('master/data/core_insights.js', 'r', encoding='utf-8') as f:
        content = f.read()

    new_insights = """
    "In": `
<div class="insight-article">
    <div class="insight-intro">
        <strong>In</strong>은 단순히 장소의 내부를 가리키는 것이 아닙니다.<br/>
        원어민에게 In은 <strong>'어떤 공간이나 경계선(Boundary) 안으로 깊숙이 진입해 포용된 락인(Lock-in) 상태'</strong>를 의미합니다.
    </div>

    <h2 class="insight-h2">In의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>In</strong>의 핵심은</p>
        <div class="quote-text">"경계선(Boundary) 내부로의 완전한 안착과 소속"</div>
        <p>입니다. 물리적 공간뿐만 아니라, 시간이나 추상적인 소속감까지 모두 아우르는 강력한 울타리입니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">경계선 내부 포용 (In)</div>
        <pre>
 ┌──────────────┐
 │    [ 나 ]    │
 └──────────────┘
        </pre>
        <div class="ascii-footer">외부와 차단된 안전한 바운더리</div>
    </div>

    <h2 class="insight-h2">① 공간적 소속 (Spatial Enclosure)</h2>
    <p class="insight-p">물리적인 공간(상자, 방, 차 등)의 3차원적인 내부로 들어갑니다.</p>
    <div class="example-group">
        <div class="ex-en">I am in the car.</div>
        <div class="ex-ko">나는 차 안에 있다. (차라는 3차원 공간 안에 포용됨)</div>
        <div class="ex-en" style="margin-top:12px;">Put it in the box.</div>
        <div class="ex-ko">그것을 상자 안에 넣어라.</div>
    </div>

    <h2 class="insight-h2">② 추상적 상태와 소속 (Abstract State)</h2>
    <p class="insight-p">눈에 보이지 않는 상황, 감정, 소속의 바운더리 안으로 들어갑니다.</p>
    <div class="example-group">
        <div class="ex-en">I am in trouble.</div>
        <div class="ex-ko">나는 곤경에 처해 있다. (곤경이라는 상황적 테두리 안)</div>
        <div class="ex-en" style="margin-top:12px;">I am in love.</div>
        <div class="ex-ko">나는 사랑에 빠졌다. (사랑이라는 감정의 테두리 안)</div>
    </div>

    <h2 class="insight-h2">③ 기한 내 완료 (Time Enclosure)</h2>
    <p class="insight-p">시간을 하나의 공간(테두리)으로 보고, 그 테두리가 닫히기 전의 시점을 의미합니다.</p>
    <div class="example-group">
        <div class="ex-en">I'll be there in 5 minutes.</div>
        <div class="ex-ko">5분 안에 그곳에 갈게. (5분이라는 시간의 바운더리 안)</div>
    </div>
</div>
`,
    "Out": `
<div class="insight-article">
    <div class="insight-intro">
        <strong>Out</strong>은 단순히 '밖으로'라는 방향만 있는 것이 아닙니다.<br/>
        원어민에게 Out은 <strong>'기존의 바운더리(경계선) 안에서 밖으로 완전히 이탈하거나 폭발적으로 빠져나온 상태'</strong>를 의미합니다.
    </div>

    <h2 class="insight-h2">Out의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Out</strong>의 핵심은</p>
        <div class="quote-text">"내부에서 외부 공간으로의 폭발적 이탈과 소진"</div>
        <p>입니다. 안에 있던 무언가가 밖으로 나오면서 '비어버림(소진)'과 '드러남(발현)'이라는 뜻까지 파생됩니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">바운더리 이탈 (Out)</div>
        <pre>
 ┌────────┐
 │        │ ──▶ [ 나 ]
 └────────┘
        </pre>
        <div class="ascii-footer">안에서 밖으로 폭발하며 나타나는 모습</div>
    </div>

    <h2 class="insight-h2">① 물리적 이탈 (Physical Exit)</h2>
    <p class="insight-p">특정 공간의 내부에서 외부로 빠져나오는 가장 직관적인 움직임입니다.</p>
    <div class="example-group">
        <div class="ex-en">Get out of here.</div>
        <div class="ex-ko">여기서 나가. (이 공간 밖으로 이탈해라)</div>
        <div class="ex-en" style="margin-top:12px;">Take it out.</div>
        <div class="ex-ko">그것을 꺼내. (내부에서 외부로)</div>
    </div>

    <h2 class="insight-h2">② 상태의 끝 및 고갈 (Depletion & End)</h2>
    <p class="insight-p">안에 있던 내용물이 모두 밖으로 빠져나와 텅 비어버린 상태를 의미합니다.</p>
    <div class="example-group">
        <div class="ex-en">We are out of gas.</div>
        <div class="ex-ko">우리는 기름이 다 떨어졌다. (연료통에서 기름이 모두 빠져나감)</div>
        <div class="ex-en" style="margin-top:12px;">Time is out.</div>
        <div class="ex-ko">시간이 끝났다. (주어진 시간이 고갈됨)</div>
    </div>

    <h2 class="insight-h2">③ 숨은 것의 발현 (Appearance)</h2>
    <p class="insight-p">어둠이나 베일 속에 있던 것이 밖(Out)으로 나오면서 시야에 또렷하게 드러납니다.</p>
    <div class="example-group">
        <div class="ex-en">Watch out!</div>
        <div class="ex-ko">조심해! (시선을 밖으로 향해 위험을 감지해라)</div>
        <div class="ex-en" style="margin-top:12px;">Find out the truth.</div>
        <div class="ex-ko">진실을 알아내라. (숨겨진 것을 밖으로 끄집어내라)</div>
    </div>
</div>
`,
    "On": `
<div class="insight-article">
    <div class="insight-intro">
        <strong>On</strong>은 단순히 '위(Above)'를 뜻하는 단어가 아닙니다.<br/>
        원어민에게 On은 <strong>'두 표면(Surface)이 떨어지지 않고 마진 없이 완벽히 밀착하여 접촉(Contact)된 상태'</strong>를 의미합니다.
    </div>

    <h2 class="insight-h2">On의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>On</strong>의 핵심은</p>
        <div class="quote-text">"두 대상의 표면이 0의 마진으로 완벽히 락킹(Locking)됨"</div>
        <p>입니다. 중력에 의해 위에 얹혀 있든, 벽에 붙어 있든, 천장에 매달려 있든 표면의 맞닿음이 중요합니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">표면의 밀착 (On)</div>
        <pre>
     [ 대상 ]
   ━━━━━━━━━━━━
     [ 표면 ]
        </pre>
        <div class="ascii-footer">떨어지지 않고 딱 붙어있는 상태</div>
    </div>

    <h2 class="insight-h2">① 표면적 물리 접촉 (Physical Contact)</h2>
    <p class="insight-p">바닥, 벽, 천장, 혹은 피부 등 어떤 표면에 물리적으로 맞닿아 있습니다.</p>
    <div class="example-group">
        <div class="ex-en">Put it on the table.</div>
        <div class="ex-ko">그것을 테이블 위에 놓아라. (테이블 표면에 접촉)</div>
        <div class="ex-en" style="margin-top:12px;">Try it on.</div>
        <div class="ex-ko">입어봐라. (옷을 피부 표면에 밀착시켜라)</div>
    </div>

    <h2 class="insight-h2">② 의존과 지속 (Dependence & Continuation)</h2>
    <p class="insight-p">접촉이 끊어지지 않는다는 것은, 상태가 멈추지 않고 계속 이어진다는 의미로 확장됩니다.</p>
    <div class="example-group">
        <div class="ex-en">Keep on going.</div>
        <div class="ex-ko">계속 가라. (행동을 끊지 말고 접착시킨 채로)</div>
        <div class="ex-en" style="margin-top:12px;">It depends on you.</div>
        <div class="ex-ko">너에게 달려있다. (결과가 너라는 존재에 딱 달라붙어 있음)</div>
    </div>

    <h2 class="insight-h2">③ 작동 및 연결 상태 (Active State)</h2>
    <p class="insight-p">전원이나 회로가 스위치 표면에 '접촉(On)'되어 전기가 흐르고 작동하는 상태입니다.</p>
    <div class="example-group">
        <div class="ex-en">Turn on the TV.</div>
        <div class="ex-ko">TV를 켜라. (회로를 접촉시켜 작동시켜라)</div>
        <div class="ex-en" style="margin-top:12px;">The show is on.</div>
        <div class="ex-ko">쇼가 진행 중이다. (쇼가 대중들과 접촉 중)</div>
    </div>
</div>
`,
    "Off": `
<div class="insight-article">
    <div class="insight-intro">
        <strong>Off</strong>는 단순히 불을 '끄는' 단어가 아닙니다.<br/>
        원어민에게 Off는 <strong>'밀착(On)되어 있던 표면들 사이의 완전한 분리와 단절'</strong>을 의미합니다.
    </div>

    <h2 class="insight-h2">Off의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Off</strong>의 핵심은</p>
        <div class="quote-text">"접착면에서의 완전한 이탈과 분리"</div>
        <p>입니다. 붙어있던 것이 떨어져 나가면서 해방감을 주기도 하고, 물리적인 단절을 만들어내기도 합니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">접착면 분리 (Off)</div>
        <pre>
     [ 대상 ]
       ↑ (분리)
   ━━━━━━━━━━━━
     [ 표면 ]
        </pre>
        <div class="ascii-footer">On 상태에서 마진이 생기며 떨어져 나감</div>
    </div>

    <h2 class="insight-h2">① 물리적 분리 (Physical Separation)</h2>
    <p class="insight-p">표면에서 떨어져 나가는 직관적인 움직임입니다.</p>
    <div class="example-group">
        <div class="ex-en">Take your hands off.</div>
        <div class="ex-ko">손 떼라. (피부 표면에서 분리해라)</div>
        <div class="ex-en" style="margin-top:12px;">Get off the bus.</div>
        <div class="ex-ko">버스에서 내려라. (버스의 발판에서 몸을 분리해라)</div>
        <div class="ex-en" style="margin-top:12px;">Take off your shoes.</div>
        <div class="ex-ko">신발을 벗어라. (발 표면에서 신발을 떼어내라)</div>
    </div>

    <h2 class="insight-h2">② 연결의 단절 (Disconnection)</h2>
    <p class="insight-p">회로나 전원, 또는 계약 등의 연결고리가 끊어지며 무효화된 상태입니다.</p>
    <div class="example-group">
        <div class="ex-en">Turn off the light.</div>
        <div class="ex-ko">불을 꺼라. (회로의 접촉을 단절시켜라)</div>
        <div class="ex-en" style="margin-top:12px;">The deal is off.</div>
        <div class="ex-ko">그 거래는 무산되었다. (약속의 결합 상태가 떨어져 나감)</div>
    </div>

    <h2 class="insight-h2">③ 일상의 이탈 (Break & Departure)</h2>
    <p class="insight-p">원래 있어야 할 자리(근무지, 현재 장소)에서 몸이 분리되어 떠나는 해방의 그림입니다.</p>
    <div class="example-group">
        <div class="ex-en">I am off today.</div>
        <div class="ex-ko">나 오늘 쉬는 날이야. (일터에서 단절됨)</div>
        <div class="ex-en" style="margin-top:12px;">I'm taking off now.</div>
        <div class="ex-ko">나 지금 출발해. (현재 위치의 바닥에서 발을 뗌)</div>
    </div>
</div>
`,
    "Up": `
<div class="insight-article">
    <div class="insight-intro">
        <strong>Up</strong>은 단순히 '위쪽으로' 이동하는 것만을 뜻하지 않습니다.<br/>
        원어민에게 Up은 <strong>'수직 상승을 넘어, 수치와 에너지가 100% 임계점(한계점)까지 꽉 차오르는 완성의 상태'</strong>를 의미합니다.
    </div>

    <h2 class="insight-h2">Up의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Up</strong>의 핵심은</p>
        <div class="quote-text">"위로 뻗어가는 에너지와 빈 공간 없는 100% 채워짐"</div>
        <p>입니다. 잔에 물이 위로 차올라 끝까지 가득 차는 모습을 상상하시면 좋습니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">상승과 임계점 도달 (Up)</div>
        <pre>
    [ 100% ]
      ▲
      │ (에너지)
      │
      │
        </pre>
        <div class="ascii-footer">최대치까지 완전히 차오름</div>
    </div>

    <h2 class="insight-h2">① 수직적 상승 (Vertical Movement)</h2>
    <p class="insight-p">물리적인 위치가 바닥에서 공중(위)을 향해 뻗어나갑니다.</p>
    <div class="example-group">
        <div class="ex-en">Look up.</div>
        <div class="ex-ko">위로 쳐다봐라.</div>
        <div class="ex-en" style="margin-top:12px;">Stand up.</div>
        <div class="ex-ko">일어서라. (자세를 수직으로 세움)</div>
    </div>

    <h2 class="insight-h2">② 수치와 강도의 증가 (Increase)</h2>
    <p class="insight-p">볼륨, 가격, 수준 등 에너지가 점점 커지는 확장 상태입니다.</p>
    <div class="example-group">
        <div class="ex-en">Speak up.</div>
        <div class="ex-ko">크게 말해라. (목소리 볼륨을 상승시켜라)</div>
        <div class="ex-en" style="margin-top:12px;">Prices are going up.</div>
        <div class="ex-ko">가격이 오르고 있다.</div>
    </div>

    <h2 class="insight-h2">③ 100% 완전한 소진 (Completion)</h2>
    <p class="insight-p">위로 계속 차오르다가 결국 꼭대기(100%)에 다다라 무언가가 끝나버린 상태입니다.</p>
    <div class="example-group">
        <div class="ex-en">Drink up.</div>
        <div class="ex-ko">다 마셔버려라. (남김없이 완전히 끝내라)</div>
        <div class="ex-en" style="margin-top:12px;">Time is up.</div>
        <div class="ex-ko">시간이 다 됐다. (주어진 시간 게이지가 끝까지 차버림)</div>
    </div>
</div>
`,
    "Down": `
<div class="insight-article">
    <div class="insight-intro">
        <strong>Down</strong>은 단순히 '아래쪽으로' 내려가는 방향성 그 이상입니다.<br/>
        원어민에게 Down은 <strong>'기준치 아래로 물리적인 추락을 하거나, 기세가 완전히 꺾여 억눌린 상태'</strong>를 의미합니다.
    </div>

    <h2 class="insight-h2">Down의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Down</strong>의 핵심은</p>
        <div class="quote-text">"중력에 의한 하강과 강제적인 억눌림"</div>
        <p>입니다. 무언가가 아래로 내려앉아 활동이 정지되거나 힘이 빠지는 무거운 뉘앙스가 있습니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">하강과 억압 (Down)</div>
        <pre>
      │
      │ (무게감)
      ▼
   ━━━━━━━ (바닥/고정)
        </pre>
        <div class="ascii-footer">에너지가 소멸하고 바닥에 고정됨</div>
    </div>

    <h2 class="insight-h2">① 수직적 하강 (Vertical Descent)</h2>
    <p class="insight-p">높은 곳에서 낮은 곳으로 중력을 따라 내려가는 기본 움직임입니다.</p>
    <div class="example-group">
        <div class="ex-en">Sit down.</div>
        <div class="ex-ko">앉아라. (자세를 아래로 내림)</div>
        <div class="ex-en" style="margin-top:12px;">Put it down.</div>
        <div class="ex-ko">내려 놓아라.</div>
    </div>

    <h2 class="insight-h2">② 기세와 수치의 억제 (Decrease)</h2>
    <p class="insight-p">솟아오르던 감정이나 수치가 꺾이며 차분해지거나 줄어듭니다.</p>
    <div class="example-group">
        <div class="ex-en">Turn it down.</div>
        <div class="ex-ko">소리를 줄여라. (볼륨의 기세를 꺾어라)</div>
        <div class="ex-en" style="margin-top:12px;">Calm down.</div>
        <div class="ex-ko">진정해라. (격양된 감정 에너지를 가라앉혀라)</div>
    </div>

    <h2 class="insight-h2">③ 기능의 정지 및 완전한 고정 (Suppression)</h2>
    <p class="insight-p">완전히 바닥으로 짓눌려 기능이 마비되거나, 어딘가에 꽉 고정되어 버린 상태입니다.</p>
    <div class="example-group">
        <div class="ex-en">The system is down.</div>
        <div class="ex-ko">시스템이 죽었다. (서버가 뻗어 기능이 완전히 마비됨)</div>
        <div class="ex-en" style="margin-top:12px;">Write it down.</div>
        <div class="ex-ko">적어 두어라. (휘발성인 정보의 목덜미를 낚아채 종이 위에 고정시킴)</div>
    </div>
</div>
`
    """

    if '"In":' not in content:
        # insert before the last closing brace
        content = content.replace('\n};', ',\n' + new_insights + '\n};')
        with open('master/data/core_insights.js', 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    update_month4()
    update_core_insights()
    print("Done")
