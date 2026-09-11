import os
import re

studio_path = "book_studio.html"
reader_path = "reader_index.html"

if not os.path.exists(studio_path):
    print("Error: book_studio.html not found.")
    sys.exit(1)

with open(studio_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the redteam-panel div
html = re.sub(r'<div class="redteam-panel.*?</script>', '', html, flags=re.DOTALL)

# Also remove the script block that contains handleEdit(), handleRedTeamToggle()
# We will just replace it by replacing the entire script block with a simplified one, or we can just remove the buttons from HTML.

# Remove edit buttons
html = re.sub(r'<button class="icon-btn edit-btn".*?</button>', '', html)
html = re.sub(r'<button class="icon-btn image-upload-btn".*?</button>', '', html)
html = re.sub(r'<input type="file" id="image-upload-input".*?>', '', html)

# Remove the Red Team toggle button
html = re.sub(r'<button class="icon-btn rt-btn".*?</button>', '', html)

# Change title
html = html.replace("<title>J-Journal Book Studio</title>", "<title>건축, AI를 만나다 - Beta v1.0</title>")

# Simplify JS: we just need renderPages and basic navigation.
# Let's remove the handleEdit and API calls.
# It's safer to just let the script be, since it will just fail to call APIs if buttons are gone.
# But wait, there are no buttons, so the functions won't be called.
# The only issue is that the Red Team Panel is gone, so if the script tries to querySelector('.redteam-panel'), it might throw an error.
# Let's wrap the script in a try-catch or remove the redteam logic.

script_to_remove = """
        // Red Team Toggle
        const rtBtn = document.querySelector('.rt-btn');
        const rtPanel = document.querySelector('.redteam-panel');
        if (rtBtn && rtPanel) {
            rtBtn.addEventListener('click', () => {
                rtPanel.classList.toggle('active');
            });
        }
"""
html = html.replace(script_to_remove, "")

with open(reader_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Created reader_index.html successfully.")
