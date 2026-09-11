import re
import json

html_path = "book_studio.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

toc_btn_html = """
    <!-- TOC Floating Button -->
    <button class="icon-btn toc-btn" title="목차 보기" style="position:fixed; top:20px; right:20px; z-index:1500; background:rgba(255,255,255,0.9); backdrop-filter:blur(10px); border:1px solid #e0e0e0; border-radius:50%; width:48px; height:48px; box-shadow:0 4px 12px rgba(0,0,0,0.1); cursor:pointer; display:flex; justify-content:center; align-items:center; transition:all 0.2s;">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#1d1d1f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
    </button>
"""

if "<!-- TOC Floating Button -->" not in html:
    html = html.replace('<body>', '<body>\n' + toc_btn_html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
