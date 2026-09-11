import sys
import re

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

# 1. Resistance & Security
res_orig = "단일 출구로 설계했다. 직원들의 로컬 PC에서 임의로 PDF를 변환해 발송하는 행위를 차단하고, 외부로 나가는 모든 공문과 보고서는 반드시 J-Hub 웹 에디터를 거치도록 강제했다."
res_new = """단일 출구로 설계했다. 물론 그 과정은 결코 순탄치 않았다. 자유롭고 예술적인 성향이 강한 건축가들에게 모든 공문 발송과 회의록 작성을 통제하는 IT 시스템을 강제하자, 초기에는 "우리가 기계 부속품이냐"며 뼈아픈 반발과 퇴사까지 이어지는 진통을 겪어야 했다. 게다가 회사의 15년 치 1급 기밀인 암묵지가 외부 AI 망으로 유출될 수 있다는 경영진의 공포도 컸다. 우리는 이 두 가지 저항을 극복하기 위해 외부망과 완벽히 차단된 '보안 폐쇄망 아키텍처'를 구축했고, 리더가 먼저 직접 시스템을 쓰며 직원들을 설득하는 피눈물 나는 섀도우 복싱의 시간을 거쳐야만 했다.

치열한 내부 진통 끝에, 우리는 직원들의 로컬 PC에서 임의로 PDF를 변환해 발송하는 행위를 원천 차단하고, 외부로 나가는 모든 공문과 보고서는 반드시 J-Hub 웹 에디터를 거치도록 강제했다."""

# 2. Client Trust
trust_orig = "계약서**에 도장을 찍었다. AI가 만들어낸 압도적인 퀄리티가 '출혈 경쟁'의 판을 뒤엎고 '정당한 대가'를 받아낸 것이다."
trust_new = "계약서**에 도장을 찍었다. 사실 보수적인 재건축 현장의 연세 많은 조합장들은 기계가 찍어낸 화려한 숫자를 불신하는 경향이 짙다. \"이거 그냥 컴퓨터가 대충 찍어낸 가짜 숫자 아냐?\"라는 그들의 서늘한 의심을 무너뜨린 것은, 다름 아닌 그 AI의 데이터를 **'진양건축의 25년 현장 경험'이 담긴 인간의 언어로 통역하여 설득**했기 때문이었다. AI가 뽑아낸 데이터를 인간의 직관으로 얹어 치열하게 브리핑했을 때, 비로소 클라이언트는 완벽하게 굴복했다. AI가 만들어낸 압도적인 퀄리티가 '출혈 경쟁'의 판을 뒤엎고 '정당한 대가'를 받아낸 것이다."

# 3. Homogenization
homo_orig = "단 하나의 공간을 인지적으로 **'선택(Choice)'**하는 것. \n\n그것이 바로 미래의 건축이다."
homo_new = "단 하나의 공간을 인지적으로 **'선택(Choice)'**하는 것. 숫자와 법규에 최적화된 기계가 100개의 대안을 짜봤자 자칫하면 가장 가성비 좋은 '붕어빵 성냥갑 아파트'가 튀어나오기 십상이다. AI는 어디까지나 용적률과 법적 한계선이라는 차가운 뼈대를 잡을 뿐이다. 그 위에 벽돌의 질감, 파사드(입면)의 비례, 사람이 걷고 머무는 동선이라는 **'따뜻한 온기(디자인의 영혼)'를 입히는 것은 철저히 기계의 개입을 차단한 인간 건축가만의 고유 영역**이다.\n\n그것이 바로 미래의 건축이다."

# Also need JS string matching (escaped newlines)
homo_orig_js = "단 하나의 공간을 인지적으로 **'선택(Choice)'**하는 것.\\n\\n그것이 바로 미래의 건축이다."
homo_new_js = "단 하나의 공간을 인지적으로 **'선택(Choice)'**하는 것. 숫자와 법규에 최적화된 기계가 100개의 대안을 짜봤자 자칫하면 가장 가성비 좋은 '붕어빵 성냥갑 아파트'가 튀어나오기 십상이다. AI는 어디까지나 용적률과 법적 한계선이라는 차가운 뼈대를 잡을 뿐이다. 그 위에 벽돌의 질감, 파사드(입면)의 비례, 사람이 걷고 머무는 동선이라는 **'따뜻한 온기(디자인의 영혼)'를 입히는 것은 철저히 기계의 개입을 차단한 인간 건축가만의 고유 영역**이다.\\n\\n그것이 바로 미래의 건축이다."

res_new_js = res_new.replace("\n\n", "\\n\\n")

def apply_fixes(file_path, is_js=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if is_js:
        text = text.replace(res_orig, res_new_js)
        text = text.replace(trust_orig, trust_new)
        text = text.replace(homo_orig_js, homo_new_js)
    else:
        text = text.replace(res_orig, res_new)
        text = text.replace(trust_orig, trust_new)
        text = text.replace(homo_orig, homo_new)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

apply_fixes(md_path, is_js=False)
apply_fixes(js_path, is_js=True)

print("Red Team V2 injection completed successfully.")
