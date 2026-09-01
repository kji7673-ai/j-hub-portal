import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix image_full text overlay wrapper
old_full = '<div style="padding: 50px 40px; display:flex; flex-direction:column; align-items:center; text-align:center; max-width: 80%; display:flex; flex-direction:column; align-items:center; text-align:center;">'
new_full = '<div style="padding: 40px; background: rgba(0, 0, 0, 0.45); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); display:flex; flex-direction:column; align-items:center; text-align:center; max-width: 85%; width: 100%; border: 1px solid rgba(255,255,255,0.1);">'
html = html.replace(old_full, new_full)

# Fix cover text overlay wrapper
old_cover = '<div class="cover-content" style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 10% 8%;">'
new_cover = '<div class="cover-content" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding: 40px; margin: auto; background: rgba(0, 0, 0, 0.45); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); max-width: 85%; width: 100%; border: 1px solid rgba(255,255,255,0.1); height: auto; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">'

# Wait! For `cover`, if there IS an image (the user said cover has white background), maybe I should add the image to the cover HTML since it's currently missing!
# Let's fix cover to actually show `page.image` as a full background if it exists!
cover_html_old = """                if (page.type === 'cover') {
                    pageEl.className += ' bg-dark';"""
                    
cover_html_new = """                if (page.type === 'cover') {
                    pageEl.style.padding = '0';
                    pageEl.style.position = 'relative';
                    if(page.image) {
                        contentHTML += `<div class="image-container" style="position:absolute; top:0; left:0; width:100%; height:100%; margin:0; z-index:0; background:#ffffff; display:flex; justify-content:center; align-items:center; padding: 0; box-sizing: border-box;"><img src="${page.image}" alt="cover_image" style="width:100%; height:100%; object-fit:cover;"></div>`;
                    } else {
                        pageEl.className += ' bg-dark';
                    }
                    contentHTML += `<div class="text-overlay" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; display:flex; flex-direction:column; justify-content:center; align-items:center; box-sizing: border-box;">`;
"""

html = html.replace(cover_html_old, cover_html_new)
html = html.replace(old_cover, new_cover)

# Since I added a `<div class="text-overlay"...>` wrapper for cover, I need to close it at the end of the cover block.
# The cover block ends with:
cover_end_old = """                    contentHTML += `<div style="width: 40px; height: 1px; background: rgba(255,255,255,0.2); margin-top: 40px;"></div>`;
                    contentHTML += `</div>`;
                }"""
cover_end_new = """                    contentHTML += `<div style="width: 40px; height: 1px; background: rgba(255,255,255,0.2); margin-top: 40px;"></div>`;
                    contentHTML += `</div></div>`;
                }"""
html = html.replace(cover_end_old, cover_end_new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Modifications applied successfully.")
