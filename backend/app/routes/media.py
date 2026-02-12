from flask import Blueprint, request, jsonify
from app import db
from app.models import Media

media_bp = Blueprint('media', __name__)


@media_bp.route('/sites/<int:site_id>/media', methods=['GET'])
def get_site_media(site_id):
    """获取遗址的所有媒体资源"""
    items = Media.query.filter_by(site_id=site_id).order_by(Media.sort_order).all()
    return jsonify({'code': 0, 'data': [m.to_dict() for m in items]})


@media_bp.route('/media', methods=['POST'])
def create_media():
    """新增媒体资源"""
    body = request.get_json()
    media = Media(
        site_id=body['site_id'],
        type=body['type'],
        url=body['url'],
        title=body.get('title', ''),
        description=body.get('description', ''),
        sort_order=body.get('sort_order', 0),
    )
    db.session.add(media)
    db.session.commit()
    return jsonify({'code': 0, 'data': media.to_dict()}), 201


@media_bp.route('/media/<int:media_id>', methods=['DELETE'])
def delete_media(media_id):
    """删除媒体资源"""
    media = Media.query.get_or_404(media_id)
    db.session.delete(media)
    db.session.commit()
    return jsonify({'code': 0, 'msg': '已删除'})
