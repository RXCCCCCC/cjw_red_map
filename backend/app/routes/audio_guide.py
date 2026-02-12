from flask import Blueprint, request, jsonify
from app import db
from app.models import AudioGuide

audio_guide_bp = Blueprint('audio_guide', __name__)


@audio_guide_bp.route('/sites/<int:site_id>/audio-guides', methods=['GET'])
def get_site_audio_guides(site_id):
    """获取遗址的语音导览列表"""
    items = AudioGuide.query.filter_by(site_id=site_id).order_by(AudioGuide.sort_order).all()
    return jsonify({'code': 0, 'data': [a.to_dict() for a in items]})


@audio_guide_bp.route('/audio-guides', methods=['POST'])
def create_audio_guide():
    """新增语音导览"""
    body = request.get_json()
    guide = AudioGuide(
        site_id=body['site_id'],
        title=body['title'],
        audio_url=body['audio_url'],
        transcript=body.get('transcript', ''),
        duration=body.get('duration', 0),
        sort_order=body.get('sort_order', 0),
    )
    db.session.add(guide)
    db.session.commit()
    return jsonify({'code': 0, 'data': guide.to_dict()}), 201


@audio_guide_bp.route('/audio-guides/<int:guide_id>', methods=['DELETE'])
def delete_audio_guide(guide_id):
    """删除语音导览"""
    guide = AudioGuide.query.get_or_404(guide_id)
    db.session.delete(guide)
    db.session.commit()
    return jsonify({'code': 0, 'msg': '已删除'})
