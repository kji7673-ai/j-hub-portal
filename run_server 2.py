from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import subprocess
import time

app = Flask(__name__)

@app.route('/edu/')
@app.route('/edu/<path:filename>')
def serve_edu(filename="index.html"):
    import os
    from flask import send_from_directory
    if not os.path.exists(os.path.join('docs_apple', filename)):
        return "File not found in docs_apple", 404
    return send_from_directory('docs_apple', filename)


DB_PATH = "data/manual_db.json"
PDF_PATH = "통합_교육매뉴얼_마스터.pdf"

def load_db():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/")
def index():
    db = load_db()
    # Simple redirect to first page
    if db:
        return viewer(0)
    return "No pages found."

@app.route("/page/<int:page_idx>")
def viewer(page_idx):
    db = load_db()
    if page_idx < 0 or page_idx >= len(db):
        return "Page not found", 404
        
    page_data = db[page_idx]
    
    # Group TOC by category
    toc = {}
    for i, p in enumerate(db):
        cat = p.get("category", "목차")
        if cat not in toc:
            toc[cat] = []
        toc[cat].append({
            "idx": i, 
            "title": p["title"],
            "summary": p.get("summary", "")
        })
    
    return render_template("viewer.html", 
                           page=page_data, 
                           idx=page_idx, 
                           total=len(db),
                           toc=toc)

@app.route("/api/save_data", methods=["POST"])
def save_data():
    req = request.json
    page_id = req.get("id")
    
    db = load_db()
    for p in db:
        if p["id"] == page_id:
            if "ai_instruction" in req:
                p["ai_instruction"] = req["ai_instruction"]
            if "ceo_thoughts" in req:
                p["ceo_thoughts"] = req["ceo_thoughts"]
            if "whiteboard_data" in req:
                p["whiteboard_data"] = req["whiteboard_data"]
            if "content" in req:
                p["content"] = req["content"]
            break
            
    save_db(db)
    return jsonify({"status": "success"})

@app.route("/api/new_page", methods=["POST"])
def new_page():
    req = request.json
    title = req.get("title", "새로운 페이지")
    
    db = load_db()
    new_id = str(len(db))
    new_idx = len(db)
    
    new_page_data = {
        "id": new_id,
        "title": title,
        "content": f'<div class="page tile-light"><div class="content-wrap"><h2 class="display-lg hairline-bottom">{title}</h2><p class="body-text">이곳에 새로운 내용을 작성해 주십시오.</p></div></div>',
        "ai_instruction": "",
        "ceo_thoughts": "",
        "whiteboard_data": "",
        "category": "추가된 페이지",
        "summary": "새롭게 추가된 내용입니다."
    }
    
    db.append(new_page_data)
    save_db(db)
    
    return jsonify({"status": "success", "new_idx": new_idx})

