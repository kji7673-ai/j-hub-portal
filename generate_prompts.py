import json
import os

js_path = "book_data.js"
with open(js_path, 'r', encoding='utf-8') as f:
    text = f.read()

data = json.loads(text[text.find('{'):text.rfind('}')+1])

prompts = []
current_chapter_title = "Architectural abstraction"

# Base prompt style
style = "fine line art, blueprint style, hand-drawn architectural draft, clean white background, monochrome, elegant, professional."

# Specific concepts mapped to keywords
concept_map = {
    "불완전한 데이터": "A frustrated architect looking at fragmented and chaotic data floating in the air, " + style,
    "아키 시냅스": "A glowing neural network made of architectural lines connecting various building blueprints, " + style,
    "AI의 시선": "An abstract glowing AI core observing an old traditional drafting table, " + style,
    "통합 보고서": "A magical, glowing architectural report emitting precise data particles, " + style,
    "교육 플랫폼": "A grand, infinite library of architectural blueprints and glowing digital archives, " + style,
    "진양 허브": "A sleek, futuristic control tower monitoring multiple architectural projects on holographic screens, " + style,
    "아름다움": "An incredibly elegant, perfectly balanced architectural presentation board radiating a subtle aura, " + style,
    "사진과 여백": "A minimalist camera lens focusing on a beautifully composed empty architectural space (void), " + style,
    "에필로그": "An experienced architect's hand and a futuristic digital interface drawing a blueprint together, " + style,
    "진짜 설계": "An architect standing before a massive, chaotic maze of generic concrete boxes, searching for meaning, " + style,
    "쟁이의 마음": "A single architectural drafting pen glowing with intense, renewed creative energy, " + style,
    "생존 신고": "A single, resilient light bulb glowing warmly in a dark, empty architectural studio, " + style,
    "선 긋기와 인생": "A hand-drawn architectural line that is slightly wavy up close but perfectly straight from a distance, " + style,
    "생각의 힘": "A glowing magnifying glass revealing the hidden structural truth beneath a complex blueprint, " + style,
    "만들어져 가는 것": "An organic architectural structure dynamically assembling and evolving itself in mid-air, " + style,
    "완벽을 추구하되": "A modern architectural structure blending seamlessly and naturally into a rugged cliff face, " + style,
    "사이 공간": "A striking architectural courtyard where the empty void is filled with soft, dramatic light, " + style,
    "방향성과 중심성": "A dynamic, sweeping spiral staircase leading the eye toward a powerful central core of light, " + style,
    "스케일과 대비": "A tiny human figure standing in awe next to a monumental, soaring architectural column, " + style,
    "단순화와 포용력": "A simple, elegant architectural pavilion with open arms, welcoming the surrounding environment, " + style,
    "주변에 순응하라": "A subtle, graceful roofline perfectly echoing the gentle curves of the surrounding mountain peaks, " + style,
    "공유 결합": "Interlocking, modular architectural blocks forming a cohesive, interconnected and sustainable city, " + style,
    "다정함": "A warm, inviting architectural facade with soft, glowing lights and welcoming proportions, " + style,
    "신입들에게": "A group of passionate young architects gathered around a glowing, beautifully crafted physical model, " + style,
}

for i in range(100, len(data['pages'])):
    p = data['pages'][i]
    if p.get('type') in ['image_top', 'image_full']:
        title = p.get('title', '').strip()
        if not title:
            # Try to get first line of text
            text_lines = p.get('text', '').strip().split('\n')
            if text_lines and text_lines[0]:
                title = text_lines[0][:30] + "..."
            else:
                title = current_chapter_title + " (연속)"
        else:
            current_chapter_title = title
            
        # Find best matching prompt
        prompt = f"A minimalist architectural conceptual sketch exploring the theme of '{title}', {style}"
        for key, val in concept_map.items():
            if key in title:
                prompt = val
                break
                
        prompts.append(f"### [{i+1}.jpg] {title}\n`{prompt}`\n")

md_content = f"""# J-Journal 캔바(Canva) 샵도 이미지 프롬프트 가이드 (101~마지막 페이지)

> **사용 방법:** 아래의 영어 텍스트를 그대로 복사하여 캔바 AI 이미지 생성기(Magic Media 등)에 붙여넣기 하세요. 생성된 이미지를 다운로드하여 순서대로 저장하시면 됩니다.

---

{chr(10).join(prompts)}
"""

with open('canva_prompts_part6_final.md', 'w', encoding='utf-8') as f:
    f.write(md_content)

print("Generated canva_prompts_part6_final.md")
