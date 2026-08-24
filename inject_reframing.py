import json
import re

with open('docs/book_data.js', 'r') as f:
    c = f.read()

prefix = c[:c.find('[')]
suffix = c[c.rfind(']')+1:]
data = json.loads(c[c.find('['):c.rfind(']')+1])

# 1. Update prologue if needed (but user suggested adding to prologue OR part 3 preface)
# We will create a preface object for Part 3.

new_part_name = "3부: 2015-2024년 현장에서 수집한 기록들"
preface_text = """<p style="font-size: 1.1em; line-height: 1.8; margin-bottom: 24px; font-style: italic; color: var(--primary);">
"이 기록들의 톤이 일관되지 않은 이유는, 내가 설계사에서 경영자로, 다시 철학자로 변해가는 과정 자체가 일관되지 않았기 때문입니다.<br><br>
그 혼란과 초현실성을 지우는 것은 이 여정의 가장 중요한 부분을 제거하는 것입니다.<br>
AI와 함께 일하게 된 이유도, 결국 이 혼란 속에서 비롯됩니다."
</p>
<p style="margin-bottom: 24px;">
이 3부의 기록들은 (톤이 변하고, 주체가 흔들리고, 초현실적인 순간들도 포함된) 실제 현장에서의 경험입니다.
</p>
"""

out_data = []
part3_started = False
essay_count = 0

for item in data:
    part_name = item.get("part", "")
    
    if "3부" in part_name:
        if not part3_started:
            part3_started = True
            # Insert the preface object right before the first essay of part 3
            out_data.append({
                "type": "essay",
                "part": new_part_name,
                "title": "3부 서문",
                "text": preface_text
            })
            
        item["part"] = new_part_name
        
        # Tag the essays based on their sequence/content
        title = item.get("title", "")
        if "type" in item and item["type"] == "essay" and title != "3부 서문" and not title.startswith("Part 3"):
            essay_count += 1
            # We have 94 essays. Let's divide them into the 3 eras roughly, 
            # while matching the user's explicit examples.
            # 1-33: 2017 (설계사 시절) -> contains 156-157? Wait, 156-157 in book_data is essay_index.
            # Let's parse the essay number from the title "01. 주변에...", "32. 외로움..."
            match = re.search(r'^(\d+)\.', title)
            if match:
                num = int(match.group(1))
                if num <= 30:
                    tag = "<span style='display:inline-block; margin-bottom: 15px; font-size: 0.85em; font-weight: 600; color: #777; background: #eee; padding: 4px 8px; border-radius: 4px;'>[2017년 설계사 시절의 기록]</span><br>"
                elif num <= 70:
                    tag = "<span style='display:inline-block; margin-bottom: 15px; font-size: 0.85em; font-weight: 600; color: #777; background: #eee; padding: 4px 8px; border-radius: 4px;'>[2019-2021년 전환기의 기록]</span><br>"
                else:
                    tag = "<span style='display:inline-block; margin-bottom: 15px; font-size: 0.85em; font-weight: 600; color: #777; background: #eee; padding: 4px 8px; border-radius: 4px;'>[2023-2024년 경영자로서의 기록]</span><br>"
                
                # Check user specific examples
                # 63번(156번 인덱스 방구쟁이) - user said it should be 2017
                if num == 63 or num == 64:
                    tag = "<span style='display:inline-block; margin-bottom: 15px; font-size: 0.85em; font-weight: 600; color: #777; background: #eee; padding: 4px 8px; border-radius: 4px;'>[2017년 설계사 시절의 기록]</span><br>"
                
                # Prefix the text with the tag
                text = item.get("text", "")
                if isinstance(text, str) and not text.startswith("<span style='display:inline-block; margin-bottom: 15px;"):
                    item["text"] = tag + text
    
    out_data.append(item)

# Also update the prologue text to include the sentence if needed, but adding a dedicated preface is cleaner.
# Let's just update the prologue bullet point for Part 3 to match the new title.
for item in out_data:
    if item.get("title") == "프롤로그":
        text = item.get("text", "")
        text = text.replace("3부 [증언과 성찰]", "3부 [2015-2024년 현장에서 수집한 기록들]")
        item["text"] = text

new_json_str = json.dumps(out_data, ensure_ascii=False, indent=4)
with open('docs/book_data.js', 'w') as f:
    f.write(prefix + new_json_str + suffix)

print("Updated docs/book_data.js with the new reframing for Part 3.")
