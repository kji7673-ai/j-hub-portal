import re

with open('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/full_book_text_final_v2.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Split the text by themes
# We know the markers are: "## ◆ 테마 1: 내가 무엇인가" etc.

intro_1 = """## [도입] 테마 1: 내가 무엇인가 - "공유결합의 첫 질문"

공유결합의 첫 번째 조건: "자기 자신을 안다"는 것입니다.

설계가 무엇인가요? 
도면을 그리는 것일까요? 아니면 공간을 만드는 것일까요?

저는 26년을 현장에서 뒹굴며 이제야 조금 알 것 같습니다. 
설계는 결국 "자기 자신이 무엇인지 아는" 과정에서 시작된다는 것을요.

나는 무엇을 원하는 사람인가?
나는 어떤 가치를 지키려는 사람인가?
나는 왜 도면 위에 이 선을 이렇게 그었는가?

이 질문들에 스스로 답할 수 없으면, 도면은 그저 남의 생각을 베낀 흉내에 불과합니다. 법규를 맞추고 수지분석을 통과할 수는 있어도, 그 안에 건축가의 영혼은 깃들지 않습니다.

아래에 이어지는 현장의 일기들은, 저 자신이 누구인지 끊임없이 자문하며 남긴 기록들입니다. 
항상 정답을 아는 완벽한 전문가로서가 아니라, 부족함을 느끼고 흔들리며, 때로는 현장의 거친 먼지 속에서 무력감을 느끼는 한 인간의 기록입니다. 
자신의 찌질함과 연약함을 마주할 용기가 있을 때 비로소 우리는 타인과 결합할 수 있는 빈 공간(여백)을 가지게 됩니다.

이 기록들 속에서, 공유결합의 가장 밑바탕이 되는 첫 번째 조건 — '나를 마주하는 시간'을 느껴보시기 바랍니다.
"""

intro_2 = """## [도입] 테마 2: 상대를 아는 것 - "공유결합의 두 번째 질문"

나를 비우고 나면, 그 빈자리에 누군가를 채울 수 있는 여유가 생깁니다.
이것이 공유결합의 두 번째 조건, 바로 "상대를 아는 것"입니다.

건축은 결코 혼자 하는 예술이 아닙니다. 
내가 그은 선 하나가 누군가의 평생의 전 재산이 걸린 집이 되고, 누군가가 매일 아침 눈을 뜨는 방이 됩니다. 
조합원들의 불안한 눈빛, 시공사의 차가운 계산기, 인허가권자의 굳은 표정… 이 모든 '상대'들을 온전히 껴안지 못하면 건축은 탁상공론에 머물고 맙니다.

상대를 안다는 것은 단순히 그들의 요구사항을 체크리스트로 만드는 것이 아닙니다.
그들이 왜 화를 내는지, 왜 두려워하는지, 그 이면에 감춰진 진짜 욕망과 결핍을 읽어내는 일입니다.

때로는 부딪히고, 때로는 설득하며, 때로는 묵묵히 져주었던 시간들.
나의 선이 상대의 삶과 닿아 스파크가 튀던 그 치열했던 교감의 기록들을 펼쳐봅니다.
"""

intro_3 = """## [도입] 테마 3: 현장의 맥락 읽기 - "공유결합의 세 번째 질문"

나를 알고 상대를 알았다면, 이제 우리는 우리가 발 딛고 있는 '땅'을 보아야 합니다.
공유결합의 세 번째 조건, "현장의 맥락을 읽는 것"입니다.

아무리 완벽한 도면이라도 현장의 흙바닥 위에서는 무력해질 때가 있습니다.
예상치 못한 암반이 튀어나오고, 옆 건물의 민원이 쏟아지며, 비바람에 자재가 망가집니다. 
데이터와 AI는 모니터 안에서 완벽한 기하학을 만들어 내지만, 그 기하학이 현실에 안착하기 위해서는 반드시 현장의 거친 숨결과 타협해야 합니다.

현장은 시스템이 아닙니다. 현장은 살아 숨 쉬는 유기체입니다.
도면 위에 그려진 선이 실제 콘크리트와 철근으로 변환되는 과정에는 수많은 사람의 땀과 변수가 엉켜 있습니다. 
완벽함을 고집하기보다 현실의 불완전함을 기꺼이 받아들이고 조화시키는 것.

이 장의 기록들은 책상머리의 기획이 현장이라는 거대한 현실과 부딪치며 깎이고 다듬어지는, 
진짜 '짓는' 행위에 대한 생생한 증언입니다.
"""

intro_4 = """## [도입] 테마 4: 공유결합의 순간들 - "신뢰가 만들어지는 현장"

나, 상대, 그리고 현장. 
이 세 가지 불완전한 요소들이 만나 비로소 하나의 완전한 결합을 이루어냅니다.
이것이 바로 '공유결합의 순간'입니다.

이 결합을 묶어주는 유일한 접착제는 다름 아닌 '신뢰'입니다. 
기계적인 계약 관계나 차가운 데이터 교환으로는 절대 만들어낼 수 없는, 사람과 사람 사이의 끈끈한 연대.
서로의 약점을 덮어주고, 공동의 목표를 향해 기꺼이 헌신할 때, 비로소 도면은 생명을 얻고 건물이 됩니다.

이 마지막 테마에서는 앞선 모든 질문과 고민들이 어떻게 실제 현장에서 아름다운 결실(혹은 뼈아픈 교훈)로 맺어지는지 보여줍니다.
시스템 너머의 본질, 기계가 결코 대체할 수 없는 인간 건축가만의 고귀한 역할이 바로 이 결합을 지휘하는 데 있음을 확인하시게 될 것입니다.
"""

# We need to process the file and replace introductions, insert bridges, and change transitions.
import sys

# A helper function to insert bridges into a list of essays
def process_theme(theme_text, intro_text, theme_idx):
    # Separate the intro part from the essays
    # Essays start with "### [기록"
    parts = re.split(r'(### \[기록 \d+\])', theme_text)
    
    if len(parts) < 3:
        return theme_text # No essays found
        
    before_essays = parts[0]
    # Replace the old intro with the new intro
    before_essays = re.sub(r'## \[도입\] ◆ 테마 \d+:.*?(?=\n\n|\Z)', intro_text, before_essays, flags=re.DOTALL)
    
    new_text = intro_text + "\n\n"
    
    essays = []
    for i in range(1, len(parts), 2):
        essays.append(parts[i] + parts[i+1])
        
    # Inject bridges
    for i, essay in enumerate(essays):
        new_text += essay
        # After every 5 essays, add a bridge, except after the last one
        if (i + 1) % 6 == 0 and i != len(essays) - 1:
            bridge_idx = (i + 1) // 6
            bridge_title = f"## [성찰 {theme_idx}-{bridge_idx}]"
            
            if theme_idx == 1:
                bridge = f"\n{bridge_title}\n\n위의 일기들을 읽으며 어떤 감정이 드셨습니까?\n\n불안, 부끄러움, 초조함, 그리고 인정받고 싶은 갈망.\n이 모든 날것의 감정들은 우리가 전문가라는 가면 뒤에 숨겨둔 진짜 내 모습입니다.\n나의 약함을 덮기 위해 더 완벽한 척할 때, 우리는 고립됩니다. 하지만 나의 부족함을 인정하고 마주하는 순간, 비로소 타인에게 다가갈 수 있는 빈틈이 열립니다. \n\n이것이 건축 설계에서, 아니 모든 인간관계에서 공유결합이 시작되는 지점입니다.\n\n---\n\n"
            elif theme_idx == 2:
                bridge = f"\n{bridge_title}\n\n도면을 그리는 일은 결국 '타인을 상상하는 일'입니다.\n\n우리가 만나는 수많은 상대방은 각자의 이기심과 상처를 안고 우리 앞에 섭니다.\n그들의 날 선 말과 억지스러운 요구 뒤에 숨은 진짜 불안을 읽어낼 때, 도면은 비로소 문제 해결의 열쇠가 됩니다. \n\n상대를 안다는 것은 그들을 내 뜻대로 통제하는 것이 아니라, 그들의 이야기에 기꺼이 귀를 내어주고 나의 선과 그들의 삶을 동기화시키는 과정입니다.\n\n---\n\n"
            elif theme_idx == 3:
                bridge = f"\n{bridge_title}\n\n모니터 앞에서의 설계는 완벽합니다. 하지만 현장에서는 모든 것이 달라집니다.\n\n도면이 현실로 번역되는 과정에서 발생하는 수많은 마찰음들. 그것은 실패가 아니라, 도면이 현실의 맥락과 결합하며 생명력을 얻는 소리입니다.\n기계는 이 마찰을 '오류'라 부르며 제거하려 하지만, 인간 건축가는 이 마찰을 '현장의 맥락'으로 포용하며 설계를 완성해 나갑니다.\n\n현장은 정답을 강요하는 곳이 아니라, 최선의 타협을 찾아가는 유연한 공간입니다.\n\n---\n\n"
            else:
                bridge = f"\n{bridge_title}\n\n결국 남는 것은 사람입니다.\n\n치열했던 회의, 흙먼지 날리던 현장, 밤을 지새우며 고쳤던 도면들. 그 모든 과정의 끝에서 우리가 얻어내는 것은 단순한 건축물이 아니라, 서로를 향한 '신뢰'입니다.\n\n완벽하지 않은 사람들이 모여 서로의 여백을 채워주며 만들어내는 이 공유결합의 순간이야말로, 기계가 결코 흉내 낼 수 없는 인간만의 위대한 성취입니다.\n\n---\n\n"
            
            new_text += bridge
            
    # Remove the old [성찰] part from the end if it exists in the last piece, but actually we split by essays.
    # The last essay might have the old 성찰 appended to it.
    last_essay = essays[-1]
    last_essay = re.sub(r'## \[성찰\] ◆ 테마 \d+:.*', '', last_essay, flags=re.DOTALL)
    
    # We will add the transition instead.
    if theme_idx == 1:
        transition = "\n\n### [테마 1 성찰 및 전환]\n\n나를 아는 고통스러운 과정을 통과해야만 우리는 어떤 선(Line)에 진심을 담을 수 있습니다.\n\n**→ 그렇다면 다음 질문은 자연스럽게 이어집니다.**\n\n\"내가 누구인지 알았다면, 이제 나의 선이 닿아야 할 '상대'는 도대체 어떤 사람들인가?\"\n"
    elif theme_idx == 2:
        transition = "\n\n### [테마 2 성찰 및 전환]\n\n상대의 마음을 열고 그들의 삶을 도면 위에 올려놓는 법을 배웠습니다.\n\n**→ 질문은 다시 확장됩니다.**\n\n\"나와 상대가 마음을 모아 그린 이 도면이, 실제 콘크리트와 흙바닥이 기다리는 '현장'과 만날 때 어떤 일이 벌어질 것인가?\"\n"
    elif theme_idx == 3:
        transition = "\n\n### [테마 3 성찰 및 전환]\n\n책상머리의 완벽함이 현장의 불완전함과 타협하며 비로소 진짜 건축이 되는 과정을 보았습니다.\n\n**→ 이제 우리는 마지막 결론을 향해 갑니다.**\n\n\"나의 진심, 상대의 삶, 그리고 현장의 맥락... 이 세 가지 불완전함이 하나로 맞물려 빚어내는 '결합의 순간'은 어떤 모습일까?\"\n"
    else:
        transition = "\n\n### [테마 4 성찰]\n\n결국 기계의 연산이 끝난 곳에서, 인간의 위대한 통찰과 신뢰가 시작됩니다. \n우리가 지켜야 할 것은 도면의 완벽함이 아니라, 사람과 사람이 맺어지는 이 '공유결합'의 숭고한 과정입니다.\n"

    # Replace the last essay with its clean version + transition
    new_text = new_text.rsplit('### [기록', 1)[0] + '### [기록' + last_essay + transition
    return new_text

# Split full text into themes
themes = re.split(r'(## ◆ 테마 \d+:.*?)(?=\n## |$)', text, flags=re.DOTALL)
# parts: [before_theme_1, theme_1_title, theme_1_body, theme_2_title, theme_2_body, ...]

if len(themes) < 9:
    print("Could not find all themes")
    sys.exit(1)

new_full_text = themes[0]

for idx in range(1, 5):
    theme_title = themes[2*idx - 1]
    theme_body = themes[2*idx]
    
    if idx == 1: intro = intro_1
    elif idx == 2: intro = intro_2
    elif idx == 3: intro = intro_3
    else: intro = intro_4
    
    processed_body = process_theme(theme_body, intro, idx)
    new_full_text += theme_title + processed_body

# Re-append anything after theme 4
# Actually, re.split might leave the rest in the last theme body, let's make sure Part 3 is preserved.
# Wait, "## 3부:" is in the text. Does re.split capture it?
# My regex `(?=\n## |$)` stops at ANY `## `.
# Let's refine the split to only stop at `## ◆ 테마` or `## 3부`

# Let's just use string finding.
parts = text.split("## ◆ 테마 1: 내가 무엇인가")
part1 = parts[0]
rest = "## ◆ 테마 1: 내가 무엇인가" + parts[1]

part2, part3 = rest.split("# 3부:", 1)
part3 = "\n# 3부:" + part3

t1, t2_rest = part2.split("## ◆ 테마 2: 상대를 아는 것")
t2, t3_rest = t2_rest.split("## ◆ 테마 3: 현장의 맥락 읽기")
t3, t4_rest = t3_rest.split("## ◆ 테마 4: 공유결합의 순간들")
t4 = t4_rest

new_t1 = process_theme(t1, intro_1, 1)
new_t2 = process_theme(t2, intro_2, 2)
new_t3 = process_theme(t3, intro_3, 3)
new_t4 = process_theme(t4, intro_4, 4)

new_full_text = part1 + "## ◆ 테마 1: 내가 무엇인가\n" + new_t1 + "## ◆ 테마 2: 상대를 아는 것\n" + new_t2 + "## ◆ 테마 3: 현장의 맥락 읽기\n" + new_t3 + "## ◆ 테마 4: 공유결합의 순간들\n" + new_t4 + part3

with open('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/full_book_text_final_v3.md', 'w', encoding='utf-8') as f:
    f.write(new_full_text)

print("Saved to full_book_text_final_v3.md")
