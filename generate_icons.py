from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename):
    img = Image.new('RGB', (size, size), color='#0066cc')
    d = ImageDraw.Draw(img)
    
    # Try to load a generic sans-serif font if possible, else default
    # We will just draw a text 'J' in the center
    # Because default font is small, we can scale it, but let's just draw a simple geometry for 'J' instead to make it look good at 512px
    
    # Or just use ImageFont.load_default() and resize the image, or manually draw polygons.
    # It's easier to just draw lines for a 'J'
    w = size
    h = size
    thickness = int(size * 0.15)
    
    # Vertical line of J
    d.rectangle([w*0.55, h*0.2, w*0.55 + thickness, h*0.75], fill='white')
    
    # Bottom curve of J (approximated with a rectangle)
    d.rectangle([w*0.35, h*0.75 - thickness, w*0.55 + thickness, h*0.75], fill='white')
    d.rectangle([w*0.35, h*0.6, w*0.35 + thickness, h*0.75], fill='white')
    
    img.save(filename)

create_icon(192, 'icon-192.png')
create_icon(512, 'icon-512.png')
print("Icons generated.")
