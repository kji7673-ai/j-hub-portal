import re

html_path = "book_studio.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

author_logic = """
                else if (page.type === 'author_profile') {
                    contentHTML += `<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 40px;">`;
                    contentHTML += `<h2 class="chapter-title" style="margin-bottom: 30px; font-size: 32px; color: var(--primary);">저자 소개</h2>`;
                    contentHTML += `<div style="background: var(--canvas-parchment, #f5f5f7); border-radius: 18px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid var(--hairline, #e0e0e0); width: 80%; max-width: 600px; display:flex; flex-direction:column; align-items:center;">`;
                    contentHTML += `<h3 style="font-size: 24px; font-weight: 600; color: var(--ink); margin-bottom: 10px; margin-top: 0;">김중일 건축사</h3>`;
                    contentHTML += `<p style="font-size: 16px; color: var(--ink-muted-80); margin-bottom: 25px; margin-top: 0;">(주)진양엔지니어링건축사사무소 대표이사</p>`;
                    
                    contentHTML += `<ul class="author-list">`;
                    contentHTML += `<li>현(現) 서울시 건축심의위원</li>`;
                    contentHTML += `<li>현(現) 빈집 및 소규모 주택 정비 사업 소위원회 위원</li>`;
                    contentHTML += `<li>현(現) 강동구, 양천구 건축심의위원</li>`;
                    contentHTML += `<li>현(現) 강북구, 구로구 특정구역 모아타운 MP(Master Planner) 위원</li>`;
                    contentHTML += `</ul>`;
                    
                    contentHTML += `<p class="author-desc" style="border-top: 1px solid var(--hairline); padding-top: 20px; margin-bottom: 0;">"정책의 최전선에서 관(서울시)의 기조를 조율하며, 정비사업의 미래를 가장 뼈저리게 목도하고 있는 건축가의 진심 어린 조언이자 따뜻한 혁신의 기록."</p>`;
                    contentHTML += `</div>`;
                    contentHTML += `</div>`;
                }
"""

# Insert it right after the cover block
cover_block_end = "contentHTML += `</div>`;\n                }"

if "page.type === 'author_profile'" not in html:
    html = html.replace(cover_block_end, cover_block_end + "\n" + author_logic)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
