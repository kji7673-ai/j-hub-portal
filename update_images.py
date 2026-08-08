import json
import os

js_path = "book_data.js"
images_dir = "static/images"

with open(js_path, 'r', encoding='utf-8') as f:
    text = f.read()

json_start = text.find('{')
json_end = text.rfind('}') + 1

if json_start != -1 and json_end != -1:
    json_str = text[json_start:json_end]
    data = json.loads(json_str)
    
    updated_count = 0
    
    for i, page in enumerate(data.get('pages', [])):
        if page.get('type') in ['image_top', 'image_full']:
            expected_img_name = f"{i+1}.jpg"
            expected_img_path = os.path.join(images_dir, expected_img_name)
            
            # Check for alternative naming e.g., 105-1.jpg
            alt_img_name = f"{i+1}-1.jpg"
            alt_img_path = os.path.join(images_dir, alt_img_name)
            
            # Check for leading zero e.g., 01.jpg, 02.jpg
            padded_img_name = f"{i+1:02d}.jpg"
            padded_img_path = os.path.join(images_dir, padded_img_name)
            
            if os.path.exists(expected_img_path):
                page['image'] = f"static/images/{expected_img_name}"
                updated_count += 1
            elif os.path.exists(alt_img_path):
                page['image'] = f"static/images/{alt_img_name}"
                updated_count += 1
            elif os.path.exists(padded_img_path):
                page['image'] = f"static/images/{padded_img_name}"
                updated_count += 1
                
    data['pages'] = data.get('pages', [])
    
    new_js = "const bookData = " + json.dumps(data, ensure_ascii=False, indent=4) + ";\n"
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(new_js)
    
    print(f"Updated {updated_count} image paths successfully.")
else:
    print("Failed to find JSON data.")
