import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Fix body height and position
html = re.sub(
    r'body\s*{[^}]*?height:\s*100vh;[^}]*?}',
    lambda m: m.group(0).replace('height: 100vh;', 'height: 100%; width: 100%; position: fixed; top: 0; left: 0; overscroll-behavior: none;'),
    html
)

html = re.sub(r'html\s*{', 'html { height: 100%; width: 100%; position: fixed; overflow: hidden; overscroll-behavior: none;', html)

# 2. Disable resize listener that triggers updateControls
html = re.sub(
    r'window\.addEventListener\(\'resize\', \(\) => \{.*?\}\);',
    '// Resize listener disabled to prevent mobile layout thrashing',
    html,
    flags=re.DOTALL
)

with open('index.html', 'w') as f:
    f.write(html)
