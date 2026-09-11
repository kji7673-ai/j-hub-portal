import json
import os
import shutil
import markdown

DB_PATH = "data/manual_db.json"
DOCS_DIR = "docs_minimal"

def build():
    if os.path.exists(DOCS_DIR):
        shutil.rmtree(DOCS_DIR)
    os.makedirs(DOCS_DIR)
    
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

    total_pages = len(db)

    for i, p in enumerate(db):
        html_out = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p['title']} - 진양엔지니어링 AI 교육 플랫폼</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ 
            margin: 0; padding: 0;
            background-color: #f4f5f7; 
            color: #111111; 
            font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif; 
            line-height: 1.6;
        }}
        
        .global-nav {{
            position: fixed; top: 0; left: 0; width: 100%; height: 60px;
            background-color: #111111; color: white;
            display: flex; align-items: center; padding: 0 20px;
            z-index: 1000;
        }}
        
        .global-nav a {{ color: white; text-decoration: none; }}
        .nav-brand {{ font-weight: bold; font-size: 16px; margin-right: 30px; }}
        
        #mobile-menu-btn {{
            background: none; border: none; color: white; font-size: 16px; font-weight: bold;
            margin-right: 15px; cursor: pointer; display: flex; align-items: center; gap: 5px;
        }}
        
        .top-menu {{
            display: flex; list-style: none; margin: 0; padding: 0; gap: 20px;
        }}
        
        .top-menu > li {{
            position: relative; padding: 20px 0; color: #ccc; font-size: 14px; cursor: pointer;
        }}
        
        .top-menu > li:hover {{ color: white; }}
        
        .dropdown-menu {{
            display: none; position: absolute; top: 60px; left: 0;
            background-color: white; border: 1px solid #ddd; border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1); list-style: none; padding: 10px 0;
            min-width: 250px; z-index: 1100;
        }}
        
        .top-menu > li:hover .dropdown-menu {{ display: block; }}
        
        .dropdown-menu li a {{
            display: block; padding: 10px 20px; color: #333; font-size: 14px;
        }}
        .dropdown-menu li a:hover {{ background-color: #f0f5ff; color: #0055ff; }}
        
        .sidebar {{
            position: fixed; top: 60px; left: -320px; width: 300px; height: calc(100vh - 60px);
            background: white; border-right: 1px solid #ddd; box-shadow: 5px 0 15px rgba(0,0,0,0.05);
            overflow-y: auto; transition: left 0.3s; z-index: 900;
            padding: 20px 0;
        }}
        
        .sidebar.open {{ left: 0; }}
        
        .sidebar-overlay {{
            position: fixed; top: 60px; left: 0; width: 100vw; height: calc(100vh - 60px);
            background: rgba(0,0,0,0.5); z-index: 800; display: none;
        }}
        .sidebar-overlay.open {{ display: block; }}
        
        .sidebar-item {{ padding: 12px 24px; border-bottom: 1px solid #f0f0f0; }}
        .sidebar-item a {{ color: #333; text-decoration: none; display: block; font-weight: bold; font-size: 14px; }}
        .sidebar-item:hover {{ background: #f9f9f9; }}
        .sidebar-item.active {{ background: #f0f5ff; border-left: 4px solid #0055ff; }}
        .sidebar-item.active a {{ color: #0055ff; }}
        
        .main-container {{
            padding-top: 60px;
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .viewer-page {{
            background: white;
            margin: 40px 20px;
            padding: 50px 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.04);
            border: 1px solid #eaeaea;
        }}
        
        .viewer-header {{
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 2px solid #000; padding-bottom: 20px; margin-bottom: 40px;
        }}
        
        .btn {{
            padding: 10px 20px; background: #f5f5f5; color: #333;
            text-decoration: none; border-radius: 6px; font-size: 14px; font-weight: bold;
            border: 1px solid #ddd;
        }}
        .btn:hover {{ background: #eaeaea; }}
        
        /* Markdown Content Styling */
        .viewer-content {{ font-size: 16px; color: #222; line-height: 1.8; }}
        .viewer-content h1 {{ font-size: 2.2rem; color: #000; margin-top: 40px; margin-bottom: 20px; }}
        .viewer-content h2 {{ font-size: 1.8rem; color: #000; margin-top: 40px; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .viewer-content h3 {{ font-size: 1.4rem; color: #0055ff; margin-top: 30px; margin-bottom: 15px; }}
        .viewer-content p {{ margin-bottom: 20px; }}
        .viewer-content ul, .viewer-content ol {{ margin-bottom: 20px; padding-left: 25px; }}
        .viewer-content li {{ margin-bottom: 8px; }}
        .viewer-content img {{ max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #eee; margin: 20px 0; }}
        .viewer-content blockquote {{ border-left: 4px solid #0055ff; background: #f0f5ff; padding: 15px 20px; margin: 20px 0; border-radius: 0 8px 8px 0; }}
        .viewer-content table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .viewer-content th, .viewer-content td {{ border: 1px solid #ddd; padding: 12px 15px; }}
        .viewer-content th {{ background: #f5f5f5; font-weight: bold; }}
        .viewer-content pre {{ background: #f5f5f5; padding: 15px; border-radius: 8px; overflow-x: auto; border: 1px solid #eee; }}
        .viewer-content code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 4px; font-family: monospace; }}
        .viewer-content pre code {{ background: transparent; padding: 0; }}
        
        @media (max-width: 768px) {{
            .top-menu {{ display: none; }}
            .viewer-page {{ margin: 0; padding: 30px 20px; border-radius: 0; border: none; box-shadow: none; }}
        }}
    </style>
</head>
<body>
    <div class="global-nav">
        <button id="mobile-menu-btn" onclick="toggleSidebar()">☰ 목차</button>
        <a href="index.html" class="nav-brand">(주)진양엔지니어링 AI 교육 플랫폼</a>
        
        <ul class="top-menu">
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
    <div class="sidebar" id="sidebar">
"""
        for cat, items in toc.items():
            html_out += f"        <div style=\"padding:15px 24px 5px;font-size:12px;color:#888;font-weight:bold;\">{cat}</div>\n"
            for item in items:
                link = "index.html" if item['idx'] == 0 else f"page_{item['idx']}.html"
                active = " active" if item['idx'] == i else ""
                html_out += f"        <div class=\"sidebar-item{active}\"><a href=\"{link}\">{item['title']}</a></div>\n"

        html_out += """
    </div>

    <div class="main-container">
        <div class="viewer-page">
            <div class="viewer-header">
"""
        if i > 0:
            prev_link = "index.html" if i - 1 == 0 else f"page_{i-1}.html"
            html_out += f"                <a href=\"{prev_link}\" class=\"btn\">◀ 이전 글</a>\n"
        else:
            html_out += "                <span class=\"btn\" style=\"visibility:hidden\">◀ 이전 글</span>\n"
            
        html_out += f"""
                <div style="text-align:center;">
                    <span style="font-size:12px;color:#666;display:block;margin-bottom:4px;">{p.get('category', '목차')}</span>
                    <strong>문서 {i+1} / {total_pages}</strong>
                </div>
"""
        if i < total_pages - 1:
            html_out += f"                <a href=\"page_{i+1}.html\" class=\"btn\">다음 글 ▶</a>\n"
        else:
            html_out += "                <span class=\"btn\" style=\"visibility:hidden\">다음 글 ▶</span>\n"
            
        html_out += f"""
            </div>
            
            <div class="viewer-content">
                {p['html']}
            </div>
            
            <div style="margin-top:60px;text-align:center;color:#666;font-size:13px;border-top:1px solid #eee;padding-top:30px;">
                발행: (주)진양엔지니어링건축사사무소 대표이사 김중일 건축사<br>문서 버전: v1.{total_pages}
            </div>
        </div>
    </div>
    
    <script>
    function toggleSidebar() {{
        document.getElementById('sidebar').classList.toggle('open');
        document.getElementById('sidebar-overlay').classList.toggle('open');
    }}
    </script>
</body>
</html>
"""
        filename = "index.html" if i == 0 else f"page_{i}.html"
        with open(os.path.join(DOCS_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html_out)

    print(f"Minimal Static site successfully built in '{DOCS_DIR}' directory.")

if __name__ == "__main__":
    build()
