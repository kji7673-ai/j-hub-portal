import re

with open("generate_apple_static.py", "r", encoding="utf-8") as f:
    text = f.read()

# We need to split the text by f"""..."""
# and only replace {{ and }} in the OUTSIDE parts (and also inside normal """...""")
parts = re.split(r'(f\"\"\"[\s\S]*?\"\"\")', text)

for i in range(len(parts)):
    if parts[i].startswith('f"""'):
        pass # do not touch f-strings
    else:
        parts[i] = parts[i].replace('{{', '{').replace('}}', '}')

with open("generate_apple_static.py", "w", encoding="utf-8") as f:
    f.write("".join(parts))

print("Fixed braces!")
