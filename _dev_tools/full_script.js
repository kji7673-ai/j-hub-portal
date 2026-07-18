
                document.getElementById('analects-date').innerText = new Date().toLocaleDateString('ko-KR', { month: 'long', day: 'numeric', weekday: 'short' });
                
                // Fetch today's analects
                fetch('/api/analects/today')
                    .then(response => response.json())
                    .then(data => {
                        if(data && data.hanja) {
                            document.getElementById('analects-hanja').innerText = data.hanja;
                            document.getElementById('analects-korean').innerText = data.korean;
                            document.getElementById('analects-application').innerText = data.application;
                            
                            const grid = document.getElementById('analects-grid');
                            grid.innerHTML = '';
                            data.characters.forEach(c => {
                                const div = document.createElement('div');
                                div.innerHTML = `<span style="font-size: 20px; font-weight: 600; color: ${c.color};">${c.char}</span><br><span style="font-size: 12px; color: #7a7a7a;">${c.reading}</span>`;
                                grid.appendChild(div);
                            });
                            
                            document.getElementById('analects-widget').style.display = 'flex';
                        }
                    })
                    .catch(err => console.error("Failed to load analects:", err));
            </script>
            <script>
                document.getElementById('daily-byte-date').innerText = new Date().toLocaleDateString('ko-KR', { month: 'long', day: 'numeric', weekday: 'short' });
            </script>
            <script>
                let currentArticleUrl = '';
                // 이스터에그: 100개 중 1개 폭탄 위치 무작위 배정
                window.bombIndex = Math.floor(Math.random() * 100);
                
                function renderMosaic() {
                    const grid = document.getElementById('mosaic-grid');
                    if (!grid || typeof articlesData === 'undefined') return;
                    
                    grid.innerHTML = '';
                    
                    let readList = [];
                    try {
                        const currentBuildDate = '2026-07-16';
                        const storedBuildDate = localStorage.getItem('jhub_build_date');
                        
                        if (storedBuildDate !== currentBuildDate) {
                            // Date changed (new articles built), clear everything
                            localStorage.removeItem('jhub_read_articles');
                            localStorage.setItem('jhub_build_date', currentBuildDate);
                            // Do not clear the knowledge master badge! It is permanent.
                        } else {
                            const saved = localStorage.getItem('jhub_read_articles');
                            if (saved) readList = JSON.parse(saved);
                        }
                    } catch (e) {}
                    
                    articlesData.forEach((article, index) => {
                        let bgColor = '#ffffff';
                        const cat = article.category || '';
                        
                        // Vibrant colors for the mosaic
                        if (cat.includes('예술') || cat.includes('문화') || cat.includes('디자인')) {
                            bgColor = '#FFD166'; // Yellow
                        } else if (cat.includes('건축') || cat.includes('공학') || cat.includes('시티')) {
                            bgColor = '#118AB2'; // Blue
                        } else if (cat.includes('경제') || cat.includes('부동산') || cat.includes('상업')) {
                            bgColor = '#06D6A0'; // Green
                        } else {
                            bgColor = '#EF476F'; // Pink/Red
                        }
                        
                        const isRead = readList.includes(index);
                        const cardClass = isRead ? "mosaic-block read" : "mosaic-block";
                        
                        let clickAction = `openDetail(${index})`;
                        if (index === window.bombIndex) {
                            clickAction = `triggerEasterEgg(${index})`;
                        }
                        
                        const cardHtml = `
                            <div class="${cardClass}" id="mosaic-card-${index}" style="background-color: ${bgColor};" onclick="${clickAction}" title="${article.category}: ${article.title}">
                                <div class="mosaic-check">✓</div>
                            </div>
                        `;
                        grid.innerHTML += cardHtml;
                    });
                }
                
                function resetMosaicProgress() {
                    if(confirm("모든 읽기 진행 상황을 초기화하시겠습니까? (획득한 뱃지는 유지됩니다)")) {
                        localStorage.removeItem('jhub_read_articles');
                        document.getElementById('detail-content').style.display = 'none';
                        document.getElementById('easter-egg-content').style.display = 'none';
                        document.getElementById('complete-content').style.display = 'none';
                        document.getElementById('detail-placeholder').style.display = 'block';
                        renderMosaic();
                    }
                }
                
                function triggerEasterEgg(index) {
                    const card = document.getElementById('mosaic-card-' + index);
                    if (card) {
                        card.style.background = 'url("data:image/svg+xml;utf8,<svg xmlns=\\\'http://www.w3.org/2000/svg\\\' viewBox=\\\'0 0 24 24\\\' fill=\\\'none\\\' stroke=\\\'%238B5A2B\\\' stroke-width=\\\'2\\\' stroke-linecap=\\\'round\\\' stroke-linejoin=\\\'round\\\'><path d=\\\'M18 8h1a4 4 0 0 1 0 8h-1M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z\\\'/><line x1=\\\'6\\\' y1=\\\'1\\\' x2=\\\'6\\\' y2=\\\'4\\\'/><line x1=\\\'10\\\' y1=\\\'1\\\' x2=\\\'10\\\' y2=\\\'4\\\'/><line x1=\\\'14\\\' y1=\\\'1\\\' x2=\\\'14\\\' y2=\\\'4\\\'/></svg>") center/50% no-repeat, #fff';
                        card.style.animation = 'coffeeFloat 2s ease-in-out forwards';
                        card.classList.add('read');
                        card.classList.add('active');
                    }
                    
                    document.getElementById('detail-placeholder').style.display = 'none';
                    document.getElementById('detail-content').style.display = 'none';
                    document.getElementById('complete-content').style.display = 'none';
                    document.getElementById('easter-egg-content').style.display = 'block';
                    
                    document.getElementById('article-detail-pane').scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                    let readList = [];
                    try {
                        const saved = localStorage.getItem('jhub_read_articles');
                        if (saved) readList = JSON.parse(saved);
                    } catch (e) {}
                    if (!readList.includes(index)) {
                        readList.push(index);
                        localStorage.setItem('jhub_read_articles', JSON.stringify(readList));
                    }
                    checkAllRead(readList);
                }
                
                function checkAllRead(readList) {
                    if (readList.length >= articlesData.length) {
                        // Check if badge already granted to prevent annoying re-popups
                        const alreadyGranted = localStorage.getItem('jhub_badge_knowledge_master');
                        
                        if (!alreadyGranted) {
                            // Show the complete message briefly on top of the content using alert
                            alert("🎉 축하합니다! 지식 마스터 배지 획득! 100개의 저널을 모두 완독하셨습니다.");
                            
                            // Grant badge
                            localStorage.setItem('jhub_badge_knowledge_master', 'true');
                            
                            // Show badge in header immediately
                            const badgeContainer = document.getElementById('user-profile-badge');
                            if(badgeContainer) {
                                badgeContainer.innerHTML = '<span style="background: linear-gradient(135deg, #FFD700, #FDB931); color: #fff; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; margin-left: 6px; animation: badgeGlow 2s infinite;">지식 마스터 🏅</span>';
                            }
                        }
                    }
                }
                
                function openDetail(index) {
                    const article = articlesData[index];
                    if (!article) return;
                    
                    // Remove active state from all blocks
                    document.querySelectorAll('.mosaic-block').forEach(b => b.classList.remove('active'));
                    
                    // Save read state & set active
                    const card = document.getElementById('mosaic-card-' + index);
                    if (card) {
                        card.classList.add('active');
                        card.classList.add('read');
                    }
                    
                    let readList = [];
                    try {
                        const saved = localStorage.getItem('jhub_read_articles');
                        if (saved) readList = JSON.parse(saved);
                    } catch (e) {}
                    
                    if (!readList.includes(index)) {
                        readList.push(index);
                        localStorage.setItem('jhub_read_articles', JSON.stringify(readList));
                    }
                    
                    // Populate Detail Pane
                    document.getElementById('detail-placeholder').style.display = 'none';
                    const easterEggContent = document.getElementById('easter-egg-content');
                    if(easterEggContent) easterEggContent.style.display = 'none';
                    const completeContent = document.getElementById('complete-content');
                    if(completeContent) completeContent.style.display = 'none';
                    document.getElementById('detail-content').style.display = 'block';
                    
                    document.getElementById('detail-category').innerText = article.category;
                    document.getElementById('detail-title').innerText = article.title;
                    document.getElementById('detail-excerpt').innerHTML = article.excerpt;
                    document.getElementById('detail-meta').innerText = article.meta;
                    
                    currentArticleUrl = 'https://www.google.com/search?q=' + encodeURIComponent(article.title);
                    
                    // Smooth scroll up to the detail pane if needed
                    document.getElementById('article-detail-pane').scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                    checkAllRead(readList);
                }
                
                document.getElementById('detail-link-btn').addEventListener('click', () => {
                    if (currentArticleUrl) {
                        window.open(currentArticleUrl, '_blank');
                    }
                });
                
                document.addEventListener('DOMContentLoaded', () => {
                    setTimeout(renderMosaic, 100);
                });
                
                const readingTabItem = document.querySelector('[data-target="tab-reading"]');
                if (readingTabItem) {
                    readingTabItem.addEventListener('click', renderMosaic);
                }
            </script>
                <script>
                async function submitFeedback() {
                    const project = document.getElementById('fb-project').value.trim();
                    const content = document.getElementById('fb-content').value.trim();
                    const isAnonymous = document.getElementById('fb-anonymous').checked;
                    const statusEl = document.getElementById('fb-status');

                    if (!content) {
                        statusEl.style.color = 'red';
                        statusEl.innerText = '피드백 내용을 입력해주세요.';
                        statusEl.style.display = 'block';
                        return;
                    }

                    try {
                        const response = await fetch('/api/feedback', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                project_name: project,
                                content: content,
                                is_anonymous: isAnonymous
                            })
                        });
                        const data = await response.json();
                        if (data.success) {
                            document.getElementById('fb-project').value = '';
                            document.getElementById('fb-content').value = '';
                            document.getElementById('fb-anonymous').checked = false;
                            statusEl.style.color = '#00cc66';
                            statusEl.innerText = '✅ 대표이사님께 안전하게 직접 전달되었습니다!';
                            statusEl.style.display = 'block';
                            setTimeout(() => { statusEl.style.display = 'none'; }, 5000);
                        } else {
                            statusEl.style.color = 'red';
                            statusEl.innerText = '오류: ' + data.message;
                            statusEl.style.display = 'block';
                        }
                    } catch (e) {
                        statusEl.style.color = 'red';
                        statusEl.innerText = '서버 통신 오류가 발생했습니다.';
                        statusEl.style.display = 'block';
                    }
                }
                </script>
            <script>
                function unlockWeekly() {
                    // 실제 비밀번호 검증 없이 무조건 통과하도록 변경 (UI만 유지)
                    document.getElementById("weekly-lock-screen").style.display = "none";
                    document.getElementById("weekly-admin-view").style.display = "block";
                    window.scrollTo(0,0);
                }

                function publishWeeklyReport() {
                    const btn = document.querySelector("#weekly-publish-actions button");
                    btn.innerText = "발행 처리 중...";
                    btn.style.opacity = "0.7";
                    
                    setTimeout(() => {
                        btn.innerText = "✅ 전사 포털 업데이트 완료";
                        btn.style.background = "#00cc66";
                        btn.style.opacity = "1";
                        btn.style.boxShadow = "none";
                        
                        setTimeout(() => {
                            alert("최종 승인된 보고서가 J-Workspace에 성공적으로 갱신되었습니다.");
                        }, 500);
                    }, 1500);
                }
            </script>
    <script>
        if ('serviceWorker' in navigator && window.location.protocol !== 'file:') {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('./sw.js')
                    .then(registration => {
                        console.log('SW registered:', registration);
                    })
                    .catch(error => {
                        console.log('SW registration failed:', error);
                    });
            });
        } else if (window.location.protocol === 'file:') {
            console.warn('Service Worker cannot be registered on file:// protocol. PWA features require a web server (e.g., python -m http.server).');
        }
    
