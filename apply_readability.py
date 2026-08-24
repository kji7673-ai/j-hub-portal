import sys
import re

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

c1_target = "이 책은 그 부끄러운 절망의 끝에서 우리 진양건축이 수많은 시행착오 끝에 찾아낸, 따뜻하지만 단단한 '생존에 관한 보고서'다."
c1_add = """

> **💡 [J-Insight] 바쁜 독자를 위한 1분 요약 (프롤로그)**
> - **위기**: 엑셀과 야근에 의존하는 기존 방식으로는 복잡한 정비사업에서 생존할 수 없다.
> - **해답**: 기술(AI)을 통해 데이터를 정복하되, 그 중심에는 항상 '사람'이 있어야 한다.
> - **이 책의 목적**: 실전에서 깨지며 완성한 진양건축만의 생존 기록을 공유한다."""

c3_target = "그렇게 우리는 정보의 파편화라는 늪에서 서서히 빠져나오기 시작했다."
c3_add = """

> **💡 [J-Insight] 바쁜 독자를 위한 1분 요약 (정보의 자산화)**
> - **문제**: 개인의 머릿속에만 갇혀 있는 정보(암묵지)는 회사의 자산이 될 수 없으며 조직을 병들게 한다.
> - **해결**: 모든 통화, 회의록, 아이디어를 하나의 플랫폼(J-Hub)에 쏟아부어야 한다.
> - **결과**: 에이스 직원 한 명에게 의존하던 구조에서 벗어나, 조직 전체가 거대한 지식 자산을 보유하게 된다."""

c5_target = "클라이언트는 우리의 진심에 깊이 공감하고 손을 내밀어 주었다. AI가 만들어낸 압도적인 퀄리티가 '출혈 경쟁'의 판을 뒤엎고 '정당한 대가'를 받아낸 것이다."
c5_new = """클라이언트는 우리의 진심에 깊이 공감하고 손을 내밀어 주었다. 보수적인 조합장이 유료 계약서에 도장을 찍었던 결정적인 이유는 단지 철학이 훌륭해서가 아니었다. 

*“조합장님, 기존 방식으로는 용적률 290%가 한계입니다. 하지만 AI로 수십 개의 대안(Alts)을 돌려본 결과, 북측 일조 사선(햇빛을 가리지 않게 건물을 깎는 규제)을 빗겨가는 최적의 아파트 건물 덩어리(주동) 배치를 찾아내 용적률 2%를 추가로 확보할 수 있습니다. 이는 조합원님들의 분담금을 수십억 원 이상 절감시키는 결과입니다.”*

눈앞에서 AI가 인간이 놓친 '숨겨진 이익'을 찾아내고, 그것이 곧바로 조합원들의 수십억 원짜리 분담금 절감으로 환산되는 것을 확인한 순간, 그들은 완벽하게 납득했다. AI가 만들어낸 압도적이고 실질적인 가치가 '무료 출혈 경쟁'의 판을 뒤엎고 '정당한 대가'를 받아낸 것이다."""

c6_target = "끊임없는 땜질과 리더의 지독한 인내로 완성된다는 것을 나는 뼈저리게 배우고 있다."
c6_add = """

> **💡 [J-Insight] 바쁜 독자를 위한 1분 요약 (시스템과 리더십)**
> - **오해**: 완벽한 시스템이 조직을 하루아침에 바꿀 것이라는 착각.
> - **현실**: 익숙한 과거의 방식과 낯선 미래의 방식(J-Hub)은 과도기적으로 병행될 수밖에 없다.
> - **리더의 역할**: 일방적 강요가 아닌, 직원 스스로 가치를 깨달을 때까지 묵묵히 시스템을 고도화하며 기다려주는 인내다."""

def apply_updates(filepath, is_js=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if is_js:
        text = text.replace(c1_target, c1_target + c1_add.replace("\n", "\\n"))
        text = text.replace(c3_target, c3_target + c3_add.replace("\n", "\\n"))
        text = text.replace(c5_target, c5_new.replace("\n\n", "\\n\\n").replace("\n", "\\n"))
        text = text.replace(c6_target, c6_target + c6_add.replace("\n", "\\n"))
    else:
        text = text.replace(c1_target, c1_target + c1_add)
        text = text.replace(c3_target, c3_target + c3_add)
        text = text.replace(c5_target, c5_new)
        text = text.replace(c6_target, c6_target + c6_add)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

apply_updates(md_path, False)
apply_updates(js_path, True)
print("Readability enhancement applied successfully.")
