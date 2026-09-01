import json
import sys
import re

def extract_json(content):
    # Matches the bookData object
    match = re.search(r'const\s+bookData\s*=\s*(\{.*?\});\n*(?:if\s*\(\s*typeof\s*module|$)', content, re.DOTALL)
    if match:
        return match.group(1), match.start(1), match.end(1)
    return None, -1, -1

def main():
    # Load docs/book_data.js
    with open('docs/book_data.js', 'r') as f:
        docs_content = f.read()
    
    docs_json_str, _, _ = extract_json(docs_content)
    if not docs_json_str:
        print("Failed to parse docs/book_data.js")
        return
        
    docs_data = json.loads(docs_json_str)
    
    images_to_insert = []
    seen_images = set()
    
    for i, p in enumerate(docs_data['pages']):
        if p.get('type') == 'image_full' and ('static/images/essay_' in p.get('image', '') or 'static/images/sketch_' in p.get('image', '') or 'static/images/line_' in p.get('image', '')):
            img = p.get('image')
            if img not in seen_images:
                seen_images.add(img)
                # Find the next page that is NOT an image_full
                next_page = None
                for j in range(i+1, len(docs_data['pages'])):
                    if docs_data['pages'][j].get('type') != 'image_full':
                        next_page = docs_data['pages'][j]
                        break
                if next_page:
                    images_to_insert.append({
                        'image_obj': p,
                        'target_title': next_page.get('title'),
                        'target_text': next_page.get('text')
                    })

    print(f"Found {len(images_to_insert)} unique generated images in docs/book_data.js.")

    # Load root book_data.js
    with open('book_data.js', 'r') as f:
        root_content = f.read()
    
    root_json_str, start_root, end_root = extract_json(root_content)
    root_data = json.loads(root_json_str)
    
    new_pages = []
    for page in root_data['pages']:
        # Only inject if this page is NOT an image_full
        if page.get('type') != 'image_full':
            # Check if this page matches any target
            for item in images_to_insert:
                match_title = item['target_title'] and page.get('title') == item['target_title']
                match_text = item['target_text'] and page.get('text') == item['target_text']
                if match_title or match_text:
                    new_pages.append(item['image_obj'])
                    images_to_insert.remove(item)
                    break
        
        new_pages.append(page)
        
    root_data['pages'] = new_pages
    
    print(f"New total pages in root: {len(new_pages)}")
    
    new_json = json.dumps(root_data, indent=4, ensure_ascii=False)
    new_content = root_content[:start_root] + new_json + root_content[end_root:]
    
    with open('book_data.js', 'w') as f:
        f.write(new_content)
    with open('docs/book_data.js', 'w') as f:
        f.write(new_content)
        
if __name__ == "__main__":
    main()
