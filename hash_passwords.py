import hashlib
import json
import re

with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract allowedUsers block
match = re.search(r'const allowedUsers = (\{.*?\});', html, re.DOTALL)
if match:
    # This is a bit tricky to parse safely, but let's use a regex to extract "Name": "Pass" pairs
    block = match.group(1)
    pairs = re.findall(r'"([^"]+)":\s*"([^"]+)"', block)
    
    hashed_users = {}
    for name, pwd in pairs:
        # We will use SHA-256 for the password
        hash_obj = hashlib.sha256(pwd.encode('utf-8'))
        hashed_pwd = hash_obj.hexdigest()
        hashed_users[name] = hashed_pwd
        
    js_output = "const allowedUsersHash = " + json.dumps(hashed_users, ensure_ascii=False, indent=4) + ";\n"
    
    with open('/Users/joongilkim/Desktop/03_업무자료/법규관련/j-hub-portal/src/components/auth_data.js', 'w', encoding='utf-8') as f:
        f.write(js_output)
    print("Successfully extracted and hashed passwords to src/components/auth_data.js")
else:
    print("Could not find allowedUsers block.")
