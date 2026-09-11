import os
import json
import base64
import time
import re
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/edu/')
@app.route('/edu/<path:filename>')
def serve_edu(filename="index.html"):
    import os
    from flask import send_from_directory
    if not os.path.exists(os.path.join('docs_apple', filename)):
        return "File not found in docs_apple", 404
    return send_from_directory('docs_apple', filename)


# Configure Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-flash-latest")
else:
    model = None
    print("WARNING: GEMINI_API_KEY not found in environment. AI feedback will be mocked.")

BOOK_DATA_PATH = "book_data.js"

@app.route('/')
def index():
    return send_from_directory('.', 'book_studio.html')

@app.route('/api/redteam', methods=['POST'])
def redteam_feedback():
    data = request.json
    original_text = data.get('original_text', '')
    ceo_opinion = data.get('ceo_opinion', '')
    
    if not ceo_opinion:
        return jsonify({"feedback": "추가 또는 수정할 의견을 입력해주세요."})
        
    if model:
        prompt = f"""
당신은 건축 및 경영 철학에 대해 비판적 시각을 제공하는 '레드팀(Red Team)' 컨설턴트입니다.
작성자(CEO)가 원고를 다듬기 위해 아래와 같은 새로운 의견/수정안을 제시했습니다.

[기존 텍스트 맥락]
{original_text}

[CEO의 추가/수정 의견]
{ceo_opinion}

이 의견이 기존 맥락과 충돌하지 않는지, 논리적 비약이나 꼰대 같은 톤(권위적인 어조)이 없는지, 철학적 깊이를 해치지 않는지 객관적이고 날카롭게 비판해 주십시오. 그리고 더 나은 방향성을 제시해 주십시오.
응답은 명확하고 정중하게 하되, 단점과 개선점을 분명히 짚어주세요.
"""
        try:
            response = model.generate_content(prompt)
            feedback = response.text
        except Exception as e:
            feedback = f"AI API 호출 오류가 발생했습니다: {str(e)}"
    else:
        feedback = "[Mock Feedback] API 키가 없습니다. 의견을 검토한 결과, 전반적으로 맥락에 부합하나 조금 더 부드러운 톤으로 수정하는 것을 권장합니다."
        
    return jsonify({"feedback": feedback})

