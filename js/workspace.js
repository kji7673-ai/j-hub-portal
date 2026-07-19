// FUNC-01 FIX: workspace.js — SSG(정적 빌드) 방식에 맞게 Dead Code 제거
// build_jhub.py가 정적 HTML을 생성하므로, 
// CSR(클라이언트 사이드 렌더링) 로직은 더 이상 사용되지 않음.
// getCurrentWeekLabel()만 유지하여 동적 주차 표시에 사용.

// 날짜 유틸: 현재 주차 레이블 생성 (유지)
function getCurrentWeekLabel() {
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    const firstDay = startOfMonth.getDay(); 
    const offset = (firstDay + 6) % 7; // Monday as first day of week
    const weekNum = Math.ceil((now.getDate() + offset) / 7);
    const month = now.getMonth() + 1;
    return `${month}월 ${weekNum}주차`;
}

// 동적 타임스탬프 업데이트 — 빌드 시점이 아닌 접속 시점 표시
document.addEventListener('DOMContentLoaded', () => {
    // 최종 업데이트 시간 동적 표시
    const syncTimeEl = document.querySelector('[data-sync-time]');
    if (syncTimeEl) {
        const now = new Date();
        const formatted = `${now.getFullYear()}.${String(now.getMonth()+1).padStart(2,'0')}.${String(now.getDate()).padStart(2,'0')} ${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
        syncTimeEl.textContent = formatted + ' (접속 시점)';
    }
    
    // 주차 레이블 동적 업데이트
    document.querySelectorAll('[data-week-label]').forEach(el => {
        el.textContent = getCurrentWeekLabel();
    });
});
