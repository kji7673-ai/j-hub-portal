import json
import re

js_path = "book_data.js"
with open(js_path, 'r', encoding='utf-8') as f:
    text = f.read()

json_start = text.find('{')
json_end = text.rfind('}') + 1

if json_start != -1 and json_end != -1:
    json_str = text[json_start:json_end]
    data = json.loads(json_str)
    
    merged_pages = []
    
    for page in data.get('pages', []):
        title = page.get('title', '')
        if "(계속)" in title:
            # Append text to the previous page
            if merged_pages:
                merged_pages[-1]['text'] += '\n\n' + page.get('text', '')
        else:
            merged_pages.append(page)
            
    data['pages'] = merged_pages
    
    new_js = "const bookData = " + json.dumps(data, ensure_ascii=False, indent=4) + ";\n"
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(new_js)
    
    print("Un-paginated successfully. Total pages:", len(merged_pages))
else:
    print("Failed to find JSON data.")
