869:    <script>
870-        let currentChapter = 0;
871-        let currentColumn = 0;
872-        const COLUMN_GAP = 40;
873-
874-        
875-        function renderTOC() {
876-            const tocList = document.getElementById('toc-list');
877-            if(!tocList) return;
878-            tocList.innerHTML = '';
879-            let currentCategory = null;
880-
881-            bookData.pages.forEach((page, index) => {
882-                if (page.type === "author_profile") return;
883-                if (page.title && page.title.trim() !== "" && !page.title.includes("(계속)")) {
884-                    let cat = page.partCategory || "프롤로그";
885-                    if (cat !== currentCategory) {
886-                        currentCategory = cat;
887-                        const catHeader = document.createElement('div');
888-                        catHeader.className = 'toc-category';
889-                        catHeader.innerText = cat;
890-                        tocList.appendChild(catHeader);
891-                    }
892-                    
893-                    const li = document.createElement('li');
894-                    li.className = 'toc-item';
895-                    li.innerHTML = '<span class="toc-title">' + page.title + '</span>';
896-                    li.onclick = () => {
897-                        currentChapter = index;
898-                        currentColumn = 0;
899-                        renderCurrentChapter();
900-                        document.getElementById('toc-modal').style.display = 'none';
901-                    };
902-                    tocList.appendChild(li);
903-                }
904-            });
905-        }
906-
907-        function renderCurrentChapter() {
908-            const container = document.getElementById('book-container');
909-            // Keep the controls div intact
910-            const controls = document.querySelector('.controls');
911-            
912-            // Remove all existing page-content
913-            document.querySelectorAll('.page-content').forEach(p => p.remove());
914-
915-            const page = bookData.pages[currentChapter];
916-            if(!page) return;
917-
918-            const pageEl = document.createElement('div');
919-            pageEl.className = 'page-content active';
920-            pageEl.id = 'page-' + currentChapter;
921-            
922-            let contentHTML = '';
923-            
924-            if (page.type === 'cover' || page.type === 'interlude') {
925-                pageEl.style.backgroundColor = '#ffffff';
926-                pageEl.style.color = '#1d1d1f';
927-                pageEl.style.padding = '0';
928-                let rawTitle = page.title || "";
929-                let pText = page.text || "";
930-                let bgStyle = page.image ? 'background: url('+page.image+') center center / cover no-repeat;' : 'background: #f5f5f7;';
931-                
932-                contentHTML += '<div class="cover-content" style="position:relative; z-index:2; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center; padding: 10% 8%;">';
933-                if(page.type === 'cover' && page.image) {
934-                    contentHTML += '<div style="position:absolute; top:0; left:0; right:0; bottom:0; background:rgba(255,255,255,0.7); z-index:-1;"></div>';
935-                }
936-                contentHTML += '<h1 style="font-size:2.5em; font-weight:800; margin-bottom:20px; letter-spacing:-0.5px; line-height:1.2;">' + rawTitle + '</h1>';
937-                if(pText) contentHTML += '<p style="font-size:1.2em; font-weight:400; color:#555; max-width:80%; line-height:1.6;">' + pText + '</p>';
938-                contentHTML += '</div>';
939-                pageEl.innerHTML = contentHTML;
940-            }
941-            else {
942-                pageEl.className += ' page-text-flow page-layout';
943-                if(page.image) contentHTML += '<div class="image-container" id="img-container-'+currentChapter+'" style="max-width: 800px; width: 90%; margin-bottom: 45px;"><img src="'+page.image+'" alt="sketch"></div>';
944-                if(page.title) contentHTML += '<h2 class="chapter-title" style="margin-bottom:20px;">' + page.title + '</h2>';
945-                if(page.text) {
946-                    let formattedText = page.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
947-                    formattedText = formattedText.replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px; margin: 24px auto; display: block; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">');
948-                    const paragraphs = formattedText.split('\n\n');
949-                    paragraphs.forEach(p => {
950-                        const trimmed = p.trim();
951-                        if (trimmed.startsWith('<table') || trimmed.startsWith('<div class="custom-table"')) {
952-                            contentHTML += '<div class="table-wrapper" style="width: 100%; overflow-x: auto; padding-bottom: 10px;">' + p + '</div>';
953-                        } else if (trimmed.startsWith('<h') || trimmed.startsWith('<ul') || trimmed.startsWith('<ol') || trimmed.startsWith('<div')) {
954-                            contentHTML += trimmed;
955-                        } else if (trimmed.startsWith('&gt;') || trimmed.startsWith('>')) {
956-                            let bqText = trimmed.replace(/^&gt;\s?/gm, '').replace(/^>\s?/gm, '');
957-                            bqText = bqText.replace(/\n/g, '<br>');
958-                            contentHTML += '<blockquote class="pull-quote">' + bqText + '</blockquote>';
959-                        } else if (trimmed.startsWith('<strong') && trimmed.endsWith('</strong>') && trimmed.indexOf('<strong', 1) === -1) {
960-                            contentHTML += '<p class="subheading">' + trimmed + '</p>';
961-                        } else {
962-                            let htmlP = p.replace(/\n(?=\d+\.\s)/g, '<br><br>');
963-                            htmlP = htmlP.replace(/\n/g, '<br>');
964-                            contentHTML += '<p class="body-text" style="line-height: 1.9; margin-bottom: 15px;">' + htmlP + '</p>';
965-                        }
966-                    });
967-                }
968-                pageEl.innerHTML = '<div class="page-inner">' + contentHTML + '</div>';
969-            }
970-            
971-            // Insert before controls
972-            container.insertBefore(pageEl, controls);
973-            
974-            // Reset scroll position to top whenever a new chapter is loaded
975-            pageEl.scrollTop = 0;
976-
977-            updateControls();
978-        }
979-
980-        function renderBook() {
981-            renderTOC();
982-            
983-            // Restore position if possible
984-            const savedChapter = localStorage.getItem('JJournal_savedChapter');
985-            if (savedChapter !== null) {
986-                const parsedChap = parseInt(savedChapter, 10);
987-                if(!isNaN(parsedChap)) {
988-                    currentChapter = Math.max(0, Math.min(parsedChap, bookData.pages.length - 1));
989-                }
990-            }
991-            
992-            renderCurrentChapter();
993-            updateBookmarkButton();
994-        }
995-
996-        function updateControls() {
997-            const totalChapters = bookData.pages.length;
998-            document.getElementById('prev-btn').disabled = (currentChapter === 0);
999-            document.getElementById('next-btn').disabled = (currentChapter === totalChapters - 1);
1000-            
1001-            // Since we abandoned multi-column horizontal pagination in favor of vertical scrolling, 
1002-            // currentColumn is basically obsolete, but we keep the UI simple:
1003-            document.getElementById('page-num').innerText = '[' + (currentChapter + 1) + ' / ' + totalChapters + ']';
1004-            
1005-            if(typeof saveProgress === 'function') saveProgress();
1006-        }
1007-
1008-        function prevPage() {
1009-            if (currentChapter > 0) {
1010-                currentChapter--;
1011-                currentColumn = 0;
1012-                renderCurrentChapter();
1013-            }
1014-        }
1015-
1016-        function nextPage() {
1017-            if (currentChapter < bookData.pages.length - 1) {
1018-                currentChapter++;
1019-                currentColumn = 0;
1020-                renderCurrentChapter();
1021-            }
1022-        }
1023-
1024-
1025-        function toggleBookmark() {
1026-            const chapterData = bookData.pages[currentChapter];
1027-            if (!chapterData) return;
1028-            
1029-            // Generate a unique ID for this position
1030-            const posId = currentChapter + '-' + currentColumn;
1031-            const idx = bookmarks.findIndex(b => b.id === posId);
1032-            
1033-            if (idx === -1) {
1034-                // Determine title snippet
1035-                let titleSnippet = chapterData.title || '페이지 ' + (currentChapter+1);
1036-                bookmarks.push({ 
1037-                    id: posId, 
1038-                    chapter: currentChapter, 
1039-                    column: currentColumn, 
1040-                    title: titleSnippet, 
1041-                    time: new Date().getTime() 
1042-                });
1043-                alert('현재 페이지를 책갈피에 추가했습니다.');
1044-            } else {
1045-                bookmarks.splice(idx, 1);
1046-                alert('현재 페이지의 책갈피를 해제했습니다.');
1047-            }
1048-            localStorage.setItem('JJournal_bookmarks_v2', JSON.stringify(bookmarks));
1049-            updateBookmarkButton();
1050-            setTimeout(() => updateControls(), 100);
1051-        }
1052-
1053-        function updateBookmarkButton() {
1054-            const btn = document.getElementById('bookmark-toggle-btn');
1055-            if (btn) {
1056-                const posId = currentChapter + '-' + currentColumn;
1057-                const isBookmarked = bookmarks.some(b => b.id === posId);
1058-                if(isBookmarked) {
1059-                    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z"></path></svg><span>해제</span>';
1060-                    btn.style.color = '#1d1d1f';
1061-                } else {
1062-                    btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z"></path></svg><span>책갈피</span>';
1063-                    btn.style.color = '#1d1d1f';
1064-                }
1065-            }
1066-        }
1067-
1068-        function openBookmarkList() {
1069-            const container = document.getElementById('bookmark-list-container');
