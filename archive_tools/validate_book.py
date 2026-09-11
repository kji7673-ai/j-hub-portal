import json
import os
import sys

BOOK_DATA_PATH = "book_data.js"
IMAGES_DIR = "static/images"

def validate_book():
    print(f"Validating {BOOK_DATA_PATH}...")
    
    if not os.path.exists(BOOK_DATA_PATH):
        print(f"❌ Error: {BOOK_DATA_PATH} not found.")
        sys.exit(1)
        
    with open(BOOK_DATA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find JSON block
    json_start = content.find('{')
    json_end = content.rfind('};')
    if json_end == -1:
        json_end = content.rfind('}')
    
    if json_start == -1 or json_end == -1:
        print("❌ Error: Cannot locate JSON object inside book_data.js. Check brackets.")
        sys.exit(1)
        
    try:
        data = json.loads(content[json_start:json_end+1])
        print("✅ JSON syntax is valid.")
    except json.JSONDecodeError as e:
        print(f"❌ JSON Syntax Error in {BOOK_DATA_PATH}: {e}")
        print("Please check for missing commas or unescaped quotes.")
        sys.exit(1)
        
    pages = data.get('pages', [])
    print(f"Total pages: {len(pages)}")
    
    missing_images = []
    
    for i, page in enumerate(pages):
        img_path = page.get('image')
        if img_path:
            # Check if file exists
            if not os.path.exists(img_path):
                missing_images.append((i+1, img_path))
                
    if missing_images:
        print(f"\n⚠️ WARNING: Found {len(missing_images)} missing image files!")
        for idx, path in missing_images:
            print(f" - Page {idx}: '{path}' does not exist.")
        print("\nPlease upload these images or correct the paths in J-Hub Studio.")
    else:
        print("✅ All image paths are valid.")
        
    print("\nValidation completed successfully.")

if __name__ == "__main__":
    validate_book()
