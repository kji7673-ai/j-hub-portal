
        // Lead Magnet Unlock Logic
        function initLeadMagnet() {
            const wrapper = document.getElementById('mdContentWrapper');
            if (!wrapper) return;
            
            if (localStorage.getItem('jhub_unlocked') === 'true') {
                wrapper.classList.add('unlocked');
                wrapper.style.maxHeight = 'none';
                return;
            }
            
            // Smart Blinding Logic
            const targets = Array.from(wrapper.querySelectorAll('h2, h3, h4, .episode'));
            const target = targets.find(el => /사례|case|프롬프트|실전|예시/i.test(el.textContent));
            
            let cutHeight = 800; // fallback
            if (target) {
                cutHeight = target.offsetTop + 40; 
            } else {
                cutHeight = wrapper.scrollHeight * 0.6;
            }
            
            if (wrapper.scrollHeight < 600) {
                cutHeight = wrapper.scrollHeight * 0.6;
            }
            
            wrapper.style.maxHeight = cutHeight + 'px';
        }

        function masterLogin() {
            const pwd = prompt("직원 인증 마스터 키워드를 입력하세요:");
            if (pwd === "jinyang2026") {
                localStorage.setItem('jhub_unlocked', 'true');
                alert("직원 인증이 완료되었습니다. 모든 문서가 개방됩니다.");
                location.reload();
            } else if (pwd !== null) {
                alert("키워드가 일치하지 않습니다.");
            }
        }
        function unlockContent() {
            const email = document.getElementById('lmEmail').value.trim();
            const company = document.getElementById('lmCompany').value.trim();
            
            if (!email || !company) {
                alert('이메일과 소속 회사를 모두 입력해주세요.');
                return;
            }
            if (!email.includes('@')) {
                alert('유효한 이메일 주소를 입력해주세요.');
                return;
            }
            
            // Webhook payload placeholder (Supabase / Google Forms)
            console.log('[Lead Capture] ' + email + ' / ' + company);
            
            localStorage.setItem('jhub_unlocked', 'true');
            const wrapper = document.getElementById('mdContentWrapper');
            if (wrapper) wrapper.classList.add('unlocked');
        }
        document.addEventListener('DOMContentLoaded', initLeadMagnet);

        // Menu Logic
        function toggleMenu() {
            if (window.innerWidth <= 900) {
                document.getElementById('mobileMenu').classList.add('active');
                document.body.style.overflow = 'hidden';
            } else {
                document.getElementById('desktopSidebar').classList.toggle('collapsed');
                document.getElementById('mainWrapper').classList.toggle('collapsed');
            }
        }
        function closeMobileMenu() {
            document.getElementById('mobileMenu').classList.remove('active');
            document.body.style.overflow = '';
        }
        

        // Favorites
        function toggleFavorite() {
            const pageId = window.location.pathname.split('/').pop() || 'index.html';
            if (pageId === 'index.html') return;
            const title = document.title.split(' - ')[0];
            let favs = JSON.parse(localStorage.getItem('jhub_favs') || '[]');
            const idx = favs.findIndex(f => f.url === pageId);
            if (idx > -1) {
                favs.splice(idx, 1);
                document.getElementById('favIcon').setAttribute('fill', 'none');
                document.getElementById('favIcon').style.color = 'inherit';
            } else {
                favs.push({url: pageId, title: title});
                document.getElementById('favIcon').setAttribute('fill', '#f5a623');
                document.getElementById('favIcon').style.color = '#f5a623';
            }
            localStorage.setItem('jhub_favs', JSON.stringify(favs));
        }
        
        function initFavorite() {
            const pageId = window.location.pathname.split('/').pop() || 'index.html';
            const favs = JSON.parse(localStorage.getItem('jhub_favs') || '[]');
            const isFav = favs.some(f => f.url === pageId);
            if (isFav && document.getElementById('favIcon')) {
                document.getElementById('favIcon').setAttribute('fill', '#f5a623');
                document.getElementById('favIcon').style.color = '#f5a623';
            }
        }
        
        document.addEventListener('DOMContentLoaded', initFavorite);

        // Progress & Quiz Analytics Logic (서버 DB 기반)
        const totalDocs = 27;
        async function initAnalytics() {
            try {
                const res = await fetch('/api/edu/analytics');
                if (!res.ok) throw new Error('API error');
                const data = await res.json();
                if (!data.success) throw new Error('Not logged in');
                
                const completedCount = data.completed_count || 0;
                const percentage = totalDocs > 0 ? Math.round((completedCount / totalDocs) * 100) : 0;
                
                if(document.getElementById('progressFill')) {
                    document.getElementById('progressFill').style.width = percentage + '%';
                    document.getElementById('progressText').innerText = `${completedCount}개 완독 (${percentage}%)`;
                }
                
                const progress = data.progress || {};
                Object.keys(progress).forEach(id => {
                    const card = document.getElementById('card_' + id);
                    if(card && !card.querySelector('.badge-done')) {
                        const badge = document.createElement('div');
                        badge.className = 'badge-done';
                        badge.innerHTML = '✓';
                        badge.title = '완독 완료';
                        card.appendChild(badge);
                    }
                });

                const quizAvg = data.quiz_average || 0;
                const quizScores = data.quiz_scores || {};
                if(document.getElementById('quizScoreText')) {
                    if(Object.keys(quizScores).length > 0) {
                        document.getElementById('quizScoreText').innerText = quizAvg + '점';
                    } else {
                        document.getElementById('quizScoreText').innerText = '-';
                    }
                }
            } catch(e) {
                console.warn('[J-Hub] 서버 연결 실패, localStorage fallback:', e.message);
                let progress = JSON.parse(localStorage.getItem('jhub_progress') || '{}');
                let completedCount = Object.keys(progress).filter(k => progress[k] === true).length;
                let percentage = totalDocs > 0 ? Math.round((completedCount / totalDocs) * 100) : 0;
                if(document.getElementById('progressFill')) {
                    document.getElementById('progressFill').style.width = percentage + '%';
                    document.getElementById('progressText').innerText = `${completedCount}개 완독 (${percentage}%)`;
                }
            }
        }
        document.addEventListener('DOMContentLoaded', initAnalytics);



        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (document.getElementById('searchOverlay').classList.contains('active')) return;
            if (e.key === 'ArrowLeft') {
                const prev = document.querySelector('.btn-page[href^="page_"]:first-child');
                if (prev) window.location.href = prev.href;
            } else if (e.key === 'ArrowRight') {
                const next = document.querySelector('.btn-page[href^="page_"]:last-child');
                if (next) window.location.href = next.href;
            }
        });
        
        // Copy buttons for pre
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('.md-content pre').forEach(pre => {
                const btn = document.createElement('button');
                btn.className = 'copy-btn';
                btn.innerText = '복사';
                btn.onclick = () => {
                    navigator.clipboard.writeText(pre.innerText).then(() => {
                        btn.innerText = '완료!';
                        setTimeout(() => btn.innerText = '복사', 2000);
                    });
                };
                pre.appendChild(btn);
            });
        });
        
        function toggleMobileToc() {
            document.getElementById('mobileTocSheet').classList.toggle('active');
            document.getElementById('mobileTocOverlay').classList.toggle('active');
        }

        // Search Logic
        const searchOverlay = document.getElementById('searchOverlay');
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');

        function openSearch() {
            searchOverlay.classList.add('active');
            setTimeout(() => searchInput.focus(), 100);
            document.body.style.overflow = 'hidden';
        }

        function closeSearch() {
            searchOverlay.classList.remove('active');
            searchInput.value = '';
            searchResults.innerHTML = '';
            document.body.style.overflow = '';
        }



        function showSecurityToast() {
            const toast = document.getElementById('securityToast');
            if (toast) {
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 3000);
            }
        }

        // Anti-Print Security
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && (e.key === 'p' || e.key === 'P')) {
                e.preventDefault();
                showSecurityToast();
            }
        });
        
        // Anti-Copy (Optional, maybe too aggressive, but let's add contextmenu prevention for images only)
        document.addEventListener('contextmenu', function(e) {
            if (e.target.tagName === 'IMG') {
                e.preventDefault();
            }
        });

        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            if (query.length < 2) {
                searchResults.innerHTML = '';
                return;
            }
            
            const results = searchIndex.filter(item => 
                item.title.toLowerCase().includes(query) || 
                item.content.toLowerCase().includes(query)
            );
            
            if (results.length === 0) {
                searchResults.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--ink-muted);">검색 결과가 없습니다.</div>';
                return;
            }
            
            let html = '';
            results.slice(0, 15).forEach(item => {
                let snippet = item.content;
                const matchIdx = snippet.toLowerCase().indexOf(query);
                if (matchIdx > -1) {
                    const start = Math.max(0, matchIdx - 30);
                    const end = Math.min(snippet.length, matchIdx + query.length + 40);
                    snippet = (start > 0 ? '...' : '') + 
                              snippet.substring(start, matchIdx) + 
                              '<span class="highlight">' + snippet.substring(matchIdx, matchIdx + query.length) + '</span>' + 
                              snippet.substring(matchIdx + query.length, end) + 
                              (end < snippet.length ? '...' : '');
                } else {
                    snippet = snippet.substring(0, 80) + '...';
                }
                
                let titleHtml = item.title;
                const titleIdx = titleHtml.toLowerCase().indexOf(query);
                if (titleIdx > -1) {
                    titleHtml = titleHtml.substring(0, titleIdx) + 
                                '<span class="highlight">' + titleHtml.substring(titleIdx, titleIdx + query.length) + '</span>' + 
                                titleHtml.substring(titleIdx + query.length);
                }
                
                html += `
                    <a href="${item.url}" class="search-result-item">
                        <div class="search-result-cat">${item.category}</div>
                        <div class="search-result-title">${titleHtml}</div>
                        <div class="search-result-snippet">${snippet}</div>
                    </a>
                `;
            });
            searchResults.innerHTML = html;
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
                closeSearch();
            }
        });
        

        // Load Favorites on Dashboard
        document.addEventListener('DOMContentLoaded', () => {
            const favs = JSON.parse(localStorage.getItem('jhub_favs') || '[]');
            if (favs.length > 0) {
                document.getElementById('favoritesSection').style.display = 'block';
                const html = favs.map(f => `
                    <a href="${f.url}" style="display:flex; align-items:center; text-decoration:none; padding:12px 16px; background:var(--canvas); border:1px solid var(--hairline); border-radius:8px;">
                        <span style="font-size:15px; font-weight:600; color:var(--ink);">${f.title}</span>
                    </a>
                `).join('');
                document.getElementById('favoritesList').innerHTML = html;
            }
        });

        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('./sw.js').catch(err => {});
            });
        }
    