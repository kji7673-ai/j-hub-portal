import os

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_studio.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update renderBook() to support image_full
image_full_logic = """
                else if (page.type === 'image_full') {
                    if(page.image) {
                        contentHTML += `<div class="image-container" style="margin-bottom:0; height:100%; border-radius:0;"><img src="${page.image}" alt="full_image" style="object-fit:contain;"></div>`;
                    }
                }
"""

if "page.type === 'image_full'" not in html:
    html = html.replace(
        "else if (page.type === 'text_only')",
        image_full_logic.strip() + "\n                else if (page.type === 'text_only')"
    )

# 2. Update image-upload listener
old_upload_logic = """
        // Image upload handling for the current active page
        document.getElementById('image-upload').addEventListener('change', function(e) {
            if(e.target.files && e.target.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const activePage = bookData.pages[currentPage];
                    activePage.image = e.target.result;
                    if(activePage.type === 'text_only') activePage.type = 'image_top';
                    renderBook();
                }
                reader.readAsDataURL(e.target.files[0]);
            }
        });
"""

new_upload_logic = """
        // Image upload handling for the current active page (Persists to backend)
        document.getElementById('image-upload').addEventListener('change', async function(e) {
            if(e.target.files && e.target.files[0]) {
                const file = e.target.files[0];
                const reader = new FileReader();
                
                // Show loading indicator
                const uploadLabel = document.querySelector('label[for="image-upload"]');
                const originalLabel = uploadLabel.innerText;
                uploadLabel.innerText = "업로드 중...";
                
                reader.onload = async function(e) {
                    const base64Data = e.target.result;
                    
                    try {
                        const response = await fetch('/api/upload_image', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                page_index: currentPage,
                                image_data: base64Data
                            })
                        });
                        
                        const result = await response.json();
                        
                        if (result.status === 'success') {
                            const activePage = bookData.pages[currentPage];
                            activePage.image = result.image_url;
                            if(activePage.type === 'text_only') activePage.type = 'image_top';
                            else if(activePage.type === 'cover') activePage.type = 'image_full';
                            
                            // Re-render and restore label
                            renderBook();
                            uploadLabel.innerText = originalLabel;
                            // alert("이미지가 서버에 영구적으로 저장되었습니다.");
                        } else {
                            alert("업로드 실패: " + result.message);
                            uploadLabel.innerText = originalLabel;
                        }
                    } catch (error) {
                        alert("서버 통신 오류: " + error.message);
                        uploadLabel.innerText = originalLabel;
                    }
                }
                reader.readAsDataURL(file);
            }
        });
"""

if 'fetch(\'/api/upload_image\'' not in html:
    html = html.replace(old_upload_logic.strip(), new_upload_logic.strip())

with open('/Users/joongilkim/Desktop/03_업무자료/J_Journal_프로젝트/웹_매뉴얼_플랫폼/book_studio.html', 'w', encoding='utf-8') as f:
    f.write(html)
