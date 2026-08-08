import re

js_path = "book_data.js"

with open(js_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix missing comma
# Find } followed by whitespace and {
fixed_text = re.sub(r'}\s+{', '},\n        {', text)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(fixed_text)
