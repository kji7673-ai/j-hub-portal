import os

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_server.py', 'r', encoding='utf-8') as f:
    server_code = f.read()

# We need to insert the import base64, time at the top
if 'import base64' not in server_code:
    server_code = server_code.replace('import json', 'import json\nimport base64\nimport time')

# Add the /api/upload_image endpoint before the if __name__ block
upload_endpoint = """
@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    data = request.json
    page_index = data.get('page_index')
    image_data = data.get('image_data')  # Expected format: data:image/jpeg;base64,...
    
    if page_index is None or not image_data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400
        
    try:
        # 1. Parse base64
        header, encoded = image_data.split(",", 1)
        ext = "jpg"
        if "png" in header:
            ext = "png"
            
        file_data = base64.b64decode(encoded)
        filename = f"upload_{int(time.time())}_{page_index}.{ext}"
        filepath = os.path.join("static", "images", filename)
        
        # Ensure dir exists
        os.makedirs(os.path.join("static", "images"), exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(file_data)
            
        image_url = f"static/images/{filename}"
        
        # 2. Update book_data.js
        if not os.path.exists(BOOK_DATA_PATH):
            return jsonify({"status": "error", "message": "book_data.js not found"}), 404
            
        with open(BOOK_DATA_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        
        book_json = json.loads(content[json_start:json_end])
        
        if 0 <= page_index < len(book_json.get('pages', [])):
            page_obj = book_json['pages'][page_index]
            page_obj['image'] = image_url
            
            # If text_only, promote to image_top. If cover, maybe leave it or make it image_full?
            if page_obj.get('type') == 'text_only':
                page_obj['type'] = 'image_top'
            elif page_obj.get('type') == 'cover':
                page_obj['type'] = 'image_full'
                
            new_js_content = "const bookData = " + json.dumps(book_json, ensure_ascii=False, indent=4) + ";\\n"
            with open(BOOK_DATA_PATH, 'w', encoding='utf-8') as f:
                f.write(new_js_content)
                
            return jsonify({"status": "success", "image_url": image_url})
        else:
            return jsonify({"status": "error", "message": "Page index out of bounds"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
"""

if '/api/upload_image' not in server_code:
    server_code = server_code.replace("if __name__ == '__main__':", upload_endpoint + "\nif __name__ == '__main__':")

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_server.py', 'w', encoding='utf-8') as f:
    f.write(server_code)
