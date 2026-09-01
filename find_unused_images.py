import os
import re

used_images = set()

# Check book_data.js
with open('book_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
for img in re.findall(r'[\'"]([^\'"]+\.(?:jpg|png|jpeg|gif))[\'"]', content, flags=re.IGNORECASE):
    used_images.add(os.path.basename(img))

# Check index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
for img in re.findall(r'[\'"]([^\'"]+\.(?:jpg|png|jpeg|gif))[\'"]', content, flags=re.IGNORECASE):
    used_images.add(os.path.basename(img))

images_dir = 'static/images'
all_images = set(os.listdir(images_dir))

unused = all_images - used_images
print(f"Total unused images: {len(unused)}")

# Delete unused images
count = 0
for img in unused:
    path = os.path.join(images_dir, img)
    if os.path.isfile(path):
        os.remove(path)
        count += 1
print(f"Deleted {count} unused images.")
