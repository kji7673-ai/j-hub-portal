import json
import re

file_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# 1. Prologue Expansion
old_prologue = "우리는 왜 수백억 원의 자산을 다루는 '전략적 비즈니스 파트너'에서, 관청의 서류를 대행해 주는 '을(乙)'로 스스로를 전락시켰는가?"
new_prologue = "우리는 왜 수백억 원의 자산을 다루는 '전략적 비즈니스 파트너'에서, 관청의 서류를 대행해 주는 '을(乙)'로 스스로를 전락시켰는가?\n\n우리는 스스로를 '예술가'라 칭하며 헛기침을 해왔다. 전통적인 빛과 그림자, 본능적인 공간감을 논하며 감동을 주고자 했지만, 정작 그 공간의 층고와 형태가 거주자의 심리와 건강, 가족 간의 소통에 어떤 영향을 미치는지에 대한 '사실적인 데이터와 연구'는 얼마나 가지고 있었던가? 우리는 반성해야 한다. 예술적 감동만을 좇을 것이 아니라, 몸과 정신, 그리고 사회에 끼치는 영향에 대해 끊임없이 공부하고 데이터로 증명해야 하는 시대다."

# 2. Chapter 5 Expansion
old_ch5 = "데이터 없는 제안에 신뢰가 생길 리 만무했다."
new_ch5 = "단순히 보고서를 그럴싸하게 포장하자는 것이 아니다. 특히 내가 몸담고 있는 '정비사업'에서 아파트는 대한민국 사회에서 매우 특수한 위치를 차지한다. 주거 공간으로서의 숭고한 중요성도 있지만, 현실적으로는 사업성에 따라 수많은 조합원들의 '분담금'이 널뛰기하는 치열한 생존의 현장이다. 사업성을 낫게 하고, 조합원들의 피 같은 자산을 지켜주는 것. 그것이 바로 우리가 엑셀을 넘어 거대한 데이터를 쥐고 비즈니스 파트너로서 싸워야 하는 진짜 이유다. 데이터 없는 제안에 신뢰가 생길 리 만무했다."

# 3. Epilogue / Mindset Expansion
old_mindset = "4. **다정함**: 디자인은 결국 본인의 인격적 성숙에서 나옵니다. 건물을 청소하는 분, 지역 주민, 바람과 조망에 대한 공감이 있을 때 진짜 설계가 나옵니다."
new_mindset = "4. **다정함**: 디자인은 결국 본인의 인격적 성숙에서 나옵니다. 건물을 청소하는 분, 지역 주민, 바람과 조망에 대한 공감이 있을 때 진짜 설계가 나옵니다.\n5. **쟁이와 학자의 결합**: 빛과 그림자가 주는 본능적 감각의 위대함을 부정하지 않습니다. 우리 역시 공간을 통한 감동을 주고 싶어 이 길을 걷고 있습니다. 하지만 이제는 본능적 감각에만 의존할 수 없습니다. 공간이 건강과 정신에 미치는 사실적 데이터와 연구를 결합하여, 더 깊이 연결되고 공부하는 '깨어있는 쟁이'가 되어야 합니다."

# Update MD
content = content.replace(old_prologue, new_prologue)
content = content.replace(old_ch5, new_ch5)
content = content.replace(old_mindset, new_mindset)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

# Update JS (Since JS might have encoded newlines or different structures, we do replace directly on strings)
# Note: In book_data.js, newlines might be represented as `\n` literal or actual newlines depending on structure.
# But `book_data.js` is pretty-printed JSON, so actual newlines inside strings are escaped as `\n`.
# So we need to format the strings correctly for replacement in JS.

js_old_prologue = old_prologue.replace('\n', '\\n')
js_new_prologue = new_prologue.replace('\n', '\\n')
js_content = js_content.replace(js_old_prologue, js_new_prologue)

js_old_ch5 = old_ch5.replace('\n', '\\n')
js_new_ch5 = new_ch5.replace('\n', '\\n')
js_content = js_content.replace(js_old_ch5, js_new_ch5)

# For Mindset, JS has markdown in text block.
js_old_mindset = old_mindset.replace('\n', '\\n')
js_new_mindset = new_mindset.replace('\n', '\\n')
js_content = js_content.replace(js_old_mindset, js_new_mindset)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print("Philosophy injected into manuscript and book_data.js successfully.")
