    <script>
        // Dark Mode Logic
        function initTheme() {
            const saved = localStorage.getItem('theme');
            if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                document.documentElement.setAttribute('data-theme', 'dark');
            }
        }
        initTheme();
        function toggleTheme() {
            const current = document.documentElement.getAttribute('data-theme');
            if (current === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            }
        }
    </script>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
--
            
            localStorage.setItem('jhub_unlocked', 'true');
            const wrapper = document.getElementById('mdContentWrapper');
            if (wrapper) wrapper.classList.add('unlocked');
        }}
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
        function toggleFavorite() {{
            const pageId = window.location.pathname.split('/').pop() || 'index.html';
            if (pageId === 'index.html') return;
            const title = document.title.split(' - ')[0];
            let favs = JSON.parse(localStorage.getItem('jhub_favs') || '[]');
            const idx = favs.findIndex(f => f.url === pageId);
            if (idx > -1) {{
                favs.splice(idx, 1);
                document.getElementById('favIcon').setAttribute('fill', 'none');
                document.getElementById('favIcon').style.color = 'inherit';
            }} else {{
                favs.push({{url: pageId, title: title}});
                document.getElementById('favIcon').setAttribute('fill', '#f5a623');
                document.getElementById('favIcon').style.color = '#f5a623';
            }}
            localStorage.setItem('jhub_favs', JSON.stringify(favs));
        }}
        
        function initFavorite() {{
            const pageId = window.location.pathname.split('/').pop() || 'index.html';
            const favs = JSON.parse(localStorage.getItem('jhub_favs') || '[]');
            const isFav = favs.some(f => f.url === pageId);
--
    <script>
        function toggleRag() {
            const w = document.getElementById('ragWindow');
            w.classList.toggle('active');
            if (w.classList.contains('active')) document.getElementById('ragInput').focus();
        }
        
        function appendMsg(text, isAi) {
            const b = document.getElementById('ragBody');
            const d = document.createElement('div');
            d.className = 'rag-bubble ' + (isAi ? 'ai' : 'user');
            d.innerHTML = text;
            b.appendChild(d);
            b.scrollTop = b.scrollHeight;
        }
        
        function submitRag() {
            const inp = document.getElementById('ragInput');
            const q = inp.value.trim();
            if (!q) return;
            inp.value = '';
            appendMsg(q, false);
            
            // 유사 RAG 검색 알고리즘 (searchIndex 활용)
            setTimeout(() => {
                const words = q.toLowerCase().split(/\s+/).filter(w => w.length > 1);
                let bestMatch = null;
                let maxScore = 0;
                
                if (typeof searchIndex !== 'undefined') {
                    searchIndex.forEach(item => {
                        let score = 0;
                        const text = (item.title + " " + item.content).toLowerCase();
                        words.forEach(w => {
                            const matches = text.split(w).length - 1;
                            score += matches;
                        });
                        if (score > maxScore) {
                            maxScore = score;
                            bestMatch = item;
                        }
                    });
                }
                
                if (bestMatch && maxScore > 0) {
                    const snippet = bestMatch.content.substring(0, 150) + "...";
                    const reply = `가장 적합한 내용을 찾았습니다!<br><br><b>[${bestMatch.title}]</b><br><span style="color:var(--ink-muted);font-size:12px;">${snippet}</span><br><br><a href="${bestMatch.url}" style="display:inline-block; margin-top:8px; padding:6px 12px; background:rgba(0,102,204,0.1); color:var(--primary); border-radius:6px; text-decoration:none; font-weight:600; font-size:12px;">📖 해당 문서 바로가기</a>`;
                    appendMsg(reply, true);
                } else {
                    appendMsg("죄송합니다, 관련된 내용을 찾지 못했습니다. 다른 검색어로 질문해 주시겠어요?", true);
                }
            }, 500);
        }
    </script>
