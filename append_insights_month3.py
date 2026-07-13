import json
import re

look_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Look</strong>은 그저 '보다'가 아닙니다.<br/>
        원어민에게 look은 <strong>'내 시선의 화살표를 특정한 방향으로 향하게 하는 의지적인 행동'</strong>입니다.
    </div>

    <h2 class="insight-h2">Look의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Look</strong>의 핵심은</p>
        <div class="quote-text">"시선의 방향과 집중 (Directing one's eyes)"</div>
        <p>무언가를 보기 위해 고개를 돌리거나 눈길을 '주는' 행위 그 자체에 초점이 맞춰져 있습니다. (결과적으로 보였는지 안 보였는지는 중요하지 않습니다.)</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">시선의 방향 (Look)</div>
        <pre>
   [ 내 눈 ]   ───시선의 화살표───▶   [ 대 상 ]
 (고개를 돌림)                        (목표물)
        </pre>
    </div>

    <h2 class="insight-h2">① 시선을 향함 (Directing attention)</h2>
    <p class="insight-p">대상을 향해 의지적으로 눈길을 줍니다. 그래서 보통 방향을 나타내는 전치사 at과 함께 씁니다.</p>
    <div class="example-group">
        <div class="ex-en">Look at me.</div>
        <div class="ex-ko">나를 봐. (네 시선을 내 쪽으로 향해라)</div>
    </div>

    <h2 class="insight-h2">② 겉모습의 인상 (Appearance)</h2>
    <p class="insight-p">시선을 주었을 때 내 눈에 들어오는 '겉모습이나 상태'를 표현할 때도 씁니다.</p>
    <div class="example-group">
        <div class="ex-en">You look tired.</div>
        <div class="ex-ko">너 피곤해 보여. (내 시선에 맺힌 너의 겉모습이 그러하다)</div>
    </div>
</div>
"""

see_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>See</strong>는 시선을 주는 행동(Look)이 아닙니다.<br/>
        원어민에게 see는 <strong>'빛이 내 눈에 들어와 망막에 상이 맺히는 자연스러운 지각 현상'</strong>입니다.
    </div>

    <h2 class="insight-h2">See의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>See</strong>의 핵심은</p>
        <div class="quote-text">"망막에 맺힘 / 인지함 (Perception & Understanding)"</div>
        <p>애써 보려고 하지 않아도 눈을 뜨고 있으니 자연스럽게 '보이는' 결과입니다. 나아가 머릿속으로 '이해했다'는 뜻으로도 확장됩니다.</p>
    </div>

    <div class="ascii-art-box">
        <div class="ascii-title">시각적 인지 (See)</div>
        <pre>
   [ 대 상 ]   ───빛이 들어옴───▶   [ 내 눈 (망막) / 뇌 ]
 (존재하는 것)                        (자연스러운 인지)
        </pre>
    </div>

    <h2 class="insight-h2">① 자연스러운 시각적 인지 (Sight)</h2>
    <p class="insight-p">의지와 무관하게 내 시야에 들어와서 보게 된 상태입니다.</p>
    <div class="example-group">
        <div class="ex-en">I saw a bird.</div>
        <div class="ex-ko">새를 봤어. (그냥 지나가다 눈에 띄어 망막에 맺힘)</div>
    </div>

    <h2 class="insight-h2">② 뇌에서의 인지 = 이해 (Understanding)</h2>
    <p class="insight-p">눈(시각)에 빛이 들어와 상이 맺히듯, 뇌(이성)에 정보가 들어와 '이해'가 맺히는 것입니다.</p>
    <div class="example-group">
        <div class="ex-en">I see what you mean.</div>
        <div class="ex-ko">무슨 말인지 알겠어. (네 의도가 내 머릿속에 선명하게 보임)</div>
    </div>
</div>
"""

