import json

with open("book_data.js", "r", encoding="utf-8") as f:
    content = f.read()

json_start = content.find("{")
json_end = content.rfind("}") + 1
json_str = content[json_start:json_end]
data = json.loads(json_str)

page_idx = 71
if len(data["pages"]) > page_idx:
    data["pages"][page_idx]["image"] = "static/images/72.jpg"
    print("Added image to index", page_idx, ":", data["pages"][page_idx].get("title"))
else:
    print("Index", page_idx, "out of range")

new_json_str = json.dumps(data, ensure_ascii=False, indent=4)
new_content = content[:json_start] + new_json_str + content[json_end:]

with open("book_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)
