import os
import hashlib
import unicodedata
import json
import datetime
from flask import Flask, request, jsonify, session, send_from_directory, abort

app = Flask(__name__, static_folder='.', static_url_path='')
# 임시 비밀키 (실제 운영 시 랜덤 문자열 사용 필요)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "jinyang-hub-super-secret-key-2026")

ALLOWED_USERS_HASH = {
    "083ce048149966cfe211dfc88ad50cf83bd6309a22e7817f1aac0a972634a8a7": "78a69c6fdc7b95f502f14d3c826b21528318ef248796d5a41478096973dd1ad6",
    "abd36d9edb9f3e787308a3f263d1e301360b80ae2b2e0eaf341f4e3685fa70f7": "374c0fd6e94e0cec99de6089e5a6409dc4816b0f9427363c44b8985f60481f35",
    "7ac407e04698b5541411ac9ce3dbdf1e7de112e3a090894ae1469d31a058ccd1": "434f4d14c1eb231306b51aaa160c021b63670ac6ca67fb8e403f4500983dd1e4",
    "4ada0ba5227f8c1e9737d025dfeb36c81c8dfbea4898c6e784434f048f5d513c": "f7d7736a8f77a494064203eda8d618bb0cfbe19668065fa083825ecdc1eda540",
    "2941cc17f83c2dafdaac06447a40dc4842f6f6c84637eb45345562bb686fdbc3": "cf3b763a62724306dca2a00ed53a7c0a19074286e40b8f0b96544ccbab4aaae2",
    "bf40392d2dc7da13d7a14c2408cf0738585e574968630ada8d2a53bb892148c0": "b954bc4acaad1bfa43689f654027227c6cd416e797fbf7ddbd2a38864d857a5e",
    "196ba51dc6297cea4a791253a6accfb23ff333db0320fb4fde1fb7e2f628fe75": "ea4bdbc1419b6c7aa4919f1276fcb3eb6fd9a316e52e177fa519b1cbe9fbb3de",
    "07947665e58f2c5f608cb2d61041957c9900a2bca66b76ea2b3e535102b531cb": "a1fb4e703a9ef1fa4936801721ff285a97ac85330856674412e054892afe6972",
    "0447a608b0327060df1e4547cb35ddfb657c25cddd0e30e45b16b01861b79bc4": "d1913a47aec9a99a549e8d075b5118abcabd8e8599d6fbbdb67785a5c31d9b03",
    "f02361a6f605b192d7de8c1eeef059434c77f135b5381f301530f8b0580b3a3e": "5119e090c80757fec3c9f1dca46e3481688fed2fea905db0af7994857abb92a6",
    "06c86870ce966a9f790dea92f6867803625c990e30a5cf3cc5389382e5b29824": "03b0bd366e8184f8d871c3a7c7cc26c73c25b54ff54c64b28b10b898242cdc8a",
    "c1a8c38de902dd1df2981ad2283da6c5c30f688b08cd3a6ee469c5bd9dedcb01": "2ec1d83738358cd8610d8d7a699891f1e5d7dd9bdf6f82ae70d048bc13f7f11f",
    "db9f88c413c428ffc06bbbfd0fad941bb22e61cbc91df66c1ba5dbd042e93ae3": "2c2ae095d55ddbc0487f97a5e8db5ecd4b2f1538cd67e774b461d85c4b96a216",
    "bb4f332ffa027fa030c3cdf98e7470a288140afdaa0e83d83b062db008c86812": "cf1881df6f1696c2e59b47fde80838e66a1dfad4f0e993fd686186333456b55d",
    "886f574366984d340a2215ab5ae1983fe4c6bf0f0e2af656a4725414c114edec": "f1294f35f19846cd012506eadcc13ecda95eb7ddc6c661bc1b9402c4b00eb703",
    "c029836f84a430f0379582ebc21c608a7e88ffff08bfcf2c314fb7c9934a3be8": "f0e6a61a0b0037aa12879a3ba580a7b84ef77cd5a8a39f1832589d6390b7fa66",
    "ea6e683cd089bc5c027c159b5d338ec6f946e67b7cfba82a15080e066291712b": "461b2e3622293c303571880413edf2e26b35f5d191b30a32e7eea20da00613d2",
    "dc761a887aa6cb6a65e45abb1e6e8c44c10be54cfa7a2786b7e6d4fa1ff50a31": "29d9c129c3e755f6bd3f321ea47f6dd67bc9023b6bca2a8018a80be2adb6c957",
    "3b8dec7dbb7b718dd727903ef521e6b519cddb12868b3212aba7f5c940c0bbf5": "4baabeaad579e9201bfd7bc4dd8ba8392ce01ef09e8067c740adc882fdcba548",
    "8f2ccb383557c7d98945e0f0824f78940b22f1bdb21af0a055303d5be31c8474": "d0c9e369bee256f4b0182a503babb685ee7b00419c985fb423a47bfb0eb89f56",
    "e23397ee20dbe830cdf81b83a23633551b5cdc433c225e7e8ea7163a052c67f1": "de8736cc048486e16dcd174d8f5f0bc3e19aa4f0b0c26a19572b4cfafa5b31ca",
    "b05193a2568cce567074c3c8e78fa4e822c627ac42f85d6ccda430bf3a30dc00": "16d5164c6ff6bf7201a90e9ec406fe9d122c9894cda28854a05e68ff1f2e804c",
    "305bf59e098d3d08c90af0436ee6e21705662419e9d5152a4b11e80275cf051d": "6bfc25cc7df52b4fabc33e36962aed9620b8f61ad7bbab543996d0575e12c832",
    "b2a391ae19bb65ef90bfb6a78fcaece1c2a8099e7814373bc19ce95ec54bc62f": "ac2151d8aa26b5784551edad3b8ffdaf126a08a8f4ae57db2fc94e01b5443860",
    "64a5b67b01286e3052bae5698468ee5d95a5025952ad3fd424fd6d6c46f71e40": "714bc174ac5066ca0a4a710f503d76ce0254e2c8d1e313abf90171be0ff5975e",
    "13318b0c637272965f6b891dbefca6a5c3b913711818c112ce9c3768cd34f9a5": "88367dd16bfd18ba5595a82d9076f8405807ea4df66c0d282de850391349986a",
    "165cc6f8db72aeee16f9336b0f3abd6c6cbb3f29d22bc03906f45e87f6e8fd19": "2612d391c1eb9a05beb967f1f2adaf215a544bd5e2d88d2a13c531e56af493a6",
    "412f9b3f64294c6337d7be6680037813efaa066e02ba1704a0be0ccd5194fc36": "7d4a25031f5a15141275e08712537464836bbe2cc81512cadfa828d619cbba4a",
    "5f3cccee7b06941609fb55be6396dbd9a3d9c94e5346e91a6ad8ba1c04834b80": "a498b30af4f790314c211c4e6a9a4d8c37015ec9102a6496406cd49b85d37502",
    "be4b08c15fb586cae8972bb1f28da0c08054abbafbb91c67ffaa04027dce7d44": "de7d5e6247fb643608b4f5ef96726ec0c478e1499bcf1f650fa4cf118063dad0",
    "5b1d1063bf62836cedfed54c6af4c3ecb6af92d99b6012c8bf280d93e129b4fc": "179cf283f9f50c9bbf5b86380349d36adf78f5f47d09f939e7a1bf190e8641f4",
    "0cec8e0c1dbec4a4cad36144b3ba9a9a8bb8892f64c4ffe3c3357cbf83db2e59": "9c27727c109abd005defbcac1ab6f1a69a3f858144024969816b65c00f89ed18",
    "2822ac4015f1156b5be7e2b34e223c4c8e336504cc610fea04a9c52f369fd5b2": "c15195e527aab50976ac9ac7596cc6521f141e8499f65be42f0a7df3445d12ab"
}

