document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (!searchInput || !searchResults) return;

    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase().trim();
        searchResults.innerHTML = '';
        
        if (query.length < 2) return;
        
        if (typeof searchIndex === 'undefined') {
            searchResults.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--ink-muted);">검색 인덱스를 불러오는 중입니다...</div>';
            return;
        }

        const matches = searchIndex.filter(item => 
            item.title.toLowerCase().includes(query) || 
            item.content.toLowerCase().includes(query)
        );

        if (matches.length === 0) {
            searchResults.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--ink-muted);">검색 결과가 없습니다.</div>';
            return;
        }

        matches.forEach(match => {
            const resultItem = document.createElement('a');
            resultItem.href = match.url;
            resultItem.className = 'search-result-item';
            resultItem.style = 'display: block; padding: 16px; border-bottom: 1px solid var(--hairline); text-decoration: none;';
            
            // Highlight title
            const titleHtml = highlightText(match.title, query);
            
            // Extract snippet
            const snippet = extractSnippet(match.content, query);
            const snippetHtml = highlightText(snippet, query);
            
            resultItem.innerHTML = `
                <div style="font-size: 11px; font-weight: 700; color: var(--primary); margin-bottom: 4px;">${match.category || '문서'}</div>
                <div style="font-size: 16px; font-weight: 600; color: var(--ink); margin-bottom: 8px;">${titleHtml}</div>
                <div style="font-size: 13px; color: var(--ink-muted); line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">${snippetHtml}</div>
            `;
            
            // Hover effect
            resultItem.addEventListener('mouseenter', () => resultItem.style.backgroundColor = 'var(--canvas-parchment)');
            resultItem.addEventListener('mouseleave', () => resultItem.style.backgroundColor = 'transparent');
            
            searchResults.appendChild(resultItem);
        });
    });

    function extractSnippet(text, query) {
        const index = text.toLowerCase().indexOf(query);
        if (index === -1) return text.substring(0, 100) + '...';
        
        const start = Math.max(0, index - 40);
        const end = Math.min(text.length, index + query.length + 40);
        let snippet = text.substring(start, end);
        
        if (start > 0) snippet = '...' + snippet;
        if (end < text.length) snippet = snippet + '...';
        
        return snippet;
    }

    function highlightText(text, query) {
        const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')})`, 'gi');
        return text.replace(regex, '<span style="background-color: rgba(0,102,204,0.15); color: var(--primary); font-weight: 700;">$1</span>');
    }
});
