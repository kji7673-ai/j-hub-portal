import sys
import re

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

interlude_md = """
### [막간] 재개발의 최전선: 욕망의 용광로에서 건축가는 무슨 생각을 하는가?

대한민국에서 '재개발/재건축'이라는 단어는 단순한 건축 행위를 넘어선다. 그것은 수천 명의 조합원, 수백억 원의 자산, 그리고 평생의 보금자리를 향한 날것의 욕망이 얽히고설킨 거대한 용광로다. 일반 대중의 눈에 비친 건축가는 그저 예쁜 조감도를 그리는 사람일지 모른다. 하지만 정비 사업의 최전선에 선 우리는, 매일같이 남의 전 재산이 걸린 지뢰밭을 걷는 기분으로 도면을 편다.

용적률 1%의 미세한 오차, 세대수 배치 모델링에서의 작은 실수가 조합원 개개인의 수천만 원 분담금 차이로 직결된다. 총회장에서는 고성이 오가고, 작은 숫자 하나에 사업의 존폐가 갈린다. 이 척박한 무대 위에서 건축가는 '예술가'라는 한가로운 타이틀을 내려놓아야 한다. 우리는 이해관계를 조율하는 '냉철한 판사'이자, 클라이언트의 피 같은 자산을 지켜내는 '숫자의 수호자'가 되어야만 한다.

그렇기에 우리는 휴먼 에러를 용납할 수 없었다. 단 한 번의 계산 실수로 수백억이 증발할 수 있는 이 아찔한 외줄 타기에서, 인간의 불완전한 엑셀 수작업에 누군가의 인생을 맡길 수는 없었다. 우리가 밤을 새워가며 기계(AI)를 학습시키고, 투명한 유리상자(J-Hub)를 구축해 데이터를 교차 검증하도록 만든 진짜 이유가 여기에 있다. 우리는 기계에게 일을 떠넘기기 위해 AI를 도입한 것이 아니다. 우리의 클라이언트, 즉 당신의 자산과 권리를 가장 완벽하게 지켜내기 위해 AI라는 무기를 벼려낸 것이다.

---

"""

# 1. Update MD
with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

target_heading = "## 5장. [Case 1] 정비 사업 통합 보고서 마법사: 신뢰를 증명하는 숫자의 위력"
md_text = md_text.replace(target_heading, interlude_md + target_heading)

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_text)


# 2. Update JS
with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

# We want to insert the new page object right before the chapter 5 page.
interlude_js = """        {
            "type": "text_only",
            "title": "[막간] 재개발의 최전선: 욕망의 용광로에서 건축가는 무슨 생각을 하는가?",
            "text": "대한민국에서 '재개발/재건축'이라는 단어는 단순한 건축 행위를 넘어선다. 그것은 수천 명의 조합원, 수백억 원의 자산, 그리고 평생의 보금자리를 향한 날것의 욕망이 얽히고설킨 거대한 용광로다. 일반 대중의 눈에 비친 건축가는 그저 예쁜 조감도를 그리는 사람일지 모른다. 하지만 정비 사업의 최전선에 선 우리는, 매일같이 남의 전 재산이 걸린 지뢰밭을 걷는 기분으로 도면을 편다.\\n\\n용적률 1%의 미세한 오차, 세대수 배치 모델링에서의 작은 실수가 조합원 개개인의 수천만 원 분담금 차이로 직결된다. 총회장에서는 고성이 오가고, 작은 숫자 하나에 사업의 존폐가 갈린다. 이 척박한 무대 위에서 건축가는 '예술가'라는 한가로운 타이틀을 내려놓아야 한다. 우리는 이해관계를 조율하는 '냉철한 판사'이자, 클라이언트의 피 같은 자산을 지켜내는 '숫자의 수호자'가 되어야만 한다.\\n\\n그렇기에 우리는 휴먼 에러를 용납할 수 없었다. 단 한 번의 계산 실수로 수백억이 증발할 수 있는 이 아찔한 외줄 타기에서, 인간의 불완전한 엑셀 수작업에 누군가의 인생을 맡길 수는 없었다. 우리가 밤을 새워가며 기계(AI)를 학습시키고, 투명한 유리상자(J-Hub)를 구축해 데이터를 교차 검증하도록 만든 진짜 이유가 여기에 있다. 우리는 기계에게 일을 떠넘기기 위해 AI를 도입한 것이 아니다. 우리의 클라이언트, 즉 당신의 자산과 권리를 가장 완벽하게 지켜내기 위해 AI라는 무기를 벼려낸 것이다."
        },
"""

target_js = """        {
            "type": "image_top",
            "title": "5장. [Case 1] 정비 사업 통합 보고서 마법사: 신뢰를 증명하는 숫자의 위력","""

js_text = js_text.replace(target_js, interlude_js + target_js)

# Do it for the second occurrence just in case? Actually book_data.js has duplicated array elements because of how I ran it earlier. Let's just replace all occurrences.

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Insertion of interlude successful.")
