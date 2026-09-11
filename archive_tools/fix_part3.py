import json
import re

with open('docs/book_data.js', 'r') as f:
    c = f.read()

prefix = c[:c.find('[')]
suffix = c[c.rfind(']')+1:]
data = json.loads(c[c.find('['):c.rfind(']')+1])

titles_to_move = [
    "4장. 선택(Choice)이 곧 건축이다",
    "5장. 기술이 지워진 자리에 남은 것 (비워냄의 미학)",
    "6장. 물방울, 그리고 시지프스의 언덕"
]

for item in data:
    if item.get("title") in titles_to_move:
        item["part"] = "3부: 증언과 성찰"
        title = item["title"]
        title = re.sub(r'^\d+장\.\s*', '', title)
        item["title"] = title

new_json_str = json.dumps(data, ensure_ascii=False, indent=4)
with open('docs/book_data.js', 'w') as f:
    f.write(prefix + new_json_str + suffix)

print("Moved items to Part 3!")
