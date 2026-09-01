import json
import os
import glob
import shutil

# Read prompts.json
with open('prompts.json', 'r') as f:
    prompts = json.load(f)

# Find all generated images in the brain directory
brain_dir = os.path.expanduser('~/.gemini/antigravity/brain')
static_images_dir = 'static/images'
docs_static_images_dir = 'docs/static/images'

if not os.path.exists(static_images_dir):
    os.makedirs(static_images_dir)

if not os.path.exists(docs_static_images_dir):
    os.makedirs(docs_static_images_dir)

all_images = glob.glob(os.path.join(brain_dir, '*', '*.jpg')) + glob.glob(os.path.join(brain_dir, '*', '*.png'))

def find_newest_image(image_name):
    matches = []
    for img_path in all_images:
        filename = os.path.basename(img_path)
        name_without_ext = os.path.splitext(filename)[0]
        if name_without_ext == image_name or name_without_ext.startswith(image_name + '_'):
            matches.append(img_path)
    
    if not matches:
        return None
    
    matches.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return matches[0]

mapped_images = {}
for p in prompts:
    img_name = p['image_name']
    newest = find_newest_image(img_name)
    if newest:
        new_filename = os.path.basename(newest)
        dest_path = os.path.join(static_images_dir, new_filename)
        docs_dest_path = os.path.join(docs_static_images_dir, new_filename)
        shutil.copy2(newest, dest_path)
        shutil.copy2(newest, docs_dest_path)
        mapped_images[p['index']] = 'static/images/' + new_filename
    else:
        print(f"Warning: No image found for {img_name}")

# Now update book_data.js
with open('book_data.js', 'r') as f:
    content = f.read()

import re
match = re.search(r'const\s+bookData\s*=\s*(\{.*?\});\n*(?:if\s*\(\s*typeof\s*module|$)', content, re.DOTALL)
data = json.loads(match.group(1))

for index, new_image_path in mapped_images.items():
    if index < len(data['pages']):
        data['pages'][index]['image'] = new_image_path

new_json = json.dumps(data, ensure_ascii=False, indent=4)
new_content = content[:match.start(1)] + new_json + content[match.end(1):]

with open('book_data.js', 'w') as f:
    f.write(new_content)

with open('docs/book_data.js', 'w') as f:
    f.write(new_content)

print(f"Successfully copied and updated {len(mapped_images)} images.")
