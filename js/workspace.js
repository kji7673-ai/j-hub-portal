// 날짜 유틸: 현재 주차 레이블 생성 (M-01 동적화)
function getCurrentWeekLabel() {
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    const firstDay = startOfMonth.getDay(); 
    const offset = (firstDay + 6) % 7; // Monday as first day of week
    const weekNum = Math.ceil((now.getDate() + offset) / 7);
    const month = now.getMonth() + 1;
    return `${month}월 ${weekNum}주차`;
}

document.addEventListener('DOMContentLoaded', () => {
    // J-Workspace 모드가 로드될 때 데이터를 가져옵니다.
    loadWorkspaceData();
});

async function loadWorkspaceData() {
    try {
        // 캐시 방지를 위해 타임스탬프 추가
        const response = await fetch('./data/workspace.json?t=' + new Date().getTime());
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        
        // 상단 업데이트 시간 렌더링
        const syncTimeEl = document.getElementById('workspace-sync-time');
        if (syncTimeEl) {
            syncTimeEl.innerText = data.lastUpdated;
        }

        // 섹션 1 렌더링
        renderSection1(data.section1);
        // 섹션 2 렌더링
        renderSection2(data.section2);
        // 섹션 3 렌더링
        renderSection3(data.section3);
        // 섹션 4 렌더링
        renderSection4(data.section4);

    } catch (error) {
        console.error('Failed to load workspace data:', error);
        // 에러 발생 시 사용자에게 알림
        const container = document.getElementById('workspace-sec1-content');
        if(container) {
            container.innerHTML = '<p style="color: red; padding: 20px;">데이터를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.</p>';
        }
    }
}

function renderSection1(data) {
    const container = document.getElementById('workspace-sec1-content');
    if (!container) return;

    let siteUpdatesHtml = data.siteUpdates.map(item => 
        `<li><span class="highlight">${item.name}</span> — ${item.desc}</li>`
    ).join('');

    let policyUpdatesHtml = data.policyUpdates.map(item => `
        <div class="report-item">
            <div class="tag-row"><span class="chip ${item.badgeClass}">${item.badge}</span></div>
            <h3 class="report-title">${item.title}</h3>
            <p class="report-desc">${item.desc}</p>
        </div>
        <div style="height: 1px; background: var(--divider-soft); margin: 8px 0;"></div>
    `).join('');

    container.innerHTML = `
        <p style="color:var(--text-secondary); margin-top:0;">${getCurrentWeekLabel()} 주요 변동 사항 및 핵심 요약</p>
        <div class="grid-2">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">현장 핵심 변동</div>
                    <span class="chip red">업데이트 완료</span>
                </div>
                <ul style="padding-left: 20px; font-size: 15px; color: var(--ink); line-height: 1.8;">
                    ${siteUpdatesHtml}
                </ul>
            </div>
            <div class="card">
                <div class="card-header">
                    <div class="card-title">법규/정책 핵심 변동</div>
                </div>
                ${policyUpdatesHtml}
            </div>
        </div>
    `;
}

