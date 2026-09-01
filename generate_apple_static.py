import json
import os
import shutil
import markdown
import re
import datetime
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

DB_PATH = "data/manual_db.json"
DOCS_DIR = "docs_apple"
BUILD_VERSION = str(int(datetime.datetime.now().timestamp()))

def strip_markdown(text):
    text = re.sub(r'#+\s', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n+', ' ', text)
    return text.strip()

def build(output_dir, include_internal=False):
    # 1. 자동 오류 수정 파이프라인 (Auto-Healer) 실행
    try:
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from scripts.auto_healer_content import run_pipeline
        run_pipeline()
    except Exception as e:
        print(f"⚠️ Auto-Healer 실행 실패: {e}")

    if os.path.exists(output_dir):
        print("  - removing output dir")
        shutil.rmtree(output_dir)
    print("  - making output dir")
    os.makedirs(output_dir)
    
    if os.path.exists("static"):
        print("  - symlinking static dir")
        os.symlink("../static", os.path.join(output_dir, "static"))
    if os.path.exists("data"):
        os.symlink("../data", os.path.join(output_dir, "data"))

    # Copy PWA files if they exist
    for pwa_file in ["sw.js", "icon-192.png", "icon-512.png"]:
        if os.path.exists(pwa_file):
            shutil.copy(pwa_file, os.path.join(output_dir, pwa_file))
        
    full_db = []
    content_dir = "content"
    if os.path.exists(content_dir):
        print("  - walking content dir")
        for root, dirs, files in os.walk(content_dir):
            for file in sorted(files):
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content_raw = f.read()
                    
                    meta = {}
                    md_content = content_raw
                    if content_raw.startswith("---json"):
                        parts = content_raw.split("---", 2)
                        if len(parts) >= 3:
                            meta_json = parts[1].replace("json", "").strip()
                            try:
                                meta = json.loads(meta_json)
                            except Exception as e:
                                print(f"  ⚠️ 메타데이터 파싱 실패: {file} - {e}")
                            md_content = parts[2].strip()
                    
                    doc = meta.copy()
                    doc["content"] = md_content
                    doc["id"] = int(meta.get("id", 0))
                    full_db.append(doc)
    
    full_db.sort(key=lambda x: x.get("id", 0))

    if not include_internal:
        db = [p for p in full_db if not p.get("is_internal", False)]
    else:
        db = full_db
    
    seen_ids = {}
    max_id = max((d.get("id", 0) for d in db), default=0)
    id_fixed = 0
    for d in db:
        doc_id = d.get("id", -1)
        if doc_id in seen_ids:
            max_id += 1
            old_id = doc_id
            d["id"] = max_id
            id_fixed += 1
            print(f"  ⚠️ ID 중복 자동 수정: {old_id} → {max_id} ({d.get('title','')[:30]})")
        seen_ids[doc_id] = True
    if id_fixed > 0:
        print(f"  🔧 총 {id_fixed}건의 ID 중복을 자동 수정했습니다.")
        
    toc = {}
    search_data = []
    
    print("  - generating HTML for pages")
    for i, p in enumerate(db):
        print(f"    - parsing page {i}: {p['title']}")
        track = p.get("track", "sop")
        if track not in toc:
            toc[track] = []
        toc[track].append({
            "idx": i, 
            "title": p["title"],
            "date": p.get("date", "")
        })
        print(f"      - running markdown")
        p["html"] = markdown.markdown(p["content"], extensions=['fenced_code', 'tables'])
        print(f"      - running restore_mermaid")
        def restore_mermaid(m):
            inner = m.group(1)
            inner = inner.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
            return '<div class="mermaid"' + inner + '</div>'
        p["html"] = re.sub(r'<div class="mermaid"(.*?)</div>', restore_mermaid, p["html"], flags=re.DOTALL)
        print(f"      - done restore_mermaid")

        first_p_match = re.search(r'<p>(.*?)</p>', p["html"], re.DOTALL)
        if first_p_match and len(first_p_match.group(1)) > 30:
            quick_win_html = f'<div class="alert alert-info" style="margin-top:20px;"><strong>⏱️ 핵심 30초 요약</strong><br>{first_p_match.group(1)}</div>'
            p["html"] = p["html"].replace(first_p_match.group(0), quick_win_html, 1)
        
        filename = f"page_{i}.html"
        search_data.append({
            "id": i,
            "title": p["title"],
            "category": track,
            "content": strip_markdown(p["content"]),
            "url": filename
        })

    with open(os.path.join(output_dir, "search_index.js"), "w", encoding="utf-8") as f:
        f.write("const searchIndex = " + json.dumps(search_data, ensure_ascii=False) + ";")
    
    manifest = {
      "name": "J-Hub Portal",
      "short_name": "J-Hub",
      "description": "진양엔지니어링 AI 교육 플랫폼",
      "start_url": "./index.html",
      "display": "standalone",
      "background_color": "#f5f5f7",
      "theme_color": "#000000",
      "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}
      ]
    }
    with open(os.path.join(output_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    env = Environment(loader=FileSystemLoader('templates'))
    
    track_meta = {
        "ceo": {"title": "트랙 1. CEO & 임원진 (비전과 통제)", "icon": "🌱", "desc": "AI 시대의 건축 비전, 7대 전략, Archi-Synapse 철학, 레드팀 방법론", "badge_class": "track-badge-a", "color": "#2e7d32"},
        "sop": {"title": "트랙 2. 설계 실무진 (SOP와 활용)", "icon": "🔧", "desc": "프롬프트 실습, 환각 방지, K-배치 알고리즘, 실전 SOP", "badge_class": "track-badge-b", "color": "#1565c0"},
        "system": {"title": "트랙 3. 시스템 & IT (구축과 연동)", "icon": "🏗️", "desc": "UX/UI 고도화, 포털 구축, DocReview, 빅데이터 연동", "badge_class": "track-badge-d", "color": "#6a1b9a"},
        "arch": {"title": "트랙 4. 건축 실무 가이드 (자료실)", "icon": "🏛️", "desc": "공동주택 법정 인증제도, 관련 부담금, 세제 혜택 등 핵심 설계 정보", "badge_class": "track-badge-c", "color": "#d84315"},
    }
    level_labels = {1: "🌱 Lv.1 입문", 2: "🔧 Lv.2 실무", 3: "🏗️ Lv.3 심화"}
    level_css = {1: "level-1", 2: "level-2", 3: "level-3"}
    
    today_date = datetime.datetime.now()
    tracks_for_index = {}
    for track_key, items in toc.items():
        meta = track_meta.get(track_key, track_meta["sop"])
        cat_short = meta["title"]
        track_items = []
        for item in items:
            is_fresh = False
            try:
                doc_date_str = db[item['idx']].get('date', '')
                if doc_date_str and (today_date - datetime.datetime.strptime(doc_date_str, "%Y-%m-%d")).days <= 14:
                    is_fresh = True
            except (ValueError, KeyError): pass
            
            doc_level = db[item['idx']].get('level', 1)
            summary = db[item['idx']].get('summary', '')
            summary_text = summary[:60] + '...' if len(summary) > 60 else summary
            if not summary_text:
                summary_text = cat_short + " 트랙의 교육 문서"
                
            track_items.append({
                "idx": item['idx'],
                "title": item['title'],
                "is_fresh": is_fresh,
                "level_label": level_labels.get(doc_level, "Lv.1"),
                "level_class": level_css.get(doc_level, "level-1"),
                "summary": summary_text
            })
        tracks_for_index[track_key] = {
            "title": cat_short,
            "icon": meta["icon"],
            "desc": meta["desc"],
            "badge_class": meta["badge_class"],
            "docs": track_items
        }
        
    index_template = env.get_template('index.html')
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_template.render(
            toc=toc, 
            tracks=tracks_for_index, 
            total_pages=len(db)
        ))
        
    page_template = env.get_template('page.html')
    for i, p in enumerate(db):
        doc_level = p.get('level', 1)
        prev_link = f"page_{i-1}.html" if i > 0 else None
        next_link = f"page_{i+1}.html" if i < len(db) - 1 else None
        
        with open(os.path.join(output_dir, f"page_{i}.html"), "w", encoding="utf-8") as f:
            f.write(page_template.render(
                toc=toc,
                current_idx=i,
                id=p.get("id", i),
                title=p["title"],
                date=p.get("date", "2026-07-20"),
                level=doc_level,
                level_class=level_css.get(doc_level, "level-1"),
                level_label=level_labels.get(doc_level, "Lv.1"),
                summary=p.get("summary", ""),
                content=p["html"],
                prev_link=prev_link,
                next_link=next_link
            ))
            
    print(f"✅ Static site successfully built in '{output_dir}' directory using Jinja2 templates.")

if __name__ == "__main__":
    print("🚀 [Track A] Building PUBLIC site (docs_apple)...")
    build("docs_apple", include_internal=False)
    
    print("🔒 [Track B] Building INTERNAL site (docs_internal)...")
    build("docs_internal", include_internal=True)
    
    print("✅ Two-Track Build System Complete!")
