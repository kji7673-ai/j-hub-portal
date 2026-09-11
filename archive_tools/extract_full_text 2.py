import json
import re

def extract_json(content):
    match = re.search(r'const\s+bookData\s*=\s*(\{.*?\});\n*(?:if\s*\(\s*typeof\s*module|$)', content, re.DOTALL)
    if match:
        return match.group(1)
    return None

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = extract_json(content)
data = json.loads(json_str)

with open('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/full_manuscript.md', 'w', encoding='utf-8') as out:
    out.write("# J-Journal 전체 본문\n\n")
    for idx, page in enumerate(data.get('pages', [])):
        title = page.get('title')
        text = page.get('text')
        ai = page.get('ai_instruction')
        ceo = page.get('ceo_thoughts')
        
        if title:
            out.write(f"## {title}\n\n")
        if text:
            out.write(f"{text}\n\n")
            
        if ai or ceo:
            out.write("---\n")
            if ai:
                out.write(f"**[수정 요청사항 / 인사이트]**\n{ai}\n\n")
            if ceo:
                out.write(f"**[경영진 코멘트 / 회고]**\n{ceo}\n\n")
            out.write("---\n\n")

print("Extraction complete.")