@app.route('/api/save', methods=['POST'])
def save_revision():
    data = request.json
    page_index = data.get('page_index')
    revised_text = data.get('revised_text')
    
    if page_index is None or revised_text is None:
        return jsonify({"status": "error", "message": "Invalid data"}), 400
        
    if not os.path.exists(BOOK_DATA_PATH):
        return jsonify({"status": "error", "message": "book_data.js not found"}), 404
        
    with open(BOOK_DATA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
        
    json_start = content.find('{')
    json_end = content.rfind('}') + 1
    
    if json_start == -1 or json_end == -1:
        return jsonify({"status": "error", "message": "Cannot parse book_data.js"}), 500
        
    try:
        book_json = json.loads(content[json_start:json_end])
        
        if 0 <= page_index < len(book_json.get('pages', [])):
            if 'text' in book_json['pages'][page_index]:
                book_json['pages'][page_index]['text'] = revised_text
            else:
                book_json['pages'][page_index]['text'] = revised_text
                
            new_js_content = "const bookData = " + json.dumps(book_json, ensure_ascii=False, indent=4) + ";\n"
            with open(BOOK_DATA_PATH, 'w', encoding='utf-8') as f:
                f.write(new_js_content)
                
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Page index out of bounds"}), 400
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


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
            
            image_layout = data.get('image_layout', '')
            if image_layout:
                page_obj['type'] = image_layout
            else:
                if page_obj.get('type') == 'text_only':
                    page_obj['type'] = 'image_top'
                elif page_obj.get('type') == 'cover':
                    page_obj['type'] = 'image_full'
                
            new_js_content = "const bookData = " + json.dumps(book_json, ensure_ascii=False, indent=4) + ";\n"
            with open(BOOK_DATA_PATH, 'w', encoding='utf-8') as f:
                f.write(new_js_content)
                
            return jsonify({"status": "success", "image_url": image_url})
        else:
            return jsonify({"status": "error", "message": "Page index out of bounds"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/redteam_chat', methods=['POST'])
def redteam_chat():
    data = request.json
    original_text = data.get('original_text', '')
    chat_history = data.get('chat_history', []) # list of dicts: {'role': 'user'|'model', 'content': '...'}
    new_message = data.get('message', '')
    
    if not new_message:
        return jsonify({"feedback": "메시지를 입력해주세요."})
        
    if model:
        # Build prompt from history
        prompt = f"당신은 건축 및 경영 철학에 대해 비판적 시각을 제공하는 '레드팀(Red Team)' 컨설턴트입니다.\n\n[현재 페이지 원고]\n{original_text}\n\n"
        prompt += "[대화 내역]\n"
        for msg in chat_history:
            role_kr = "CEO" if msg['role'] == 'user' else "RedTeam"
            prompt += f"{role_kr}: {msg['content']}\n"
        
        prompt += f"CEO: {new_message}\nRedTeam:"
        
        try:
            response = model.generate_content(prompt)
            return jsonify({"feedback": response.text})
        except Exception as e:
            return jsonify({"feedback": f"API 오류: {str(e)}"})
    else:
        return jsonify({"feedback": "[로컬 테스트 모드] 입력하신 메시지에 대한 가상의 비판적 피드백입니다. 실제 API 키를 설정해주세요."})

@app.route('/api/apply_revision', methods=['POST'])
def apply_revision():
    data = request.json
    page_index = data.get('page_index')
    original_text = data.get('original_text', '')
    chat_history = data.get('chat_history', [])
    prev_text = data.get('prev_text', '')
    next_text = data.get('next_text', '')
    
    if page_index is None:
        return jsonify({"status": "error", "message": "Invalid page index"}), 400
        
    if model:
        prompt = f"""당신은 전문 에디터이자 작가입니다. 
아래의 [현재 원고]를 [대화 내역(피드백 및 수정 요청)]을 적극 반영하여 완전히 새롭게 다시 작성(Rewrite)해 주십시오.
단락과 문맥이 매우 매끄러워야 하며, [이전 페이지 원고]와 [다음 페이지 원고]를 참고하여 자연스럽게 이어지도록 써주세요.
반드시 마크다운이나 부연 설명 없이 '새롭게 작성된 본문 텍스트'만 출력해야 합니다.

[이전 페이지 원고 (참고용)]
{prev_text}

[다음 페이지 원고 (참고용)]
{next_text}

[현재 원고 (수정 대상)]
{original_text}

[대화 내역 (반영해야 할 요구사항)]
"""
        for msg in chat_history:
            role_kr = "CEO" if msg['role'] == 'user' else "RedTeam"
            prompt += f"{role_kr}: {msg['content']}\n"
            
        try:
            response = model.generate_content(prompt)
            revised_text = response.text.strip()
            
            # Save to book_data.js
            if not os.path.exists(BOOK_DATA_PATH):
                return jsonify({"status": "error", "message": "book_data.js not found"}), 404
                
            with open(BOOK_DATA_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
                
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            book_json = json.loads(content[json_start:json_end])
            
            if 0 <= page_index < len(book_json.get('pages', [])):
                page_obj = book_json['pages'][page_index]
                page_obj['text'] = revised_text
                
                new_js_content = "const bookData = " + json.dumps(book_json, ensure_ascii=False, indent=4) + ";\n"
                with open(BOOK_DATA_PATH, 'w', encoding='utf-8') as f:
                    f.write(new_js_content)
                    
                return jsonify({"status": "success", "revised_text": revised_text})
            else:
                return jsonify({"status": "error", "message": "Page index out of bounds"}), 400

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        # Mock save
        return jsonify({"status": "error", "message": "API key not found, cannot rewrite text."}), 500

if __name__ == '__main__':
    print("Starting Secret Room Server on http://0.0.0.0:5051")
    app.run(host='0.0.0.0', port=5051, debug=True)
