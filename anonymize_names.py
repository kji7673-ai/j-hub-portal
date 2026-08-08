import sys

md_path = "master_manuscript_v4_targeted.md"
js_path = "book_data.js"

replacements = {
    "청파2구역": "C구역",
    "용문동": "Y구역",
    "정린 CMP의 홍성훈 회장님": "굴지의 디벨로퍼 H 회장님",
    "용산구 Y구역 19-1번지 일원": "서울시 Y구역 일원", # Because 용산구 용문동 was changed to 용산구 Y구역, let's fix it better.
}

def replace_all(text):
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Fix the specific address issue if any
    text = text.replace("용산구 Y구역 19-1번지 일원", "서울시 Y구역 일원")
    text = text.replace("용산구 용문동 19-1번지 일원", "서울시 Y구역 일원")
    return text

with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

md_text = replace_all(md_text)

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_text)

with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

js_text = replace_all(js_text)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Anonymization complete.")
