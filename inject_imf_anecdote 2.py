import json

file_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

old_text = """3년 전 겨울, 가장 아끼던 5년 차 대리가 퇴사 면담을 요청했다. "대표님, 여기선 더 이상 제가 성장할 수 없는 것 같습니다." 가슴이 철렁했다. 그가 떠나는 것은 단순히 인력 유출이 아니었다. 수없이 야근하며 겪은 까다로운 협상 스킬, 지하주차장 동선 설계 꿀팁이 모두 흩어지는 것이었다.

동료 소장님들도 이 밑빠진 독의 고통을 아실 것이다. 인재들이 떠나는 것을 막으려면, 이 공간 안에 그들이 탐낼 만한 **'보물(Treasure)'**이 있어야 한다. "이 회사에 있으면 무조건 남들보다 앞서가는 전문가로 성장한다"는 강력한 확신. 

우리는 이를 위해 '진양 교육 플랫폼(J-Edu)'을 구축했다. 고연차 임원들이 온몸으로 부딪혀 얻은 실패담과 성공담을 담아내는 살아 숨 쉬는 유기체다. 누구나 부담 없이 읽도록 실무 노하우를 **'3분짜리 카드형 숏폼 UI'**로 압축했다."""

new_text = """3년 전 겨울, 가장 아끼던 5년 차 대리가 퇴사 면담을 요청했다. 가슴이 철렁했다. 그가 떠나는 것은 단순히 인력 유출이 아니었다. 수없이 야근하며 겪은 까다로운 협상 스킬과 노하우가 공중으로 흩어지는 것이었다. 에이스 직원이 퇴사할 때마다 회사의 20년 치 경쟁력도 함께 리셋되는 참담한 현실을 언제까지 방관할 것인가? 

이 뼈아픈 고민 끝에 우리는 '진양 교육 플랫폼(J-Edu)'을 구축했다. 하지만 오해해서는 안 된다. **정말 중요한 것은 플랫폼이나 AI 기술이 아니라, 결국 '사람'이다.** 

'철이 철을 날카롭게 하는 것 같이 사람이 그 친구의 얼굴을 빛나게 하느니라' (잠언 27:17). 

내가 이 시스템에 집착했던 진짜 이유는, 각자가 가진 작은 경험치들을 합치면 거대한 시너지를 낼 수 있다는 믿음 때문이었다. 내가 처음 입사했던 IMF 직후의 시절이 떠오른다. 당시 윗선배들이 대거 퇴사하고 사무실에는 온통 신입들만 남겨진 암담한 상황이었다. 그때 1~2년 차 동기 다섯 명이 모여 굳은 결의를 다졌다. 
**'우리 1, 2년 차 5명이 경험을 공유하고 합치면 10년 차 베테랑이 될 수 있다. 우리가 부딪히고 깨진 경험을 남김없이 나누자.'**

J-Edu 플랫폼은 바로 그 시절, 동기들과 나누었던 절박한 연대감의 디지털 진화 버전이다. AI와 시스템은 단지 거들 뿐이다. 핵심은 선배와 후배, 동료들이 서로의 실수와 경험을 투명하게 데이터화하여 공유하고, 서로를 날카롭게 벼려주며 함께 성장하는 '조직 문화' 그 자체에 있다."""

# Update MD
if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated manuscript successfully.")
else:
    print("Could not find old text in manuscript.")

# Update JS
js_old = old_text.replace('\n', '\\n')
js_new = new_text.replace('\n', '\\n')

if js_old in js_content:
    js_content = js_content.replace(js_old, js_new)
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Updated book_data.js successfully.")
else:
    print("Could not find old text in book_data.js.")
