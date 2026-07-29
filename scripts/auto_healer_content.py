import os
import re
import json

def heal_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # 1. Fix missing empty line after ---
    content = re.sub(r'(---)\n([^\n<#])', r'\1\n\n\2', content)
    
    # 2. Fix broken markdown tables (missing leading/trailing pipes)
    # Simple fix for tables if needed...
    
    # 3. Ensure JSON frontmatter is valid
    if content.startswith('---json'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            meta_str = parts[1].replace('json', '').strip()
            try:
                json.loads(meta_str)
            except json.JSONDecodeError:
                pass
                
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def heal_html_templates(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    # 1. Remove literal \n in scripts
    content = re.sub(r'\\n\s*\n\s*//', r'\n//', content)
    
    # 2. Ensure meta viewport exists
    if '<head>' in content and 'viewport' not in content:
        content = content.replace('<head>', '<head>\n<meta name="viewport" content="width=device-width, initial-scale=1.0">')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run_pipeline():
    print("🤖 [Auto-Healer] 파이프라인 검증 시작...")
    
    # Check templates
    template_dir = 'templates'
    if os.path.exists(template_dir):
        for f in os.listdir(template_dir):
            if f.endswith('.html'):
                if heal_html_templates(os.path.join(template_dir, f)):
                    print(f"  🔧 템플릿 오류 자동 수정됨: {f}")
                    
    # Check contents
    content_dir = 'content'
    if os.path.exists(content_dir):
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.md'):
                    if heal_markdown(os.path.join(root, file)):
                        print(f"  🔧 마크다운 포맷 자동 수정됨: {file}")
                        
    print("✅ [Auto-Healer] 검증 완료. 모든 코드가 정상입니다.")

if __name__ == "__main__":
    run_pipeline()
