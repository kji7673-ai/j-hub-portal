import sys
import os

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"
task_path = "/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/task.md"
walkthrough_path = "/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/walkthrough.md"

# 1. Update MD
with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

target_md = "이 책은 바로 그 참담한 실패와 뼈저린 좌절, 그리고 다시 일어서기 위한 치열한 투쟁의 기록이다."
new_md = "사실, 불과 몇 년 전까지만 해도 우리 진양건축 역시 엑셀을 두드리며 며칠 밤을 새우고, 허술한 종이 한 장짜리 보고서를 들고 조합을 찾아가던 수많은 평범한 설계사무소 중 하나였다. 우리 역시 무지했고, 무식하게 몸을 갈아 넣었다. 이 책은 그 부끄러운 절망의 끝에서 우리 진양건축이 피 흘리며 찾아낸, 처절하지만 가장 현실적인 '생존에 관한 보고서'다."

if target_md in md_text:
    md_text = md_text.replace(target_md, new_md)
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_text)

# 2. Update JS
with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

target_js = "이 책은 바로 그 참담한 실패와 뼈저린 좌절, 그리고 다시 일어서기 위한 치열한 투쟁의 기록이다."
new_js = "사실, 불과 몇 년 전까지만 해도 우리 진양건축 역시 엑셀을 두드리며 며칠 밤을 새우고, 허술한 종이 한 장짜리 보고서를 들고 조합을 찾아가던 수많은 평범한 설계사무소 중 하나였다. 우리 역시 무지했고, 무식하게 몸을 갈아 넣었다. 이 책은 그 부끄러운 절망의 끝에서 우리 진양건축이 피 흘리며 찾아낸, 처절하지만 가장 현실적인 '생존에 관한 보고서'다."

if target_js in js_text:
    js_text = js_text.replace(target_js, new_js)
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

# 3. Fix Task and Walkthrough
if os.path.exists(task_path):
    with open(task_path, 'r', encoding='utf-8') as f:
        task_text = f.read()
    task_text = task_text.replace("정린", "진양건축")
    with open(task_path, 'w', encoding='utf-8') as f:
        f.write(task_text)

if os.path.exists(walkthrough_path):
    with open(walkthrough_path, 'r', encoding='utf-8') as f:
        walk_text = f.read()
    walk_text = walk_text.replace("정린", "진양건축")
    with open(walkthrough_path, 'w', encoding='utf-8') as f:
        f.write(walk_text)

print("Fixed company name to 진양건축 successfully.")
