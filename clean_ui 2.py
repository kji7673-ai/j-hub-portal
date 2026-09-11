import re
import shutil

file_path = 'docs/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove box-shadows from .book-container
content = re.sub(r'box-shadow:\s*inset[^;]+;\s*/\* Outer elevation \*/', '', content)
content = re.sub(r'box-shadow:\s*inset[^;]+;', '', content)
# Replace all #f5f5f7 and var(--canvas-parchment) with #ffffff
content = content.replace('#f5f5f7', '#ffffff')
content = content.replace('var(--canvas-parchment)', '#ffffff')
content = content.replace('var(--canvas-parchment, #f5f5f7)', '#ffffff')

# Remove box-shadows and borders from the injected JS containers
content = re.sub(r'box-shadow:\s*0\s+4px\s+20px\s+rgba\(0,0,0,0\.05\);', 'box-shadow: none;', content)
content = re.sub(r'border:\s*1px\s+solid\s+var\(--hairline,\s*#e0e0e0\);', 'border: none;', content)

# Remove border-radius if they want a clean flat look for text containers
content = re.sub(r'border-radius:\s*18px;', 'border-radius: 0;', content)

# Remove background gray from book container
content = re.sub(r'background-color:\s*#f8f9fa;', 'background-color: #ffffff;', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

shutil.copy2(file_path, 'index.html')
print("Cleaned docs/index.html and copied to index.html")
