import json
import re

def main():
    with open('docs/book_data.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract JSON
    json_str = re.search(r'const bookData = (\{.*?\});$', content, re.DOTALL | re.MULTILINE)
    if not json_str:
        json_str = re.search(r'const bookData = (\{.*\});?', content, re.DOTALL)
    
    data = json.loads(json_str.group(1))
    
    pages = data['pages']
    
    # Analyze current pages
    for i, p in enumerate(pages):
        title = p.get('title', '')
        if "철학" in title or "원칙" in title or "영역성" in title or "순응" in title or "포용력" in title or "사이공간" in title:
            print(f"[{i}] {title}")
            
if __name__ == '__main__':
    main()