watch_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Watch</strong>는 단순한 시선(Look)이나 인지(See)가 아닙니다.<br/>
        원어민에게 watch는 <strong>'움직이거나 변화하는 대상을 일정 시간 동안 주의 깊게 추적하는 관찰'</strong>입니다.
    </div>

    <h2 class="insight-h2">Watch의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Watch</strong>의 핵심은</p>
        <div class="quote-text">"시간을 두고 주의 깊게 관찰/추적함 (Observing over time)"</div>
        <p>TV 프로그램, 경기, 뛰어노는 아이들처럼 '움직임'이 있는 대상을 유심히 지켜볼 때 사용합니다.</p>
    </div>

    <h2 class="insight-h2">① 움직이는 대상의 관찰 (Monitoring)</h2>
    <p class="insight-p">고정된 그림(Look)이 아니라 움직이는 영상(Watch)을 주의 깊게 보는 행위입니다.</p>
    <div class="example-group">
        <div class="ex-en">I'm watching a movie.</div>
        <div class="ex-ko">영화 보는 중이야. (영상의 흐름과 변화를 추적하며 감상함)</div>
    </div>
    
    <h2 class="insight-h2">② 주의 및 경계 (Be careful)</h2>
    <p class="insight-p">위험한 일이나 변화가 생기지 않는지 '예의 주시'하는 뉘앙스입니다.</p>
    <div class="example-group">
        <div class="ex-en">Watch your step.</div>
        <div class="ex-ko">발밑 조심해. (걸음걸이의 변화를 주의 깊게 살펴라)</div>
    </div>

    <h2 class="insight-h2">👀 Look vs See vs Watch 비교</h2>
    <div class="compare-grid" style="grid-template-columns: 1fr 1fr 1fr;">
        <div class="compare-col">
            <div class="c-title">Look (방향성)</div>
            <p>시선을 의지적으로 향함</p>
            <div class="c-tag">액션 중심</div>
        </div>
        <div class="compare-col">
            <div class="c-title">See (결과/인지)</div>
            <p>눈에 들어와 망막에 맺힘</p>
            <div class="c-tag">결과 중심</div>
        </div>
        <div class="compare-col">
            <div class="c-title">Watch (추적/관찰)</div>
            <p>움직임을 시간 두고 지켜봄</p>
            <div class="c-tag">과정 중심</div>
        </div>
    </div>
</div>
"""

listen_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Listen</strong>은 귀로 들어오는 소리를 무작정 듣는 것이 아닙니다.<br/>
        원어민에게 listen은 <strong>'소리를 파악하기 위해 청각의 안테나를 쫑긋 세우는 의지적인 행동'</strong>입니다. (Look의 청각 버전)
    </div>

    <h2 class="insight-h2">Listen의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Listen</strong>의 핵심은</p>
        <div class="quote-text">"청각적 집중 (Paying attention to sound)"</div>
        <p>귀를 기울여 집중하는 행동 그 자체입니다. 결과적으로 잘 안 들렸어도 귀를 기울이는 행위 자체가 Listen입니다.</p>
    </div>

    <h2 class="insight-h2">① 의도적인 청취 (Intentional hearing)</h2>
    <p class="insight-p">대상을 향해 의지적으로 귀를 엽니다. 방향을 나타내는 to와 주로 씁니다.</p>
    <div class="example-group">
        <div class="ex-en">Listen to me.</div>
        <div class="ex-ko">내 말 좀 들어봐. (네 청각의 안테나를 내 쪽으로 돌려라)</div>
    </div>
</div>
"""

hear_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Hear</strong>는 귀를 기울이는 행동(Listen)이 아닙니다.<br/>
        원어민에게 hear는 <strong>'소리가 고막을 때려 뇌에서 인지되는 자연스러운 결과'</strong>입니다. (See의 청각 버전)
    </div>

    <h2 class="insight-h2">Hear의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Hear</strong>의 핵심은</p>
        <div class="quote-text">"고막에 닿아 인지됨 (Perceiving sound)"</div>
        <p>가만히 있어도 들려오는 소음을 인지하거나, 특정 소문장/소식을 전해 들었을 때 사용합니다.</p>
    </div>

    <h2 class="insight-h2">① 자연스러운 청각적 인지 (Perception)</h2>
    <p class="insight-p">의지와 무관하게 소리가 고막에 도달하여 들리는 상태입니다.</p>
    <div class="example-group">
        <div class="ex-en">I can't hear you.</div>
        <div class="ex-ko">네 목소리가 안 들려. (네가 내는 소리가 내 고막에 도달하지 않음)</div>
    </div>
    
    <h2 class="insight-h2">🎧 Listen vs Hear 비교</h2>
    <div class="compare-grid">
        <div class="compare-col">
            <div class="c-title">Listen (귀를 기울임)</div>
            <p><strong>Are you listening?</strong></p>
            <p>내 말에 집중해서 귀를 열고 있어?</p>
            <div class="c-tag">행동, 의지</div>
        </div>
        <div class="compare-col">
            <div class="c-title">Hear (소리가 들림)</div>
            <p><strong>Can you hear me?</strong></p>
            <p>내 목소리가 네 귀에 잘 도달하고 있어?</p>
            <div class="c-tag">결과, 인지</div>
        </div>
    </div>