function renderSection2(data) {
    const container = document.getElementById('workspace-sec2-content');
    if (!container) return;

    let deptsHtml = data.departments.map(dept => {
        let rows = dept.projects.map(p => `
            <tr>
                <td>${p.highlight ? `<span class="highlight">${p.name}</span>` : p.name}</td>
                <td>${p.status}</td>
            </tr>
        `).join('');
        return `
            <h3 style="font-size:16px; margin: 10px 0 5px 0; color:var(--accent);">■ ${dept.name}</h3>
            <table class="card-table">
                <tr><th>프로젝트</th><th>진행 현황</th></tr>
                ${rows}
            </table>
        `;
    }).join('');

    let biddingRows = data.bidding.map(b => `
        <tr>
            <td>${b.highlight ? `<span class="highlight">${b.name}</span>` : b.name}</td>
            <td>${b.schedule}</td>
            <td>${b.position}</td>
        </tr>
    `).join('');

    let adjacentHtml = data.adjacentTrends.map(trend => `
        <div class="accordion" style="margin-bottom:12px;">
            <div class="acc-header" style="font-weight:700; margin-bottom:4px;">${trend.region}</div>
            <ul class="acc-body">
                ${trend.items.map(item => `<li>${item}</li>`).join('')}
            </ul>
        </div>
    `).join('');

    let apiRows = data.apiData.map(api => `
        <tr>
            <td><strong>${api.name}</strong></td>
            <td>${api.active ? `<span style="font-weight:700;">[ ${api.status} ]</span>` : `<span style="color:var(--text-secondary);">[ ${api.status} ]</span>`}</td>
            <td>${api.desc}</td>
        </tr>
    `).join('');

    container.innerHTML = `
        <p style="color:var(--text-secondary); margin-top:0;">본부별 현황, 입찰 전선, 인접지 및 정보몽땅</p>
        <div class="grid-2">
            <div>
                <div class="card">
                    <div class="card-header"><div class="card-title">본부별 주요 프로젝트</div></div>
                    ${deptsHtml}
                </div>
                <div class="card" style="margin-top: 32px;">
                    <div class="card-header">
                        <div class="card-title">입찰/수주 전선 (전략기획)</div>
                        <span class="chip red">총력전</span>
                    </div>
                    <table class="card-table">
                        <tr><th>프로젝트</th><th>일정</th><th>당사 지위</th></tr>
                        ${biddingRows}
                    </table>
                </div>
            </div>
            <div>
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">인접지 개발 동향</div>
                        <span class="chip">완벽 복원</span>
                    </div>
                    ${adjacentHtml}
                </div>
                <div class="card" style="margin-top: 32px;">
                    <div class="card-header">
                        <div class="card-title">정보몽땅 자동 크롤링 (API)</div>
                        <span class="chip blue">실시간 연동</span>
                    </div>
                    <table class="card-table">
                        <tr><th>구역</th><th>상태</th><th>변동 내역</th></tr>
                        ${apiRows}
                    </table>
                </div>
            </div>
        </div>
    `;
}

function renderSection3(data) {
    const container = document.getElementById('workspace-sec3-content');
    if (!container) return;

    let daysHtml = data.map(day => `
        <div class="day-block">
            <div class="day-header">
                <div class="day-date">${day.date}</div>
                <div class="day-weekday">${day.weekday}</div>
            </div>
            <div class="event-card ${day.important ? 'important' : ''}">
                <div class="event-name">${day.event}</div>
                <div class="event-note">${day.note}</div>
            </div>
        </div>
    `).join('');

    container.innerHTML = `
        <p style="color:var(--text-secondary); margin-top:0;">향후 2주간의 본부별 총회, 미팅, 인허가 일정</p>
        <div class="card" style="max-width: 800px; margin: 0 auto;">
            <div class="card-header">
                <div class="card-title">${getCurrentWeekLabel()} 주요 일정</div>
                <button class="chip">캘린더 연동</button>
            </div>
            ${daysHtml}
        </div>
    `;
}

function renderSection4(data) {
    const container = document.getElementById('workspace-sec4-content');
    if (!container) return;

    let newLawsRows = data.newLaws.map(law => `
        <tr><td>${law.date}</td><td>${law.name}</td><td>${law.desc}</td></tr>
    `).join('');

    let localNoticesHtml = data.localNotices.map(notice => `<li>${notice}</li>`).join('');

    let suggestionsRows = data.suggestions10.map(s => `
        <tr>
            <td>${s.item}</td>
            <td>${s.current}</td>
            <td><strong style="color:var(--text-primary)">${s.suggested}</strong></td>
            <td>${s.status}</td>
        </tr>
    `).join('');

    container.innerHTML = `
        <p style="color:var(--text-secondary); margin-top:0;">최근 30일 이내 신규 시행 법령 및 10대 건의안 추적</p>
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><div class="card-title">신규 시행 법령</div></div>
                <table class="card-table">
                    <tr><th>시행일</th><th>법령</th><th>주요 내용</th></tr>
                    ${newLawsRows}
                </table>
            </div>
            <div class="card">
                <div class="card-header"><div class="card-title">지자체 고시/공고</div></div>
                <ul>${localNoticesHtml}</ul>
            </div>
            <div class="card" style="grid-column: 1 / -1; margin-top: 32px;">
                <div class="card-header"><div class="card-title">서울시 10대 법령 개정 건의안 추적표</div></div>
                <table class="card-table">
                    <tr><th>건의 항목</th><th>현행</th><th>건의안</th><th>상태</th></tr>
                    ${suggestionsRows}
                </table>
            </div>
        </div>
    `;
}
