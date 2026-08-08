import json

file_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# 1. Prologue hook
prologue_marker_md = "# 📘 프롤로그: 우리는 왜 '진짜 설계'를 잃어버렸는가?"
prologue_hook_md = prologue_marker_md + "\n\n이 책은 밤을 새우며 도면을 그리는 젊은 건축가들, 직원의 퇴사에 절망하는 중소 설계사무소 소장들, 그리고 내 집의 가치(분담금)를 지키고 싶은 재건축 조합원 모두를 위한 생존의 기록이다. 건축가의 이상과 개발의 현실, 그 사이에서 어떻게 기계(AI)를 딛고 인간의 자리를 지켜냈는지에 대한 치열한 보고서다."
content = content.replace(prologue_marker_md, prologue_hook_md)

prologue_marker_js = "\"창조적인 공간을 고민해야 할 젊고 뛰어난 건축사들이"
prologue_hook_js = "\"이 책은 밤을 새우며 도면을 그리는 젊은 건축가들, 직원의 퇴사에 절망하는 중소 설계사무소 소장들, 그리고 내 집의 가치(분담금)를 지키고 싶은 재건축 조합원 모두를 위한 생존의 기록이다. 건축가의 이상과 개발의 현실, 그 사이에서 어떻게 기계(AI)를 딛고 인간의 자리를 지켜냈는지에 대한 치열한 보고서다.\\n\\n창조적인 공간을 고민해야 할 젊고 뛰어난 건축사들이"
js_content = js_content.replace(prologue_marker_js, prologue_hook_js)


# 2. Chapter 5 Visualization of Value
old_ch5 = "현실적으로는 사업성에 따라 수많은 조합원들의 '분담금'이 널뛰기하는 치열한 생존의 현장이다. 사업성을 낫게 하고, 조합원들의 피 같은 자산을 지켜주는 것. 그것이 바로 우리가 엑셀을 넘어 거대한 데이터를 쥐고 비즈니스 파트너로서 싸워야 하는 진짜 이유다."
new_ch5 = "현실적으로는 사업성에 따라 수많은 조합원들의 '분담금'이 널뛰기하는 치열한 생존의 현장이다. **용적률 단 1%의 차이, 세대수 몇 가구의 배치가 수십, 수백억 원의 사업성 차이로 직결된다.** 사업성을 낫게 하고, 조합원들의 피 같은 자산을 지켜주는 것. 종이 한 장짜리 데이터 보고서가 수백억의 가치를 창출하는 이 현실이 바로 우리가 엑셀을 넘어 거대한 데이터를 쥐고 비즈니스 파트너로서 싸워야 하는 진짜 이유다."

content = content.replace(old_ch5, new_ch5)
js_old_ch5 = old_ch5.replace('\n', '\\n')
js_new_ch5 = new_ch5.replace('\n', '\\n')
js_content = js_content.replace(js_old_ch5, js_new_ch5)


# 3. Chapter 6 Bridge
old_ch6 = "이 뼈아픈 고민 끝에 우리는 '진양 교육 플랫폼(J-Edu)'을 구축했다."
new_ch6 = "그렇다면 철이 철을 벼려주고, 경험이 경험을 키워주는 이 위대한 아날로그적 연대감을 어떻게 21세기의 방식(디지털)으로 구현할 것인가? 감성과 철학만으로는 바쁜 현대의 실무를 감당할 수 없다. 우리는 이 절박한 연대감을 시스템이라는 단단한 그릇에 담기로 했다.\n\n이 뼈아픈 고민 끝에 우리는 '진양 교육 플랫폼(J-Edu)'을 구축했다."

content = content.replace(old_ch6, new_ch6)
js_old_ch6 = old_ch6.replace('\n', '\\n')
js_new_ch6 = new_ch6.replace('\n', '\\n')
js_content = js_content.replace(js_old_ch6, js_new_ch6)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print("Commercial improvements injected successfully.")
