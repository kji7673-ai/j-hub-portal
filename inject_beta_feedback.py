import sys

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

beta_feedback = """

---

## 📬 [Beta v1.0] 독자 피드백 (Reader Feedback)

이 책은 진양건축의 J-Hub 시스템처럼 아직 완결되지 않았습니다. 현장에 계신 여러분의 날카로운 피드백을 받아 계속해서 진화할 '살아있는 문서'입니다. 

건축계 동료, 조합 관계자, 그리고 IT 업계 종사자 여러분의 따뜻한 조언과 날 선 비판 모두 환영합니다. 여러분이 주신 소중한 의견은 다음 정식 출간 버전에 적극 반영될 것입니다.

**[👉 피드백 남기기 (Google Forms 등 링크 삽입 예정) ]**

*진양건축 전 대표이사 올림*
"""

# Append to MD
with open(md_path, 'a', encoding='utf-8') as f:
    f.write(beta_feedback)

# Append to JS (Need to carefully inject before the closing brace of the Epilogue or append as a new section)
# Since the JS is structured, let's see how to append it safely. We can just append it to the Epilogue content.
with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

target = "그것이 바로 미래의 건축이다."
new_target = "그것이 바로 미래의 건축이다.\\n\\n---\\n\\n## 📬 [Beta v1.0] 독자 피드백 (Reader Feedback)\\n\\n이 책은 진양건축의 J-Hub 시스템처럼 아직 완결되지 않았습니다. 현장에 계신 여러분의 날카로운 피드백을 받아 계속해서 진화할 '살아있는 문서'입니다.\\n\\n건축계 동료, 조합 관계자, 그리고 IT 업계 종사자 여러분의 따뜻한 조언과 날 선 비판 모두 환영합니다. 여러분이 주신 소중한 의견은 다음 정식 출간 버전에 적극 반영될 것입니다.\\n\\n**[👉 피드백 남기기 (Google Forms 등 링크 삽입 예정) ]**\\n\\n*진양건축 전 대표이사 올림*"

if target in js_text:
    js_text = js_text.replace(target, new_target)
    
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Beta feedback section injected successfully.")
