import json
import re

js_path = "book_data.js"

with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

# The JS file looks like: const bookData = { ... };
# Let's extract the JSON part.
json_start = js_text.find('{')
json_end = js_text.rfind('}') + 1

if json_start != -1 and json_end != -1:
    json_str = js_text[json_start:json_end]
    
    # It has a syntax error because of unescaped quotes.
    # The error is at "이거 그냥 컴퓨터가 대충 찍어낸 가짜 숫자 아냐?"
    # Let's just fix this specific error by replacing it with single quotes or escaped quotes.
    # But wait, json_str is invalid JSON, so we can't json.loads() it.
    
    # Manual fix:
    json_str = json_str.replace('"이거 그냥 컴퓨터가 대충 찍어낸 가짜 숫자 아냐?"', '\\"이거 그냥 컴퓨터가 대충 찍어낸 가짜 숫자 아냐?\\"')
    
    # Are there any other unescaped quotes inside "text": "..." values?
    # Let's try to parse it.
    try:
        data = json.loads(json_str)
        print("JSON is now valid!")
    except Exception as e:
        print(f"Still invalid: {e}")
        # Let's just replace all unescaped quotes inside the text.
        # A better way: just regenerate book_data.js from master_manuscript_v4_targeted.md!
        
    js_text = js_text[:json_start] + json_str + js_text[json_end:]
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_text)
