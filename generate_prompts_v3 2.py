import json
import re
import os

style = "Pure solid white background #FFFFFF, absolutely no parchment, no cream, or yellow tones. A highly abstract, mathematical, and geometric architectural sketch. Extremely fine, ultra-thin, hairline black wireframe construction lines. Minimalist geometric patterns (precise grids, concentric circles, intersecting polygons, orthographic projections). No organic shapes. Absolutely NO text, NO letters, NO words, NO characters. Pure high contrast of black ultra-thin geometric lines on a perfectly pure white background."

with open('book_data.js', 'r') as f:
    content = f.read()

match = re.search(r'const\s+bookData\s*=\s*(\{.*?\});\n*(?:if\s*\(\s*typeof\s*module|$)', content, re.DOTALL)
data = json.loads(match.group(1))

prompts = []
pages = data['pages']

for i, p in enumerate(pages):
    if p.get('type') == 'image_full':
        # Find the next non-image page
        next_page = None
        for j in range(i+1, len(pages)):
            if pages[j].get('type') != 'image_full':
                next_page = pages[j]
                break
        
        title = next_page.get('title', 'Unknown') if next_page else 'Unknown'
        text = next_page.get('text', '') if next_page else ''
        short_text = text[:300].replace('\n', ' ')
        
        prompt = f"Context: {title}. {short_text}. {style} Create a conceptual, abstract architectural illustration representing the core theme of this text using ONLY geometric shapes and ultra-thin lines on a pure white background. REMEMBER: NO TEXT ALLOWED."
        
        img_url = p.get('image', '')
        if img_url:
            img_name = os.path.basename(img_url).replace('.jpg', '').replace('.png', '')
        else:
            img_name = f"essay_{i:03d}_{title[:5].replace('.', '').replace(' ', '_')}"
            
        prompts.append({
            'index': i,
            'title': title,
            'image_name': img_name,
            'prompt': prompt
        })

with open('prompts_v3.json', 'w') as f:
    json.dump(prompts, f, ensure_ascii=False, indent=2)

print(f"Generated strict prompts for {len(prompts)} images in prompts_v3.json.")
