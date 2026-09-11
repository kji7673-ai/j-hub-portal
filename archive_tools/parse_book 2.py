import re
import json
import os

def chunk_text(text, max_len=300):
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_len = 0
    for p in paragraphs:
        p = p.strip()
        if not p: continue
        if current_len + len(p) > max_len and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [p]
            current_len = len(p)
        else:
            current_chunk.append(p)
            current_len += len(p)
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    return chunks

with open('/Users/joongilkim/.gemini/antigravity/brain/8f6eccf3-af13-4f19-a784-0d89020d9da8/master_manuscript_final.md', 'r', encoding='utf-8') as f:
    text = f.read()

# We need to split by lines starting with # or ##
sections = []
current_section_lines = []

for line in text.split('\n'):
    if line.startswith('# ') or line.startswith('## '):
        if current_section_lines:
            sections.append('\n'.join(current_section_lines))
        current_section_lines = [line]
    else:
        current_section_lines.append(line)
if current_section_lines:
    sections.append('\n'.join(current_section_lines))

pages = []
pages.append({
    'type': 'cover',
    'title': 'J-Journal 철학편',
    'subtitle': '우리는 왜 진짜 설계를 잃어버렸는가'
})

# Gather images in order
images = [
    'static/images/media_1785978231415.jpg',
    'static/images/media_1785978231469.jpg',
    'static/images/media_1785978571030.jpg',
    'static/images/media_1785978571031.jpg',
    'static/images/media_1785978571032.jpg',
    'static/images/media_1785978635199.jpg',
    'static/images/media_1785978635201.jpg',
    'static/images/media_1785978635202.jpg',
    'static/images/media_1785978571049.png',
    'static/images/media_1785978231456.png',
    'static/images/media_1785978231458.png',
    'static/images/media_1785978231570.jpg'
]

img_idx = 0

for section in sections:
    section = section.strip()
    if not section: continue
    
    lines = section.split('\n')
    header = lines[0]
    body = '\n'.join(lines[1:]).strip()
    
    if header.startswith('# '):
        pages.append({
            'type': 'cover',
            'title': header.replace('# ', '').strip(),
            'subtitle': ''
        })
        if img_idx < len(images):
            pages.append({
                'type': 'image_full',
                'image': images[img_idx]
            })
            img_idx += 1
    elif header.startswith('## '):
        pages.append({
            'type': 'text_only',
            'title': header.replace('## ', '').strip(),
            'text': ''
        })
    else:
        body = section
    
    if body:
        # replace remaining headers
        body = re.sub(r'###\s+(.*)', r'[\1]', body)
        chunks = chunk_text(body, max_len=700)
        for i, chunk in enumerate(chunks):
            # Interleave images if there's enough text
            if len(chunk) > 50 and img_idx < len(images) and i % 3 == 0:
                pages.append({
                    'type': 'image_top',
                    'title': '',
                    'image': images[img_idx],
                    'text': chunk
                })
                img_idx += 1
            else:
                pages.append({
                    'type': 'text_only',
                    'title': '',
                    'text': chunk
                })

# Post processing to fix titles if needed
for i in range(len(pages)):
    if pages[i]['type'] == 'text_only' and pages[i]['text'] == '' and i + 1 < len(pages):
        # Merge title to next page if it's text only or image top
        next_page = pages[i+1]
        if not next_page.get('title'):
            next_page['title'] = pages[i]['title']
            pages[i]['delete'] = True

pages = [p for p in pages if not p.get('delete')]

js_content = "const bookData = {\n"
js_content += '    title: "J-Journal 철학편 (가제)",\n'
js_content += '    author: "CEO",\n'
js_content += '    pages: '
js_content += json.dumps(pages, ensure_ascii=False, indent=4)
js_content += '\n};\n'

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Generated {len(pages)} pages.")
