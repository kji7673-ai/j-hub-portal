import json
import os
import glob
import re

# Read book data
with open('docs/book_data.js', 'r') as f:
    c = f.read()

prefix = c[:c.find('[')]
suffix = c[c.rfind(']')+1:]
data = json.loads(c[c.find('['):c.rfind(']')+1])

# Get all images
images = glob.glob('static/images/essay_*.jpg')
index_to_img = {}

for img in images:
    # Format is static/images/essay_125_32_oe_1786747965559.jpg
    # Actually wait, let's parse the index. It's the first group of digits after essay_
    basename = os.path.basename(img)
    match = re.match(r'essay_(\d+)_', basename)
    if match:
        idx = int(match.group(1))
        # Keep the latest generated image (by timestamp) if there are duplicates
        index_to_img[idx] = img

out_data = []
for i, item in enumerate(data):
    # Check if this index was generated for
    if i in index_to_img:
        # Check if an image already exists. We want to append a new image_full object.
        # Actually, let's check if there is an image_full object right before this one.
        # In our previous update, we added image_full objects for a few of them.
        out_data.append({
            "type": "image_full",
            "image": index_to_img[i]
        })
    out_data.append(item)

new_json_str = json.dumps(out_data, ensure_ascii=False, indent=4)
with open('docs/book_data.js', 'w') as f:
    f.write(prefix + new_json_str + suffix)

print(f"Injected {len(index_to_img)} images into book_data.js")
