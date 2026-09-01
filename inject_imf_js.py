import json

js_path = "book_data.js"

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

old_js_text = """[3분짜리 통찰력, 그리고 30년의 경험치]\n\n3년 전 겨울, 회사에서 가장 아끼던 5년 차 대리가 퇴사 면담을 요청해 왔다. "대표님, 죄송하지만 여기선 더 이상 제가 성장할 수 없는 것 같습니다. 배울 게 없어요." 담담한 그의 말에 가슴이 철렁 내려앉았다. 그가 회사를 떠나는 것은 단순히 젊은 인력 한 명이 나가는 것이 아니었다. 그가 5년 동안 수없이 야근하며 겪은 까다로운 구청 주무관과의 협상 스킬, 좁은 대지에서의 지하주차장 동선 설계 꿀팁, 심의 위원을 설득하던 논리가 모두 그의 등 뒤로 함께 걸어 나가는 것이었다. 건축 업계의 고질적인 문제인 '도제식 교육'과 '인력 유출'의 뼈아픈 현장이었다.\n\n젊고 똑똑한 인재들이 회사를 떠나는 것을 막으려면, 그들이 머무는 공간 안에 그들이 탐낼 만한 **'보물(Treasure)'**이 있어야 한다. 단순히 월급의 액수만이 아니다. "이 회사에 있으면 내가 무조건 남들보다 앞서가는 전문가로 성장한다"는 강력한 확신, 즉 내일 당장 실무에 써먹을 수 있는 '압도적인 생존 지식'이 보물이다."""

new_js_text = """[철이 철을 날카롭게 하듯, 사람이 조직을 빛나게 한다]\n\n3년 전 겨울, 회사에서 가장 아끼던 5년 차 대리가 퇴사 면담을 요청해 왔다. 가슴이 철렁 내려앉았다. 그가 회사를 떠나는 것은 단순히 젊은 인력 한 명이 나가는 것이 아니었다. 수없이 야근하며 겪은 까다로운 협상 스킬과 설계 꿀팁이 모두 허공으로 흩어지는 것이었다. 에이스 직원이 퇴사할 때마다 회사의 20년 치 경쟁력도 리셋되는 이 참담한 현실을 언제까지 방관할 것인가?\n\n이 뼈아픈 고민 끝에 우리는 '진양 교육 플랫폼(J-Edu)'을 구축했다. 하지만 결코 오해해서는 안 된다. **조직에서 가장 중요한 것은 플랫폼이나 AI 기술이 아니라, 결국 '사람'이다.**\n\n'철이 철을 날카롭게 하는 것 같이 사람이 그 친구의 얼굴을 빛나게 하느니라' (잠언 27:17).\n\n내가 이 시스템에 집착했던 진짜 이유는, 각자가 가진 경험치들을 합치면 거대한 시너지를 낼 수 있다는 믿음 때문이었다. 내가 처음 입사했던 IMF 직후, 윗선배들이 대거 퇴사하고 사무실에 온통 신입들만 남겨졌을 때 1~2년 차 동기 다섯 명이 모여 했던 다짐이 있다.\n\n**'우리 1, 2년 차 5명이 경험을 공유하고 합치면 10년 차 베테랑이 될 수 있다. 우리가 부딪히고 깨진 경험을 남김없이 나누자.'**\n\nJ-Edu 플랫폼은 바로 그 시절, 동기들과 나누었던 절박한 연대감의 디지털 진화 버전이다. AI와 시스템은 단지 거들 뿐이다. 핵심은 선배와 후배가 서로의 실수와 경험을 데이터화하여 투명하게 공유하고, 서로를 날카롭게 벼려주며 함께 성장하는 '조직 문화' 그 자체에 있다."""

js_old = old_js_text.replace('\n', '\\n')
js_new = new_js_text.replace('\n', '\\n')

if js_old in js_content:
    js_content = js_content.replace(js_old, js_new)
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Updated book_data.js successfully.")
else:
    print("Could not find old text in book_data.js. Trying direct string replacement.")
    # Fallback to direct replacement just in case
    js_content = js_content.replace(old_js_text, new_js_text)
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Updated book_data.js (fallback).")
