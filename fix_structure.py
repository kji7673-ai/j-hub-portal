import json

with open('docs/book_data.js', 'r') as f:
    c = f.read()

prefix = c[:c.find('[')]
suffix = c[c.rfind(']')+1:]
data = json.loads(c[c.find('['):c.rfind(']')+1])

# Indices to move: 137 to 192
# Indices to delete: 132 to 136

part1_body = data[137:193]
for item in part1_body:
    item['part'] = '1부: 시스템편 (진양 J-Hub 도입 사례)'

# Build the new array
new_data = data[:28] + part1_body + data[28:132] + data[193:]

# Verify lengths
# original: 196
# deleted: 5 (132 to 136)
# expected new length: 191
print(f"Old length: {len(data)}")
print(f"New length: {len(new_data)}")
if len(new_data) != len(data) - 5:
    print("Error: Length mismatch!")

new_json_str = json.dumps(new_data, ensure_ascii=False, indent=4)
with open('docs/book_data.js', 'w') as f:
    f.write(prefix + new_json_str + suffix)

print("Restructured successfully!")
