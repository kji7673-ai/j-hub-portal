"""
J-Hub 교육 플랫폼 — Flask Blueprint (API 엔드포인트)
학습 진도 및 퀴즈 점수를 서버 DB에 저장/조회하는 REST API를 제공합니다.
"""
from flask import Blueprint, jsonify, request, session
from functools import wraps
import hashlib
import unicodedata

from edu_db import (
    save_progress,
    get_user_progress,
    save_quiz_score,
    get_user_quiz_scores,
    get_admin_overview
)

edu_bp = Blueprint('edu', __name__)


def _get_user_hash():
    """현재 세션의 사용자명을 SHA-256 해시로 변환하여 반환합니다.
    DB에는 사용자 실명 대신 해시만 저장하여 개인정보를 보호합니다.
    """
    user_name = session.get('user_name', '')
    if not user_name:
        return None
    normalized = unicodedata.normalize('NFC', user_name.strip())
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def login_required(f):
    """교육 API 전용 인증 데코레이터"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({"success": False, "message": "로그인이 필요합니다."}), 401
        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════
# API Endpoints
# ═══════════════════════════════════════════════

@edu_bp.route('/api/edu/progress', methods=['GET'])
@login_required
def api_get_progress():
    """사용자의 전체 완독 현황을 반환합니다.
    Response: {"success": true, "progress": {doc_id: timestamp, ...}}
    """
    user_hash = _get_user_hash()
    if not user_hash:
        return jsonify({"success": False, "message": "사용자 식별 실패"}), 400

    progress = get_user_progress(user_hash)
    # dict keys를 문자열로 변환 (JSON 호환)
    progress_str = {str(k): v for k, v in progress.items()}
    return jsonify({"success": True, "progress": progress_str})


@edu_bp.route('/api/edu/progress', methods=['POST'])
@login_required
def api_save_progress():
    """문서 완독을 기록합니다.
    Request: {"doc_id": 5}
    """
    user_hash = _get_user_hash()
    if not user_hash:
        return jsonify({"success": False, "message": "사용자 식별 실패"}), 400

    data = request.get_json()
    if not data or 'doc_id' not in data:
        return jsonify({"success": False, "message": "doc_id가 필요합니다."}), 400

    doc_id = int(data['doc_id'])
    result = save_progress(user_hash, doc_id)

    if result:
        return jsonify({"success": True, "message": f"문서 {doc_id} 완독 기록 완료"})
    return jsonify({"success": False, "message": "저장 실패"}), 500


@edu_bp.route('/api/edu/quiz', methods=['POST'])
@login_required
def api_save_quiz():
    """퀴즈 점수를 저장합니다.
    Request: {"doc_id": 11, "score": 80}
    """
    user_hash = _get_user_hash()
    if not user_hash:
        return jsonify({"success": False, "message": "사용자 식별 실패"}), 400

    data = request.get_json()
    if not data or 'doc_id' not in data or 'score' not in data:
        return jsonify({"success": False, "message": "doc_id와 score가 필요합니다."}), 400

    doc_id = int(data['doc_id'])
    score = int(data['score'])

    if not (0 <= score <= 100):
        return jsonify({"success": False, "message": "점수는 0~100 범위여야 합니다."}), 400

    result = save_quiz_score(user_hash, doc_id, score)

    if result:
        return jsonify({"success": True, "message": f"문서 {doc_id} 퀴즈 점수 {score}점 저장"})
    return jsonify({"success": False, "message": "저장 실패"}), 500


@edu_bp.route('/api/edu/analytics', methods=['GET'])
@login_required
def api_get_analytics():
    """사용자의 학습 현황 종합 통계를 반환합니다.
    Response: {
        "success": true,
        "progress": {doc_id: timestamp},
        "quiz_scores": {doc_id: score},
        "completed_count": 5,
        "quiz_average": 85
    }
    """
    user_hash = _get_user_hash()
    if not user_hash:
        return jsonify({"success": False, "message": "사용자 식별 실패"}), 400

    progress = get_user_progress(user_hash)
    quiz_scores = get_user_quiz_scores(user_hash)

    # 평균 퀴즈 점수 계산
    scores = list(quiz_scores.values())
    quiz_avg = round(sum(scores) / len(scores)) if scores else 0

    return jsonify({
        "success": True,
        "progress": {str(k): v for k, v in progress.items()},
        "quiz_scores": {str(k): v for k, v in quiz_scores.items()},
        "completed_count": len(progress),
        "quiz_average": quiz_avg
    })


@edu_bp.route('/api/edu/admin/overview', methods=['GET'])
@login_required
def api_admin_overview():
    """관리자 전용: 전체 임직원 교육 현황을 반환합니다.
    대표이사(is_master) 권한이 필요합니다.
    """
    if not session.get('is_master'):
        return jsonify({"success": False, "message": "대표이사 권한이 필요합니다."}), 403

    overview = get_admin_overview()
    return jsonify({"success": True, **overview})
