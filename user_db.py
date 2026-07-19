"""
J-Hub 포털 — 회원 관리 데이터베이스
회원가입 신청, 계정 등록, 비밀번호 초기화를 위한 SQLite 모델.
"""
import sqlite3
import os
import uuid
import datetime
import hashlib
import unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), 'edu_data.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_user_tables():
    """회원 관리 테이블을 생성합니다. 서버 시작 시 1회 호출."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS join_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT,
            position TEXT,
            contact TEXT,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            reject_reason TEXT,
            approval_token TEXT,
            requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS user_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            username_hash TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            display_name TEXT NOT NULL,
            department TEXT,
            position TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            last_login TIMESTAMP,
            reset_token TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_join_status ON join_requests(status);
        CREATE INDEX IF NOT EXISTS idx_user_active ON user_accounts(is_active);
    """)
    conn.close()


def _hash(text):
    """SHA-256 해시를 생성합니다."""
    normalized = unicodedata.normalize('NFC', text.strip())
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


# ═══════════════════════════════════════════════
# 회원가입 신청 (Join Requests)
# ═══════════════════════════════════════════════

def create_join_request(name, department='', position='', contact='', reason=''):
    """회원가입 신청을 생성합니다."""
    conn = get_db()
    try:
        conn.execute(
            """INSERT INTO join_requests (name, department, position, contact, reason)
               VALUES (?, ?, ?, ?, ?)""",
            (name.strip(), department.strip(), position.strip(), contact.strip(), reason.strip())
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[user_db] create_join_request error: {e}")
        return False
    finally:
        conn.close()


def get_join_requests(status=None):
    """회원가입 신청 목록을 반환합니다."""
    conn = get_db()
    try:
        if status:
            rows = conn.execute(
                "SELECT * FROM join_requests WHERE status = ? ORDER BY requested_at DESC", (status,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM join_requests ORDER BY requested_at DESC"
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def approve_request(request_id):
    """신청을 승인하고 등록 토큰을 발급합니다."""
    token = uuid.uuid4().hex
    conn = get_db()
    try:
        conn.execute(
            """UPDATE join_requests
               SET status = 'approved', approval_token = ?, processed_at = ?
               WHERE id = ? AND status = 'pending'""",
            (token, datetime.datetime.now().isoformat(), request_id)
        )
        conn.commit()
        return token
    except Exception as e:
        print(f"[user_db] approve_request error: {e}")
        return None
    finally:
        conn.close()


def reject_request(request_id, reason=''):
    """신청을 거절합니다."""
    conn = get_db()
    try:
        conn.execute(
            """UPDATE join_requests
               SET status = 'rejected', reject_reason = ?, processed_at = ?
               WHERE id = ? AND status = 'pending'""",
            (reason, datetime.datetime.now().isoformat(), request_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[user_db] reject_request error: {e}")
        return False
    finally:
        conn.close()


def get_request_by_token(token):
    """토큰으로 승인된 신청을 조회합니다."""
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT * FROM join_requests WHERE approval_token = ? AND status = 'approved'",
            (token,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def consume_token(token):
    """등록 완료 후 토큰을 소비(무효화)합니다."""
    conn = get_db()
    try:
        conn.execute(
            "UPDATE join_requests SET status = 'registered', approval_token = NULL WHERE approval_token = ?",
            (token,)
        )
        conn.commit()
    finally:
        conn.close()


# ═══════════════════════════════════════════════
# 회원 계정 (User Accounts)
# ═══════════════════════════════════════════════

def register_user(username, password, display_name, department='', position=''):
    """새 회원을 등록합니다."""
    conn = get_db()
    try:
        conn.execute(
            """INSERT INTO user_accounts
               (username, username_hash, password_hash, display_name, department, position)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (username.strip(), _hash(username), _hash(password), display_name, department, position)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # 중복 아이디
    except Exception as e:
        print(f"[user_db] register_user error: {e}")
        return False
    finally:
        conn.close()


def check_user_login(username, password):
    """user_accounts 테이블에서 로그인을 검증합니다.
    Returns: dict(display_name, department, ...) or None
    """
    conn = get_db()
    try:
        row = conn.execute(
            """SELECT * FROM user_accounts
               WHERE username_hash = ? AND password_hash = ? AND is_active = 1""",
            (_hash(username), _hash(password))
        ).fetchone()
        if row:
            # 마지막 로그인 시간 업데이트
            conn.execute(
                "UPDATE user_accounts SET last_login = ? WHERE id = ?",
                (datetime.datetime.now().isoformat(), row['id'])
            )
            conn.commit()
            return dict(row)
        return None
    finally:
        conn.close()


def verify_password_by_display_name(display_name, password):
    """display_name(실명)과 비밀번호로 user_accounts 사용자를 검증합니다.
    세션에 display_name이 저장된 사용자의 비밀번호 변경에 사용됩니다.
    Returns: dict(id, username, display_name, ...) or None
    """
    conn = get_db()
    try:
        row = conn.execute(
            """SELECT * FROM user_accounts
               WHERE display_name = ? AND password_hash = ? AND is_active = 1""",
            (display_name, _hash(password))
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_all_members():
    """등록된 전체 회원 목록을 반환합니다. (비밀번호 해시 제외)"""
    conn = get_db()
    try:
        rows = conn.execute(
            """SELECT id, username, display_name, department, position,
                      registered_at, is_active, last_login
               FROM user_accounts ORDER BY registered_at DESC"""
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def reset_user_password(user_id):
    """비밀번호를 초기화하고 재설정 토큰을 발급합니다."""
    token = uuid.uuid4().hex
    conn = get_db()
    try:
        conn.execute(
            "UPDATE user_accounts SET reset_token = ? WHERE id = ?",
            (token, user_id)
        )
        conn.commit()
        return token
    except Exception as e:
        print(f"[user_db] reset_user_password error: {e}")
        return None
    finally:
        conn.close()


def get_user_by_reset_token(token):
    """비밀번호 재설정 토큰으로 사용자를 조회합니다."""
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT * FROM user_accounts WHERE reset_token = ? AND is_active = 1",
            (token,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_password(user_id, new_password):
    """비밀번호를 변경하고 재설정 토큰을 소비합니다."""
    conn = get_db()
    try:
        conn.execute(
            "UPDATE user_accounts SET password_hash = ?, reset_token = NULL WHERE id = ?",
            (_hash(new_password), user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[user_db] update_password error: {e}")
        return False
    finally:
        conn.close()


def toggle_user_active(user_id, is_active):
    """회원 활성/비활성 전환."""
    conn = get_db()
    try:
        conn.execute("UPDATE user_accounts SET is_active = ? WHERE id = ?", (is_active, user_id))
        conn.commit()
        return True
    finally:
        conn.close()