</div>
"""

think_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Think</strong>는 단순히 머리를 굴리는 것이 아닙니다.<br/>
        원어민에게 think는 <strong>'뇌 속에서 정보를 처리하여 의견이나 결론을 만들어내는 능동적인 과정'</strong>입니다.
    </div>

    <h2 class="insight-h2">Think의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Think</strong>의 핵심은</p>
        <div class="quote-text">"사고의 프로세스 가동 (Processing thoughts)"</div>
        <p>확실한 사실(Know)과는 다릅니다. 내 머릿속으로 판단하고 저울질하여 도출해 낸 주관적인 의견(Opinion)에 가깝습니다.</p>
    </div>

    <h2 class="insight-h2">① 주관적인 의견 (Opinion / Belief)</h2>
    <p class="insight-p">100% 팩트가 아니라 내 머릿속 프로세스를 거쳐 도출해 낸 '내 생각'을 말합니다.</p>
    <div class="example-group">
        <div class="ex-en">I think it's a good idea.</div>
        <div class="ex-ko">내 생각엔 좋은 아이디어 같아. (내 주관적 판단)</div>
    </div>
</div>
"""

feel_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Feel</strong>은 이성적인 판단(Think)과는 결이 다릅니다.<br/>
        원어민에게 feel은 <strong>'피부(촉각)나 가슴(감정)으로 직관적으로 와닿는 떨림이나 직감'</strong>입니다.
    </div>

    <h2 class="insight-h2">Feel의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Feel</strong>의 핵심은</p>
        <div class="quote-text">"직관적인 감각과 감정 (Sensation & Intuition)"</div>
        <p>논리적인 근거(Think)가 없어도 왠지 모르게 쎄하거나 긍정적으로 느껴질 때 직감적으로 사용합니다.</p>
    </div>

    <h2 class="insight-h2">① 감정 및 직감 (Intuition)</h2>
    <p class="insight-p">머리(뇌)가 아니라 가슴(감각)이 먼저 반응하는 본능적인 의견입니다.</p>
    <div class="example-group">
        <div class="ex-en">I feel like we should go.</div>
        <div class="ex-ko">왠지 우리 가야 할 것 같아. (논리적 근거보다 직감에 의존함)</div>
    </div>
</div>
"""

notice_html = """
<div class="insight-article">
    <div class="insight-intro">
        <strong>Notice</strong>는 일상에서 아주 빈도 높게 쓰이는 인지 동사입니다.<br/>
        원어민에게 notice는 <strong>'배경에 묻혀있던 무언가가 내 신경(레이더)에 띠리링 하고 걸리는 순간'</strong>입니다.
    </div>

    <h2 class="insight-h2">Notice의 핵심 이미지</h2>
    <div class="insight-box highlight-box">
        <p>원어민에게 <strong>Notice</strong>의 핵심은</p>
        <div class="quote-text">"레이더에 포착됨 / 알아차림 (Catching one's attention)"</div>
        <p>평소와 다른 미세한 변화(머리스타일, 기분 등)를 나의 예민한 감각으로 낚아채듯 알아차릴 때 사용합니다.</p>
    </div>

    <h2 class="insight-h2">① 미세한 변화의 포착 (Detecting change)</h2>
    <p class="insight-p">눈에 띄지 않던 것이 내 주의력에 들어와 인식되는 현상입니다.</p>
    <div class="example-group">
        <div class="ex-en">Did you notice her new haircut?</div>
        <div class="ex-ko">그녀 머리 자른 거 알아챘어? (변화가 네 레이더에 걸렸어?)</div>
    </div>
</div>
"""

def append_month3():
    with open('master/data/core_insights.js', 'r', encoding='utf-8') as f:
        content = f.read()

    last_brace_idx = content.rfind('}')
    if last_brace_idx != -1:
        prefix = content[:last_brace_idx].rstrip()
        if not prefix.endswith(','):
            prefix += ','
            
        new_content = prefix + f"""
    "Look": `{look_html}`,
    "See": `{see_html}`,
    "Watch": `{watch_html}`,
    "Listen": `{listen_html}`,
    "Hear": `{hear_html}`,
    "Think": `{think_html}`,
    "Feel": `{feel_html}`,
    "Notice": `{notice_html}`
}};
"""
        with open('master/data/core_insights.js', 'w', encoding='utf-8') as f:
            f.write(new_content)

if __name__ == "__main__":
    append_month3()
