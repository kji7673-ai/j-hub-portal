import os

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_server.py', 'r', encoding='utf-8') as f:
    server_code = f.read()

new_api_code = """
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
        prompt = f"당신은 건축 및 경영 철학에 대해 비판적 시각을 제공하는 '레드팀(Red Team)' 컨설턴트입니다.\\n\\n[현재 페이지 원고]\\n{original_text}\\n\\n"
        prompt += "[대화 내역]\\n"
        for msg in chat_history:
            role_kr = "CEO" if msg['role'] == 'user' else "RedTeam"
            prompt += f"{role_kr}: {msg['content']}\\n"
        
        prompt += f"CEO: {new_message}\\nRedTeam:"
        
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
        prompt = f\"\"\"당신은 전문 에디터이자 작가입니다. 
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
\"\"\"
        for msg in chat_history:
            role_kr = "CEO" if msg['role'] == 'user' else "RedTeam"
            prompt += f"{role_kr}: {msg['content']}\\n"
            
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
                
                new_js_content = "const bookData = " + json.dumps(book_json, ensure_ascii=False, indent=4) + ";\\n"
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
"""

# Replace the old redteam_feedback and /api/save if possible, or just append
if '@app.route(\'/api/redteam_chat\')' not in server_code:
    # We will just insert new_api_code before if __name__ == '__main__':
    server_code = server_code.replace("if __name__ == '__main__':", new_api_code + "\nif __name__ == '__main__':")

# Update upload_image to handle image_layout
upload_mod_old = """
            # If text_only, promote to image_top. If cover, maybe leave it or make it image_full?
            if page_obj.get('type') == 'text_only':
                page_obj['type'] = 'image_top'
            elif page_obj.get('type') == 'cover':
                page_obj['type'] = 'image_full'
"""

upload_mod_new = """
            image_layout = data.get('image_layout', '')
            if image_layout:
                page_obj['type'] = image_layout
            else:
                if page_obj.get('type') == 'text_only':
                    page_obj['type'] = 'image_top'
                elif page_obj.get('type') == 'cover':
                    page_obj['type'] = 'image_full'
"""

server_code = server_code.replace(upload_mod_old, upload_mod_new)

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_server.py', 'w', encoding='utf-8') as f:
    f.write(server_code)
