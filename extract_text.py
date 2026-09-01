import json

with open("book_data.js", "r", encoding="utf-8") as f:
    content = f.read()

json_start = content.find("{")
json_end = content.rfind("}") + 1
data = json.loads(content[json_start:json_end])

with open("book_text.txt", "w", encoding="utf-8") as f:
    for i, page in enumerate(data.get("pages", [])):
        if "title" in page:
            f.write(f"--- Page {i+1} ---\nTitle: {page['title']}\n")
        if "text" in page:
            f.write(f"Text:\n{page['text']}\n")
        f.write("\n")
