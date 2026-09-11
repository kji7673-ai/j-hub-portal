import json

DB_PATH = 'data/manual_db.json'
with open(DB_PATH, 'r', encoding='utf-8') as f:
    db = json.load(f)

for doc in db:
    if 'html' in doc and '/static/images/' in doc['html']:
        doc['html'] = doc['html'].replace('/static/images/', 'static/images/')
    if 'content' in doc and '/static/images/' in doc['content']:
        doc['content'] = doc['content'].replace('/static/images/', 'static/images/')

with open(DB_PATH, 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=4)
print("Fixed all image paths in JSON")
