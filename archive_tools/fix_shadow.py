import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Revert image_full box
bad_full = '<div style="padding: 40px; background: rgba(0, 0, 0, 0.45); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); display:flex; flex-direction:column; align-items:center; text-align:center; max-width: 85%; width: 100%; border: 1px solid rgba(255,255,255,0.1);">'
good_full = '<div style="padding: 50px 40px; display:flex; flex-direction:column; align-items:center; text-align:center; max-width: 80%; display:flex; flex-direction:column; align-items:center; text-align:center;">'
html = html.replace(bad_full, good_full)

# 2. Revert cover box
bad_cover = '<div class="cover-content" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding: 40px; margin: auto; background: rgba(0, 0, 0, 0.45); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); max-width: 85%; width: 100%; border: 1px solid rgba(255,255,255,0.1); height: auto; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">'
good_cover = '<div class="cover-content" style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 10% 8%;">'
html = html.replace(bad_cover, good_cover)

bad_cover_start = """                if (page.type === 'cover') {
                    pageEl.style.padding = '0';
                    pageEl.style.position = 'relative';
                    if(page.image) {
                        contentHTML += `<div class="image-container" style="position:absolute; top:0; left:0; width:100%; height:100%; margin:0; z-index:0; background:#ffffff; display:flex; justify-content:center; align-items:center; padding: 0; box-sizing: border-box;"><img src="${page.image}" alt="cover_image" style="width:100%; height:100%; object-fit:cover;"></div>`;
                    } else {
                        pageEl.className += ' bg-dark';
                    }
                    contentHTML += `<div class="text-overlay" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; display:flex; flex-direction:column; justify-content:center; align-items:center; box-sizing: border-box;">`;
"""
good_cover_start = """                if (page.type === 'cover') {
                    pageEl.style.padding = '0';
                    pageEl.style.position = 'relative';
                    if(page.image) {
                        contentHTML += `<div class="image-container" style="position:absolute; top:0; left:0; width:100%; height:100%; margin:0; z-index:0; background:#ffffff; display:flex; justify-content:center; align-items:center; padding: 0; box-sizing: border-box;"><img src="${page.image}" alt="cover_image" style="width:100%; height:100%; object-fit:cover;"></div>`;
                    } else {
                        pageEl.className += ' bg-dark';
                    }
                    contentHTML += `<div class="text-overlay" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; display:flex; flex-direction:column; justify-content:center; align-items:center; box-sizing: border-box;">`;
"""
# Wait, I SHOULD keep the background image logic for cover, because without it, the user's cover image wouldn't display! The user said they wanted to see the drawing, so the background image logic is GOOD. I just need to remove the extra </div> that I added at the end of cover since I am reverting cover_content to not be absolute. Wait, I will keep text-overlay.

# Let's just fix text-shadow everywhere for overlaid text:
# h1 text-shadow
html = re.sub(r'text-shadow: 0 4px 12px rgba\(0,0,0,0\.5\);', r'text-shadow: 0 2px 8px rgba(0,0,0,0.8), 0 4px 20px rgba(0,0,0,0.6), 0 0 30px rgba(0,0,0,0.4);', html)
# subtitle text-shadow
html = re.sub(r'text-shadow: 0 2px 8px rgba\(0,0,0,0\.5\);', r'text-shadow: 0 2px 6px rgba(0,0,0,0.9), 0 4px 15px rgba(0,0,0,0.7);', html)
# body text text-shadow
html = re.sub(r'text-shadow: 0 1px 10px rgba\(255,255,255,0\.9\);', r'text-shadow: 0 2px 6px rgba(0,0,0,0.9), 0 4px 12px rgba(0,0,0,0.7); color:#ffffff;', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
