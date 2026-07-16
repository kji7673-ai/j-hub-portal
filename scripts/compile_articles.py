import json
import os
import subprocess
import random

def compile_articles():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    daily_path = os.path.join(data_dir, 'daily_articles.json')
    weekly_path = os.path.join(data_dir, 'weekly_articles.json')
    
    all_articles = []
    
    # Load daily articles
    if os.path.exists(daily_path):
        with open(daily_path, 'r', encoding='utf-8') as f:
            all_articles.extend(json.load(f))
            
    # We no longer mix weekly articles into the 100 daily tiles.
    # Weekly briefings will be handled separately if needed.
    
    random.shuffle(all_articles)
    
    # Limit to 100 if we want to keep the 100-limit for the badge
    if len(all_articles) > 100:
        all_articles = all_articles[:100]
        
    js_content = "const articlesData = " + json.dumps(all_articles, ensure_ascii=False, indent=4) + ";\n"
    
    articles_js_path = os.path.join(base_dir, 'articles.js')
    with open(articles_js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Compiled {len(all_articles)} articles into {articles_js_path}")
    
    # Call build_jhub.py
    build_script = os.path.join(base_dir, 'build_jhub.py')
    print("Running build_jhub.py...")
    subprocess.run(['python3', build_script], cwd=base_dir, check=True)
    print("Compilation and build complete.")

if __name__ == "__main__":
    compile_articles()
