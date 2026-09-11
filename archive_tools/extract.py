import json

with open("book_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start = content.find("{")
end = content.rfind("}") + 1
book = json.loads(content[start:end])

for i in range(40, min(60, len(book["pages"]))):
    p = book["pages"][i]
    title = p.get("title", "")
    text = p.get("text", "")
    print(f"[{i+1}] Title: {title}")
    print(f"Text: {text[:100].replace(chr(10), ' ')}...")
