import json
import re

# Read the file content
with open('book_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# The episode 1 text
episode_1_text = """2019년 9월, 대전 유성 장대B구역 재개발사업 현상설계.
내가 진양건축의 본부장으로 부임한 뒤 처음으로 지휘한 현상설계였다.

상대사는 토문건축(300명 규모)과 정림건축(200명 규모).
당시 진양의 전체 직원은 고작 20명 남짓이었다. 골리앗과 다윗의 싸움조차 되지 않는 체급 차이. 단독으로는 명함조차 내밀 수 없었기에, 200명 규모의 유선엔지니어링과 컨소시엄을 맺고 그들의 사무실로 우리 직원 4명을 파견 보냈다.

"좋은 경험이 될 겁니다."
주변에서 내게 던지는 위로 섞인 말들은, 사실상 우리의 패배를 기정사실화하고 있었다. 현상설계를 단 한 번도 해본 적 없는 4명의 직원들과 함께, 나는 그 낯선 사무실에서 지독하게 외롭고 고단한 밤들을 견뎌야 했다.

하지만 우리는 물러서지 않았다. 
파견 나간 4명의 직원들은 매일 새벽 2~3시까지 악착같이 도면을 물고 늘어졌다. 경험이 부족하면 시간과 체력으로 메웠고, 체력이 바닥나면 오기로 버텼다. 결국 최종안은 우리가 주도하여 계획한 안으로 제출되었고, 기적처럼 '당선'이라는 결과를 거머쥐었다.

모두가 불가능하다고 했던 싸움에서 승리한, 참으로 기분 좋은 날이었다.
그러나 영광은 짧았고, 상실은 뼈아팠다. 

당선의 축배가 채 마르기도 전인 1~2달 사이, 그 캄캄한 밤들을 함께 지새웠던 4명의 직원이 차례로 사직서를 내밀었다. 이유는 하나였다. '너무 힘들어서'였다.

그 이후로도 우리는 1년에 한 번씩 현상설계에 뛰어들었고, 나가는 족족 거의 대부분 당선이라는 쾌거를 이루었다. 하지만 패턴은 참혹할 정도로 똑같이 반복되었다. 승리한 뒤에는 반드시 누군가가 회사를 떠나거나, 다시는 현상설계를 하지 않겠다고 선언했다.

도대체 왜 이렇게 된 것일까.
처음에는 그저 시대의 흐름인 줄 알았다. "요즘 친구들은 편하고 안정적인 것만 찾으려고 하는구나." 서운한 마음이 들었던 것도 사실이다. 하지만 누군가는 계속 이 일을 이끌어가야만 했고, 나는 텅 빈 자리들을 바라보며 뼈저리게 깨달아야만 했다. 

**승리를 위해 누군가를 갉아먹어야만 작동하는 시스템은, 결국 무너질 수밖에 없다는 것을.**

시간이 흘러 지금, 우리는 또 다른 사업지의 현상설계를 진행하고 있다.
하지만 이번에는 방식이 다르다. 사업지에 대한 분석, 대안의 작성, 그리고 머릿속의 아이디어를 이미지화하는 그 고된 작업의 중심에 'AI'가 들어와 있다. 

물론 현상설계라는 본질적인 치열함은 여전히 남아있고, 여전히 고단한 과정이다. 
하지만 적어도, 새벽 3시의 모니터 불빛 아래서 누군가의 영혼을 태워 연료로 삼는 일은 멈추었다. 

어설프게나마, 변화는 이미 시작되었다."""

new_page_json = f"""        }},
        {{
            "type": "chapter",
            "title": "[Episode 1] 상처 뿐인 영광, 그리고 붕괴의 서막",
            "subtitle": "2019년 9월, 장대B구역 당선의 역설"
        }},
        {{
            "type": "text_only",
            "text": {json.dumps(episode_1_text, ensure_ascii=False)}
        }},"""

# We want to insert this right after the Prologue section ends.
# The Prologue section is the first few elements. Let's find "다시, 선을 그릴 시간이다."
# The end of that object is "},". We will insert our new objects right after it.

target_str = "다시, 선을 그릴 시간이다.\\n\\n---\","
# Actually it is: "다시, 선을 그릴 시간이다.\n\n---",

# Let's use a regex to find the end of that specific page object
match = re.search(r'다시, 선을 그릴 시간이다.*?},', content, re.DOTALL)
if match:
    insert_pos = match.end()
    new_content = content[:insert_pos] + "\n" + new_page_json + content[insert_pos:]
    with open('book_data.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Success")
else:
    print("Failed to find insertion point")

