import re
import os

files = ['dashboard.html', 'laws.html', 'projects.html', 'calendar.html', 'reading.html']

for f_name in files:
    path = os.path.join('src/pages', f_name)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove the outermost div like <div id="tab-reading" class="tab-content"> and its closing </div>
    # Using regex to find the first <div id="tab-...> and remove it.
    # The simplest way is to replace `<div id="tab-[^"]+" class="tab-content">` with '' and the last `</div>` with ''
    
    html = re.sub(r'<div id="tab-[^"]+" class="tab-content">', '', html, count=1)
    
    # Remove the last </div>
    if '</div>' in html:
        # rsplit to replace from right
        html = html.rsplit('</div>', 1)[0] + html.rsplit('</div>', 1)[1]
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html.strip() + "\n")

print("Cleaned module wrappers.")
