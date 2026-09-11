import sys

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

# --- PROLOGUE UPDATE ---
prologue_addition_md = """

**이 책은 단순히 '건축'에 관한 책이 아니다.** 
AI가 인간의 지적 노동을 대체한다는 공포가 엄습하는 지금, 이것은 전 산업군의 모든 비즈니스맨을 위한 '생존 바이블'이다. 어떻게 기계에게 단순 연산과 잡무를 완벽하게 떠넘기고, 인간만이 할 수 있는 '진짜 결정(여백)'의 통제권을 되찾을 것인가? 수백억 원의 자산과 욕망이 충돌하는 재개발 판에서, 우리가 피 튀기게 증명해 낸 이 AI 협업의 철학이 당신의 일터에도 완벽한 해답이 되어 줄 것이다."""

prologue_addition_js = "\\n\\n**이 책은 단순히 '건축'에 관한 책이 아니다.**\\nAI가 인간의 지적 노동을 대체한다는 공포가 엄습하는 지금, 이것은 전 산업군의 모든 비즈니스맨을 위한 '생존 바이블'이다. 어떻게 기계에게 단순 연산과 잡무를 완벽하게 떠넘기고, 인간만이 할 수 있는 '진짜 결정(여백)'의 통제권을 되찾을 것인가? 수백억 원의 자산과 욕망이 충돌하는 재개발 판에서, 우리가 피 튀기게 증명해 낸 이 AI 협업의 철학이 당신의 일터에도 완벽한 해답이 되어 줄 것이다."


# --- CHAPTER 5 INSIGHT UPDATE ---
insight_md = """

### 💡 [Universal Insight] 당신의 업계에도 '신통기획' 같은 딜레마가 있는가?

우리가 건축 현장에서 겪은 '무료 기획설계의 딜레마'는 비단 건축 업계만의 이야기가 아니다. 마케팅, 컨설팅, IT 개발, 디자인 등 모든 지식 서비스 산업에는 고객이 '빠르고 저렴한(또는 무료인) 초기 시안'을 요구하는 병목 구간이 존재한다. 이 초기 결과물이 훗날의 거대한 본계약을 좌우하기 때문에, 당신은 울며 겨자 먹기로 직원들의 야근을 갈아 넣어 퀄리티를 맞춘다.

이 잔인한 딜레마를 깨부수는 유일한 방법은 **'나만의 J-Hub'를 구축하는 것**이다. 
당신의 업무에서 '데이터 수집'과 '단순 반복 연산(엑셀, 리서치)'이 차지하는 80%의 시간을 AI에게 위임하라. 그리고 당신은 남은 20%의 시간 동안 고객의 욕망을 조율하고, 프로젝트에 철학을 불어넣는 '진짜 지휘자'의 역할에만 집중하라. 기계가 완벽한 숫자를 증명하고 당신이 철학을 더할 때, 당신은 비로소 가격 경쟁력의 늪에서 빠져나와 **대체 불가능한 진짜 전문가**로 거듭날 것이다.
"""

insight_js = """        {
            "type": "text_only",
            "title": "💡 [Universal Insight] 당신의 업계에도 '신통기획' 같은 딜레마가 있는가?",
            "text": "우리가 건축 현장에서 겪은 '무료 기획설계의 딜레마'는 비단 건축 업계만의 이야기가 아니다. 마케팅, 컨설팅, IT 개발, 디자인 등 모든 지식 서비스 산업에는 고객이 '빠르고 저렴한(또는 무료인) 초기 시안'을 요구하는 병목 구간이 존재한다. 이 초기 결과물이 훗날의 거대한 본계약을 좌우하기 때문에, 당신은 울며 겨자 먹기로 직원들의 야근을 갈아 넣어 퀄리티를 맞춘다.\\n\\n이 잔인한 딜레마를 깨부수는 유일한 방법은 **'나만의 J-Hub'를 구축하는 것**이다. \\n당신의 업무에서 '데이터 수집'과 '단순 반복 연산(엑셀, 리서치)'이 차지하는 80%의 시간을 AI에게 위임하라. 그리고 당신은 남은 20%의 시간 동안 고객의 욕망을 조율하고, 프로젝트에 철학을 불어넣는 '진짜 지휘자'의 역할에만 집중하라. 기계가 완벽한 숫자를 증명하고 당신이 철학을 더할 때, 당신은 비로소 가격 경쟁력의 늪에서 빠져나와 **대체 불가능한 진짜 전문가**로 거듭날 것이다."
        },
"""


# 1. Update MD
with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

# Inject into Prologue
old_prologue_end = "이 책은 그 절망의 끝에서 우리 정린이 찾아낸, 처절하지만 가장 현실적인 '생존에 관한 보고서'다."
md_text = md_text.replace(old_prologue_end, old_prologue_end + prologue_addition_md)

# Inject after Chapter 5
old_ch5_end = "결국 플랫폼이 곧 회사의 경쟁력이다. 정비 사업 통합 보고서 마법사는 우리에게 야근 없는 저녁을 선물한 것을 넘어, 철저한 숫자의 증명으로 수백억 원의 딜을 성사시키는 우리의 가장 강력한 최전방 공격수가 되었다."
md_text = md_text.replace(old_ch5_end, old_ch5_end + "\n" + insight_md)

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_text)


# 2. Update JS
with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

# Inject into Prologue (JS)
old_prologue_end_js = "이 책은 그 절망의 끝에서 우리 정린이 찾아낸, 처절하지만 가장 현실적인 '생존에 관한 보고서'다."
js_text = js_text.replace(old_prologue_end_js, old_prologue_end_js + prologue_addition_js)

# Inject after Chapter 5 (JS)
# We need to find the object that ends Chapter 5 and insert a new object after it.
# The end of Chapter 5 page in JS starts with "결과가 아닌 '과정'이 신뢰를 만든다"
target_page_js = """        {
            "type": "image_top",
            "title": "",
            "text": "이 압도적인 12장짜리 <용문동 타당성 검토 보고서>를 받아 든 클라이언트의 반응은 굳이 설명할 필요가 없었다.\\n\\n단순히 결과(세대수)만 덜렁 적힌 것이 아니라, 어떤 법조항(빈집특례법 등)을 근거로 가산 용적률을 얻어냈는지, 현금청산 시나리오와 대지 축소 방안 중 왜 전자가 압도적으로 유리한지 그 **'도출 과정(Process)' 전체가 투명하게 증명**되어 있었기 때문이다. 클라이언트는 이 보고서를 통해 자신의 수천억 원대 자산이 가장 안전하고 완벽하게 분석되고 있음을 확인했다. 의심은 무한한 신뢰로 바뀌었다.\\n\\n결국 플랫폼이 곧 회사의 경쟁력이다. 정비 사업 통합 보고서 마법사는 우리에게 야근 없는 저녁을 선물한 것을 넘어, 철저한 숫자의 증명으로 수백억 원의 딜을 성사시키는 우리의 가장 강력한 최전방 공격수가 되었다.\\n\\n---",
            "image": "static/images/42.jpg"
        },"""

js_text = js_text.replace(target_page_js, target_page_js + "\n" + insight_js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Bestseller strategy successfully applied.")
