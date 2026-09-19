import json

def normalize_book():
    with open('book_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    pages = data.get('pages', [])
    current_title = None

    for i, p in enumerate(pages):
        ptype = p.get('type')
        title = p.get('title', '')
        
        # 1. Type Consistency Enforcement
        if ptype == 'text_only':
            p['image'] = None
            p['isImageOnly'] = False
        elif ptype == 'image_top':
            if not p.get('text') or str(p.get('text')).strip() == "":
                p['isImageOnly'] = True
            else:
                p['isImageOnly'] = False
                
        # Handle explicitly missing keys
        if 'isImageOnly' not in p:
            p['isImageOnly'] = False

        # 2. Hierarchy and isContinuation Logic
        if ptype in ['cover', 'author_profile']:
            p['isContinuation'] = False
            current_title = title # Reset hierarchy at structural dividers
            continue

        if title:
            if title != current_title:
                # It's a definitively new chapter
                p['isContinuation'] = False
                current_title = title
            else:
                # Same title as before, must be a continuation
                p['isContinuation'] = True
        else:
            # Title is empty. This is standard for subsequent gallery pages.
            # It inherently continues the current_title's block.
            p['isContinuation'] = True

    # Save normalized data
    with open('book_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Book structure normalized successfully.")

if __name__ == '__main__':
    normalize_book()
