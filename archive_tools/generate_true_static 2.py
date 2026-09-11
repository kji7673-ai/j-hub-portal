import json
import os
import shutil
import markdown

DB_PATH = "data/manual_db.json"
DOCS_DIR = "docs"

def build():
    if os.path.exists(DOCS_DIR):
        shutil.rmtree(DOCS_DIR)
    os.makedirs(DOCS_DIR)
    
    shutil.copytree("static", os.path.join(DOCS_DIR, "static"))
    
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
        
    toc = {}
    for i, p in enumerate(db):
        cat = p.get("category", "목차")
        if cat not in toc:
            toc[cat] = []
        toc[cat].append({
            "idx": i, 
            "title": p["title"]
        })
        p["html"] = markdown.markdown(p["content"], extensions=['fenced_code', 'tables'])

    with open("templates/viewer.html", "r", encoding="utf-8") as f:
        template_content = f.read()
        
    css_start = template_content.find("<style>")
    css_end = template_content.find("</style>") + 8
    css_content = template_content[css_start:css_end]

    total_pages = len(db)

    for i, p in enumerate(db):
        html_out = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{p['title']} - (주)진양엔지니어링 AI 교육 플랫폼</title>
    {css_content}
    <style>
        body {{ background-color: #fcfcfc; color: #222; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}
        #viewer-page {{ max-width: 800px; width: 100%; background-color: #ffffff; padding: 60px 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #e0e0e0; margin: 40px auto; }}
        @media (max-width: 768px) {{
            #viewer-page {{ padding: 30px 20px; border: none; box-shadow: none; margin: 0 auto; }}
            .main-container {{ padding-top: 60px; }}
        }}
    </style>
</head>
<body>
    <div class="global-nav visible" id="global-nav" style="transform: translateY(0);">
        <button id="mobile-menu-btn" onclick="toggleSidebar()">
            ☰ <span>목차</span>
        </button>
        <a href="index.html" class="nav-brand">
            (주)진양엔지니어링 AI 교육 플랫폼
        </a>
        <ul class="top-menu" id="top-menu">
"""
        for cat, items in toc.items():
            html_out += f"            <li>{cat}\n                <ul class=\"dropdown-menu\">\n"
            for item in items:
                link = "index.html" if item['idx'] == 0 else f"page_{item['idx']}.html"
                html_out += f"                    <li><a href=\"{link}\">{item['title']}</a></li>\n"
            html_out += "                </ul>\n            </li>\n"

        html_out += """
        </ul>
    </div>

    <div class="sidebar-overlay" id="sidebar-overlay" onclick="toggleSidebar()"></div>
    <div class="sidebar" id="entry-list">
"""
        for cat, items in toc.items():
            html_out += f"        <div style=\"padding: 15px 24px 5px; font-size: 12px; font-weight: bold; color: #666;\">{cat}</div>\n"
            for item in items:
                link = "index.html" if item['idx'] == 0 else f"page_{item['idx']}.html"
                active_class = " active" if item['idx'] == i else ""
                html_out += f"        <div class=\"entry-list-item{active_class}\">\n"
                html_out += f"            <a href=\"{link}\" style=\"text-decoration:none; color:inherit;\"><h4>{item['title']}</h4></a>\n"
                html_out += "        </div>\n"

        html_out += """
    </div>

    <div class="main-container">
        <div id="viewer-page" style="display:block;">
            <div class="viewer-header">
"""
        if i > 0:
            prev_link = "index.html" if i - 1 == 0 else f"page_{i-1}.html"
            html_out += f"                <a href=\"{prev_link}\" class=\"viewer-nav-btn\">◀ 이전 글</a>\n"
        else:
            html_out += "                <span class=\"viewer-nav-btn disabled\" style=\"visibility:hidden;\">◀ 이전 글</span>\n"
            
        html_out += f"""
                <div style="text-align:center;">
                    <span style="font-size: 12px; color: #666; display:block; margin-bottom:4px;">{p.get('category', '목차')}</span>
                    <span style="font-weight:600; font-size: 14px;">문서 {i+1} / {total_pages}</span>
                </div>
"""
        if i < total_pages - 1:
            html_out += f"                <a href=\"page_{i+1}.html\" class=\"viewer-nav-btn\">다음 글 ▶</a>\n"
        else:
            html_out += "                <span class=\"viewer-nav-btn disabled\" style=\"visibility:hidden;\">다음 글 ▶</span>\n"
            
        html_out += f"""
            </div>
            
            <div class="viewer-content-wrapper" style="color: #222;">
                {p['html']}
            </div>
            
            <div style="margin-top: 80px; border-top: 1px solid #e0e0e0; padding-top: 30px; text-align: center; color: #666; font-size: 0.9rem; line-height: 1.8;">
                발행: <strong>(주)진양엔지니어링건축사사무소 대표이사 김중일 건축사</strong><br>
                문서 버전: <strong>v1.{total_pages}</strong>
            </div>
        </div>
    </div>

    <script>
        function toggleSidebar() {{
            document.getElementById('entry-list').classList.toggle('open');
            document.getElementById('sidebar-overlay').classList.toggle('open');
        }}
    </script>
</body>
</html>
"""
        filename = "index.html" if i == 0 else f"page_{i}.html"
        with open(os.path.join(DOCS_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html_out)

    print(f"True Static site successfully built in '{DOCS_DIR}' directory.")

if __name__ == "__main__":
    build()