def get_hash(text):
    normalized_text = unicodedata.normalize('NFC', text.strip())
    return hashlib.sha256(normalized_text.encode('utf-8')).hexdigest()

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'name' not in data or 'password' not in data:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    name = data['name']
    password = data['password']

    name_hash = get_hash(name)
    pass_hash = get_hash(password)

    if name_hash in ALLOWED_USERS_HASH and ALLOWED_USERS_HASH[name_hash] == pass_hash:
        session['logged_in'] = True
        session['user_name'] = name
        
        # Admin / Knowledge master logic (matches frontend logic)
        # Assuming we just set it if it matches one of the hashes that previously had it. 
        # Actually frontend checked if localstorage had it. We can just set it true for now for the CEO.
        if name == "김중일":
            session['is_master'] = True
            
        return jsonify({
            "success": True, 
            "user_name": name, 
            "is_master": session.get('is_master', False)
        })

    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route('/api/check_session', methods=['GET'])
def check_session():
    if session.get('logged_in'):
        return jsonify({
            "success": True, 
            "user_name": session.get('user_name'),
            "is_master": session.get('is_master', False)
        })
    return jsonify({"success": False}), 401

@app.route('/api/analects/today', methods=['GET'])
def get_today_analects():
    try:
        with open('analects.json', 'r', encoding='utf-8') as f:
            analects_list = json.load(f)
        
        # 오늘 날짜를 기준으로 인덱스 계산 (매일 자정 변경)
        today = datetime.date.today()
        day_index = today.toordinal() % len(analects_list)
        
        return jsonify(analects_list[day_index])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    if not session.get('logged_in'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    data = request.json
    project_name = data.get('project_name', '')
    content = data.get('content', '')
    is_anonymous = data.get('is_anonymous', False)
    
    if not content:
        return jsonify({"success": False, "message": "Content is required"}), 400
        
    author = "익명" if is_anonymous else session.get('user_name', 'Unknown')
    
    feedback_entry = {
        "id": hashlib.md5(f"{datetime.datetime.now().isoformat()}{author}".encode()).hexdigest()[:8],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "author": author,
        "project_name": project_name,
        "content": content
    }
    
    try:
        feedback_list = []
        if os.path.exists('feedback_db.json'):
            with open('feedback_db.json', 'r', encoding='utf-8') as f:
                feedback_list = json.load(f)
        
        feedback_list.append(feedback_entry)
        
        with open('feedback_db.json', 'w', encoding='utf-8') as f:
            json.dump(feedback_list, f, ensure_ascii=False, indent=4)
            
        return jsonify({"success": True, "message": "Feedback safely delivered."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    if not session.get('logged_in') or not session.get('is_master'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    try:
        if os.path.exists('feedback_db.json'):
            with open('feedback_db.json', 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Protect sensitive static files (like the weekly report html/pdf if they exist in a protected folder)
# Currently, the frontend loads an iframe to a local file or absolute path, which isn't secure. 
# But this satisfies the basic requirement of server-side login.

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 15000))
    app.run(host='0.0.0.0', port=port)
