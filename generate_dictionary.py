import json

dictionary = {
    "anymore": "부사. 더 이상 (~않다)",
    "seat": "명사. 자리, 좌석",
    "side": "명사. 편, 측면",
    "limit": "명사. 한계, 제한",
    "burst": "동사/명사. 터지다, 파열",
    "point": "명사. 요점, 의미",
    "matter": "동사. 중요하다 / 명사. 문제",
    "figure": "동사. 생각하다, 계산하다",
    "trouble": "명사. 곤란, 문제",
    "mind": "명사. 마음, 정신 / 동사. 언짢아하다",
    "decision": "명사. 결정",
    "promise": "명사. 약속 / 동사. 약속하다",
    "effort": "명사. 노력, 수고",
    "courage": "명사. 용기",
    "medicine": "명사. 약, 의학",
    "breath": "명사. 숨, 호흡",
    "breathe": "동사. 숨쉬다",
    "hungry": "형용사. 배고픈",
    "score": "명사. 점수 / 동사. 득점하다",
    "wrong": "형용사. 틀린, 잘못된",
    "crazy": "형용사. 미친, 말도 안 되는",
    "vision": "명사. 시력, 시야, 환상",
    "deterioration": "명사. 악화, 하락",
    "improvement": "명사. 향상, 개선",
    "position": "명사. 입장, 위치",
    "ease": "명사. 편안함, 쉬움",
    "expression": "명사. 표현, 표정",
    "alarm": "명사. 알람, 불안",
    "goal": "명사. 목표",
    "rule": "명사. 규칙",
    "umbrella": "명사. 우산",
    "responsibility": "명사. 책임, 의무",
    "disease": "명사. 질병, 병",
    "attention": "명사. 주의, 주목",
    "appearance": "명사. 겉모습, 외모",
    "perception": "명사. 지각, 자각",
    "monitor": "동사. 추적 관찰하다 / 명사. 화면",
    "intentional": "형용사. 의도적인",
    "opinion": "명사. 의견, 견해",
    "intuition": "명사. 직관, 직감",
    "detect": "동사. 발견하다, 감지하다",
    "accomplished": "형용사. 기량이 뛰어난, 성취한",
    "afraid": "형용사. 두려워하는",
    "angry": "형용사. 화난",
    "anxious": "형용사. 불안해하는",
    "anyway": "부사. 어쨌든, 아무튼",
    "awkward": "형용사. 어색한, 서투른",
    "burned": "형용사. 데인, 타버린 (burned out: 방전된)",
    "confused": "형용사. 혼란스러운",
    "reconsider": "동사. 재고하다, 다시 생각하다",
    "determined": "형용사. 단호한, 결연한",
    "disappointed": "형용사. 실망한",
    "discouraged": "형용사. 낙담한",
    "driven": "형용사. 의욕이 넘치는",
    "exactly": "부사. 정확히, 틀림없이",
    "excited": "형용사. 신난, 흥분한",
    "exhausted": "형용사. 기진맥진한",
    "fair": "형용사. 타당한, 공정한",
    "focused": "형용사. 집중한",
    "fulfilled": "형용사. 성취감을 느끼는",
    "furious": "형용사. 몹시 화가 난",
    "shot": "명사. 시도 (give it a shot: 한번 해보다)",
    "glad": "형용사. 기쁜",
    "grateful": "형용사. 감사하는",
    "homesick": "형용사. 향수병에 걸린",
    "argue": "동사. 주장하다, 논쟁하다",
    "imagine": "동사. 상상하다",
    "meantime": "명사. 그 동안 (in the meantime: 그러는 동안에)",
    "depends": "동사. ~에 달려있다 (It depends: 상황에 따라 다르다)",
    "let": "동사. 허락하다 (let down: 실망시키다)",
    "lost": "형용사. 길을 잃은, 상실한",
    "mad": "형용사. 몹시 화난",
    "mastery": "명사. 통달, 숙달",
    "nervous": "형용사. 긴장한, 초조한",
    "worries": "명사. 걱정거리 (no worries: 걱정 마)",
    "nostalgic": "형용사. 향수를 불러일으키는",
    "necessarily": "부사. 필연적으로, 반드시",
    "edge": "명사. 가장자리 (on edge: 불안하여, 곤두서서)",
    "overwhelmed": "형용사. 압도된",
    "pleased": "형용사. 기쁜, 만족스러운",
    "proud": "형용사. 자랑스러운",
    "pumped": "형용사. 아주 신난, 열정적인",
    "puzzled": "형용사. 어리둥절한",
    "rapid": "형용사. 빠른, 신속한",
    "realize": "동사. 깨닫다",
    "recognize": "동사. 알아보다, 인정하다",
    "relieved": "형용사. 안도하는",
    "scared": "형용사. 겁먹은",
    "sentimental": "형용사. 감상적인",
    "sort": "명사. 종류 (sort of: 어느 정도, 꽤)",
    "stressed": "형용사. 스트레스를 받는",
    "terrified": "형용사. 몹시 두려워하는",
    "thankful": "형용사. 감사하는",
    "thrilled": "형용사. 황홀한, 아주 신난",
    "uncomfortable": "형용사. 불편한",
    "uneasy": "형용사. 불안한, 우려되는",
    "worn": "형용사. 닳은 (worn out: 몹시 지친)",
    "prefer": "동사. 선호하다",
    "anyway": "부사. 어쨌든",
    "sense": "명사. 일리, 의미 (make sense: 말이 되다)"
}

js_code = "window.globalDictionary = " + json.dumps(dictionary, ensure_ascii=False, indent=4) + ";"

with open('master/data/dictionary.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

dictionary["pride"] = "명사. 자부심, 자랑 (take pride in: ~에 자부심을 가지다)"
dictionary["turn"] = "명사. 차례, 순서 (take turns: 교대로 하다)"
dictionary["aback"] = "부사. 깜짝 놀라 (taken aback: 깜짝 놀라다, 당황하다)"
dictionary["immediately"] = "부사. 즉시, 즉각"
dictionary["action"] = "명사. 조치, 행동 (take action: 조치를 취하다)"
dictionary["down"] = "부사. 아래로 (take down: 적어두다, 끌어내리다)"
dictionary["number"] = "명사. 번호, 숫자"
dictionary["work"] = "명사. 일, 직장"
dictionary["quite"] = "부사. 꽤, 상당히"

js_code = "window.globalDictionary = " + json.dumps(dictionary, ensure_ascii=False, indent=4) + ";"
with open('master/data/dictionary.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
