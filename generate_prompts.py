import json

style = "Line-art style illustration, minimalist, thin straight and curved lines, with important focal parts depicted in thick black lines. Black and white architectural sketching style."

with open('missing_images.json', 'r') as f:
    items = json.load(f)

prompts = []
for item in items:
    title = item['title']
    text = item['text']
    prompt = f"Title: {title}. Context: {text}. {style} Create a conceptual illustration representing the core theme of the text."
    
    # Specific adjustment for the watermelon
    if "수박" in title:
        prompt = f"{style} A conceptual drawing of a smashed watermelon where its seeds are perfectly arranged to form a pyramid structure, representing rigid hierarchy hidden inside an organic shape."
        
    img_name = f"essay_{item['index']:03d}_{title[:5].replace('.', '').replace(' ', '_')}"
    prompts.append({
        'index': item['index'],
        'title': title,
        'image_name': img_name,
        'prompt': prompt
    })

with open('prompts.json', 'w') as f:
    json.dump(prompts, f, ensure_ascii=False, indent=2)
print("Generated prompts for 51 images.")
