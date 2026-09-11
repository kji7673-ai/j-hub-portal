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
    
    new_pages = []
    
    for page in data.get('pages', []):
        if page.get('type') in ['text_only', 'image_top', 'image_full'] and 'text' in page:
            p_text = page['text']
            
            # Simple heuristic: if text is very long (e.g., > 400 chars), split by paragraphs
            paragraphs = p_text.split('\n\n')
            
            chunks = []
            current_chunk = []
            current_len = 0
            
            # Different max length depending on type
            max_len = 500 if page['type'] == 'text_only' else 300
            
            for p in paragraphs:
                p_len = len(p)
                if current_len + p_len > max_len and current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                    current_chunk = [p]
                    current_len = p_len
                else:
                    current_chunk.append(p)
                    current_len += p_len
            
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                
            if len(chunks) > 1:
                # First page retains original type (e.g., image_top)
                first_page = page.copy()
                first_page['text'] = chunks[0]
                new_pages.append(first_page)
                
                # Subsequent pages become text_only
                for chunk in chunks[1:]:
                    new_pages.append({
                        "type": "text_only",
                        "title": page.get('title', '') + " (계속)",
                        "text": chunk
                    })
            else:
                new_pages.append(page)
        else:
            new_pages.append(page)
            
    data['pages'] = new_pages
    
    # Write back
    new_js = "const bookData = " + json.dumps(data, ensure_ascii=False, indent=4) + ";\n"
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(new_js)
    
    print("Pagination applied successfully. Total pages:", len(new_pages))
else:
    print("Failed to find JSON data.")
