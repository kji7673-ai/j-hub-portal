import json
import os
import glob
import shutil
from PIL import Image

# Read prompts_v3.json
with open('prompts_v3.json', 'r') as f:
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

def make_white_transparent(img_path, dest_path):
    # Open the image and convert to RGBA
    img = Image.open(img_path).convert("RGBA")
    data = img.getdata()
    
    new_data = []
    for item in data:
        # Check if the pixel is near white
        # item is (R, G, B, A)
        avg = (item[0] + item[1] + item[2]) / 3
        # If the pixel is very bright, make it transparent
        # We can map the brightness to the alpha channel
        # 255 (white) -> alpha 0
        # 0 (black) -> alpha 255
        # This preserves anti-aliasing perfectly!
        # The color can be set to black (0, 0, 0), and opacity based on darkness
        alpha = int(255 - avg)
        new_data.append((0, 0, 0, alpha))
        
    img.putdata(new_data)
    img.save(dest_path, "PNG")

mapped_images = {}
for p in prompts:
    img_name = p['image_name']
    newest = find_newest_image(img_name)
    if newest:
        # Create a clean .png filename
        new_filename = img_name + '.png'
        dest_path = os.path.join(static_images_dir, new_filename)
        docs_dest_path = os.path.join(docs_static_images_dir, new_filename)
        
        # Process and save transparent PNG
        make_white_transparent(newest, dest_path)
        shutil.copy2(dest_path, docs_dest_path)
        
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

print(f"Successfully processed, copied, and updated {len(mapped_images)} images.")
