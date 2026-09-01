from PIL import Image, ImageDraw

def draw_j_icon(size, filename):
    # Dark apple-like background
    img = Image.new('RGB', (size, size), color='#1d1d1f')
    draw = ImageDraw.Draw(img)
    
    # Calculate dimensions
    margin = size * 0.2
    w = size - margin * 2
    h = size - margin * 2
    
    # Draw 'J' geometrically
    # Top horizontal line
    thickness = size * 0.15
    draw.rectangle(
        [margin + w*0.4, margin, size - margin, margin + thickness],
        fill='#ffffff'
    )
    
    # Vertical line
    draw.rectangle(
        [size/2, margin, size/2 + thickness, size - margin - size*0.1],
        fill='#ffffff'
    )
    
    # Bottom curve (approximated with rectangles/polygons for simplicity)
    draw.rectangle(
        [margin + w*0.2, size - margin - thickness, size/2 + thickness, size - margin],
        fill='#ffffff'
    )
    
    draw.rectangle(
        [margin + w*0.2, size - margin - size*0.25, margin + w*0.2 + thickness, size - margin],
        fill='#ffffff'
    )
    
    img.save(filename)

draw_j_icon(192, 'docs_apple/icon-192.png')
draw_j_icon(512, 'docs_apple/icon-512.png')
print("Icons created!")