@app.route("/api/export_pdf", methods=["POST"])
def export_pdf():
    # Render PDF using Modular Document Rendering Engine
    db = load_db()
    
    # 1. Create scratch/chapters directory
    scratch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scratch", "chapters")
    os.makedirs(scratch_dir, exist_ok=True)
    
    # Clean previous chapter files
    for f in os.listdir(scratch_dir):
        if f.endswith(".html"):
            os.remove(os.path.join(scratch_dir, f))
            
    # 2. Generate HTML file for each chapter
    for i, p in enumerate(db):
        idx_str = f"{i:02d}"
        chapter_path = os.path.join(scratch_dir, f"ch{idx_str}.html")
        
        # Build content for this chapter with Apple Design
        html_out = f'<div class="page">\n'
        html_out += f'<div class="content-area" style="flex: 1; border-bottom: 1px solid var(--hairline); padding-bottom: 24px; margin-bottom: 24px;">\n{p["content"]}\n</div>\n'
        html_out += f'<div class="comments-area" style="display: flex; gap: 24px; height: 280px;">\n'
        
        # 1. 수정 요청
        html_out += f'<div class="comment-box" style="flex: 1; background: var(--canvas); border: 1px solid var(--hairline); border-radius: 18px; padding: 24px; font-size: 14px; overflow: hidden;"><div class="box-title" style="font-family: \'SF Pro Display\', system-ui, sans-serif; font-size: 17px; font-weight: 600; color: var(--primary); margin-bottom: 16px; border-bottom: 1px solid var(--hairline); padding-bottom: 12px; letter-spacing: -0.374px;">✏️ 수정 요청사항</div><p style="font-family: \'SF Pro Text\', system-ui, sans-serif; font-size: 14px; line-height: 1.43; letter-spacing: -0.224px; color: var(--ink);">{p.get("ai_instruction", "")}</p></div>\n'
        # 2. 나의 생각
        ceo_thoughts = p.get("ceo_thoughts", "").replace(chr(10), "<br>")
        html_out += f'<div class="comment-box" style="flex: 1; background: var(--canvas); border: 1px solid var(--hairline); border-radius: 18px; padding: 24px; font-size: 14px; overflow: hidden;"><div class="box-title" style="font-family: \'SF Pro Display\', system-ui, sans-serif; font-size: 17px; font-weight: 600; color: var(--primary); margin-bottom: 16px; border-bottom: 1px solid var(--hairline); padding-bottom: 12px; letter-spacing: -0.374px;">💡 경영진 인사이트</div><p style="font-family: \'SF Pro Text\', system-ui, sans-serif; font-size: 14px; line-height: 1.43; letter-spacing: -0.224px; color: var(--ink);">{ceo_thoughts}</p></div>\n'
        # 3. 화이트보드
        wb_data = p.get("whiteboard_data", "")
        if wb_data and len(wb_data) > 100:
            html_out += f'<div class="comment-box" style="flex: 1; background: var(--canvas); border: 1px solid var(--hairline); border-radius: 18px; padding: 24px; overflow: hidden;"><div class="box-title" style="font-family: \'SF Pro Display\', system-ui, sans-serif; font-size: 17px; font-weight: 600; color: var(--primary); margin-bottom: 16px; border-bottom: 1px solid var(--hairline); padding-bottom: 12px; letter-spacing: -0.374px;">🎨 스케치 도면</div><div style="height: calc(100% - 44px); border-radius: 8px; overflow: hidden;"><img class="wb-img" style="width: 100%; height: 100%; object-fit: contain;" src="{wb_data}"/></div></div>\n'
        else:
            html_out += f'<div class="comment-box" style="flex: 1; background: var(--canvas); border: 1px solid var(--hairline); border-radius: 18px; padding: 24px; overflow: hidden;"><div class="box-title" style="font-family: \'SF Pro Display\', system-ui, sans-serif; font-size: 17px; font-weight: 600; color: var(--primary); margin-bottom: 16px; border-bottom: 1px solid var(--hairline); padding-bottom: 12px; letter-spacing: -0.374px;">🎨 스케치 도면</div><p style="font-family: \'SF Pro Text\', system-ui, sans-serif; font-size: 14px; line-height: 1.43; letter-spacing: -0.224px; color: var(--body-muted); text-align: center; margin-top: 40px;">(스케치 없음)</p></div>\n'
            
        html_out += '</div>\n</div>\n'
        
        with open(chapter_path, "w", encoding="utf-8") as f:
            f.write(html_out)
            
    # 3. Execute build_document.py
    build_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".agents", "skills", "모듈형-문서렌더링-엔진", "scripts", "build_document.py"))
    
    cmd = [
        "python3",
        build_script,
        "--chapters_dir", scratch_dir,
        "--output_name", PDF_PATH,
        "--title", "회사 교육 자료 매뉴얼"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return jsonify({"status": "success", "file": PDF_PATH})
    except subprocess.CalledProcessError as e:
        print("Error generating PDF:", e.stderr.decode('utf-8'))
        return jsonify({"status": "error", "message": e.stderr.decode('utf-8')})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5050)
