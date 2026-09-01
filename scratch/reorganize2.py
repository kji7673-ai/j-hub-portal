import json
import re

with open("docs/book_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("[")
end_idx = content.rfind("]") + 1
json_str = content[start_idx:end_idx]
data = json.loads(json_str)

# 0~106: keep as is
part1 = data[:107]

# 107~118: 쟁이의 단상 12 items
dangsang_12 = data[107:119]

# 119~124: 부록 & 액션
appendix = data[119:125]

# 125~128: 시지프스 & 마치는 글
sisyphus = data[125:129]

# 129~201: 쟁이의 단상 73 items
dangsang_73 = data[129:]

# Merge 12 and 73
merged_dangsang = dangsang_12 + dangsang_73

# Renumber the merged items
for i, item in enumerate(merged_dangsang):
    title = item.get("title", "")
    # Remove existing numbering or prefixes like "쟁이의 단상:", "N.", etc.
    title = re.sub(r'^(쟁이의 단상:\s*|대전 100년 시장 덮개공원 스케치\s*\d*\s*|올해의 신입들에게:\s*|\d+\.\s*)', '', title).strip()
    if not title:
        title = "무제"
    
    new_title = f"{i+1}. {title}"
    item["title"] = new_title

# New order: part1 + appendix + sisyphus + merged_dangsang
new_data = part1 + appendix + sisyphus + merged_dangsang

# Convert back to javascript
new_json_str = json.dumps(new_data, ensure_ascii=False, indent=4)
new_content = content[:start_idx] + new_json_str + content[end_idx:]

with open("docs/book_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Updated docs/book_data.js successfully.")
