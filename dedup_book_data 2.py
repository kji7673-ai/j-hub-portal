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
    # Load docs/book_data.js which is the ground truth but has duplicate images
    with open('docs/book_data.js', 'r') as f:
        content = f.read()
    
    json_str, start_idx, end_idx = extract_json(content)
    data = json.loads(json_str)
    
    new_pages = []
    seen_generated_images = set()
    
    for p in data['pages']:
        if p.get('type') == 'image_full' and ('essay_' in p.get('image', '') or 'sketch_' in p.get('image', '')):
            img = p.get('image')
            # Deduplicate ONLY consecutive images or if we've seen this generated image already
            if img in seen_generated_images:
                continue
            seen_generated_images.add(img)
            
        new_pages.append(p)
    
    data['pages'] = new_pages
    
    print(f"Total pages after deduplication: {len(new_pages)}")
    
    new_json = json.dumps(data, indent=4, ensure_ascii=False)
    new_content = content[:start_idx] + new_json + content[end_idx:]
    
    with open('docs/book_data.js', 'w') as f:
        f.write(new_content)
    with open('book_data.js', 'w') as f:
        f.write(new_content)
        
if __name__ == "__main__":
    main()
