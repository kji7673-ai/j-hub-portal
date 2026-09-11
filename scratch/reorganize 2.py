import json
import re

with open("docs/book_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("[")
end_idx = content.rfind("]") + 1
json_str = content[start_idx:end_idx]
data = json.loads(json_str)

for i, item in enumerate(data):
    print(f"{i}: {item.get('title', '')}")
