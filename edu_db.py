"""
J-Hub 교육 플랫폼 — SQLite 데이터 모델
학습 진도(progress)와 퀴즈 점수(quiz_scores)를 중앙 DB에 저장합니다.
"""
import sqlite3
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'edu_data.db')


def get_db():
    """SQLite 연결을 반환합니다."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # 동시 읽기 성능 향상
    return conn


def init_db():
    """테이블이 없으면 생성합니다. 서버 시작 시 1회 호출."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS edu_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_hash TEXT NOT NULL,
            doc_id INTEGER NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_hash, doc_id)
        );

        CREATE TABLE IF NOT EXISTS edu_quiz_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_hash TEXT NOT NULL,
            doc_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_hash, doc_id)
        );

        CREATE INDEX IF NOT EXISTS idx_progress_user ON edu_progress(user_hash);
        CREATE INDEX IF NOT EXISTS idx_quiz_user ON edu_quiz_scores(user_hash);
    """)
    conn.close()


# ═══════════════════════════════════════════════
# CRUD Operations
# ═══════════════════════════════════════════════

def save_progress(user_hash, doc_id):
    """문서 완독 기록을 저장합니다. 이미 완독한 경우 무시합니다."""
    conn = get_db()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO edu_progress (user_hash, doc_id) VALUES (?, ?)",
            (user_hash, doc_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[edu_db] save_progress error: {e}")
        return False
    finally:
        conn.close()


def get_user_progress(user_hash):
    """사용자의 전체 완독 현황을 반환합니다.
    Returns: {doc_id: completed_at_timestamp, ...}
    """
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT doc_id, completed_at FROM edu_progress WHERE user_hash = ?",
            (user_hash,)
        ).fetchall()
        return {row['doc_id']: row['completed_at'] for row in rows}
    finally:
        conn.close()


def save_quiz_score(user_hash, doc_id, score):
    """퀴즈 점수를 저장합니다. 기존 점수가 있으면 덮어씁니다."""
    conn = get_db()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO edu_quiz_scores (user_hash, doc_id, score) VALUES (?, ?, ?)",
            (user_hash, doc_id, score)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[edu_db] save_quiz_score error: {e}")
        return False
    finally:
        conn.close()


def get_user_quiz_scores(user_hash):
    """사용자의 전체 퀴즈 점수를 반환합니다.
    Returns: {doc_id: score, ...}
    """
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT doc_id, score FROM edu_quiz_scores WHERE user_hash = ?",
            (user_hash,)
        ).fetchall()
        return {row['doc_id']: row['score'] for row in rows}
    finally:
        conn.close()


def get_admin_overview():
    """관리자용 전체 현황을 반환합니다.
    Returns: {
        'total_users': int,
        'user_progress': {user_hash: [doc_ids]},
        'user_quiz_scores': {user_hash: {doc_id: score}},
        'module_completion': {doc_id: count}
    }
    """
    conn = get_db()
    try:
        # 전체 사용자 수
        users = conn.execute(
            "SELECT DISTINCT user_hash FROM edu_progress"
        ).fetchall()
        user_hashes = [r['user_hash'] for r in users]

        # 사용자별 진도
        user_progress = {}
        for uh in user_hashes:
            rows = conn.execute(
                "SELECT doc_id FROM edu_progress WHERE user_hash = ?", (uh,)
            ).fetchall()
            user_progress[uh] = [r['doc_id'] for r in rows]

        # 모듈별 완료 수
        module_rows = conn.execute(
            "SELECT doc_id, COUNT(*) as cnt FROM edu_progress GROUP BY doc_id"
        ).fetchall()
        module_completion = {r['doc_id']: r['cnt'] for r in module_rows}

        # 사용자별 퀴즈 점수
        user_quiz_scores = {}
        quiz_rows = conn.execute(
            "SELECT user_hash, doc_id, score FROM edu_quiz_scores"
        ).fetchall()
        for r in quiz_rows:
            if r['user_hash'] not in user_quiz_scores:
                user_quiz_scores[r['user_hash']] = {}
            user_quiz_scores[r['user_hash']][r['doc_id']] = r['score']

        return {
            'total_users': len(user_hashes),
            'user_progress': user_progress,
            'user_quiz_scores': user_quiz_scores,
            'module_completion': module_completion
        }
    finally:
        conn.close()
