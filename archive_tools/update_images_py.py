import json
import re
import os
import shutil

book_data_path = "docs/book_data.js"
source_dir = "/Users/joongilkim/Downloads/책이미지"
dest_dir = "docs/static/images"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir, exist_ok=True)

with open(book_data_path, "r", encoding="utf-8") as f:
    content = f.read()

# Instead of parsing JSON (which failed), let's just find and replace all instances of "static/images/.*\.png"
# But we need to do it only 116 times, and in the order they appear.
# Wait, we can find all matches of `"image":\s*"(static/images/[^"]+\.png)"`
matches = list(re.finditer(r'"image"\s*:\s*"(static/images/[^"]+\.png)"', content))

print("Found PNG images:", len(matches))

updated_count = 0
png_counter = 1

# Process each match
new_content = ""
last_end = 0

for match in matches:
    new_content += content[last_end:match.start(1)]
    
    # Calculate the new name
    new_num = 118 - png_counter
    new_name = str(new_num).zfill(2) + ".jpg"
    src_path = os.path.join(source_dir, new_name)
    
    dest_name = "user_" + new_name
    dest_path = os.path.join(dest_dir, dest_name)
    
    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)
        new_content += "static/images/" + dest_name
        updated_count += 1
    else:
        print("Warning: not found", src_path)
        new_content += match.group(1) # Keep original if not found
    
    png_counter += 1
    last_end = match.end(1)

new_content += content[last_end:]

# Write back
with open(book_data_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Updated images:", updated_count)
