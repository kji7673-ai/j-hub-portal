import sys

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

target_text = "치열한 내부 진통 끝에, 우리는 직원들의 로컬 PC에서 임의로 PDF를 변환해 발송하는 행위를 원천 차단하고, 외부로 나가는 모든 공문과 보고서는 반드시 J-Hub 웹 에디터를 거치도록 강제했다."

new_text = """나는 이 완벽해 보이는 시스템이 단숨에 정착되었다고 거짓말하지 않겠다. 사실, 나는 그 거센 반발 앞에서 차마 직원들에게 신체제를 일방적으로 강요하지 못했다. 

현재 우리 진양건축은 무식하지만 익숙한 '과거의 시스템'과, 낯설지만 압도적인 '새로운 J-Hub 시스템'을 아슬아슬하게 병행(Two-track)하며 과도기를 걷고 있다. J-Hub 역시 완성된 유토피아가 아니다. 매일 현장의 피드백을 받으며 깨지고, 수정하고, 생각에 생각을 더해 더 나은 AI 프로그램을 덧붙여가는 '미완성의 공사판'에 가깝다.

리더인 내가 할 수 있는 것은, 강압적인 채찍질이 아니다. 과거의 방식(엑셀과 철야)으로 고통받는 직원들 옆에서 묵묵히 시스템을 고도화하며, 그들 스스로 '이 깔때기(AI)에 올라타는 것이 나의 퇴근 시간을 앞당기고 나를 진짜 건축가로 만들어준다'는 사실을 깨달을 때까지 기다려주는 것뿐이다. 혁신은 선언으로 이루어지는 것이 아니라, 끊임없는 땜질과 리더의 지독한 인내로 완성된다는 것을 나는 뼈저리게 배우고 있다."""

target_text_js = target_text
new_text_js = new_text.replace("\n\n", "\\n\\n")

# Update MD
with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

md_text = md_text.replace(target_text, new_text)

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_text)

# Update JS
with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

js_text = js_text.replace(target_text_js, new_text_js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Confession injection successful.")
