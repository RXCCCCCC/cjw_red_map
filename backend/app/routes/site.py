from flask import Blueprint, request, jsonify
from app import db
from app.models import Site

site_bp = Blueprint('site', __name__)


@site_bp.route('/sites', methods=['GET'])
def get_sites():
    """获取全部遗址列表"""
    sites = Site.query.order_by(Site.sort_order).all()
    return jsonify({'code': 0, 'data': [s.to_dict() for s in sites]})


@site_bp.route('/sites/<int:site_id>', methods=['GET'])
def get_site(site_id):
    """获取单个遗址详情"""
    site = Site.query.get_or_404(site_id)
    data = site.to_dict()
    data['media'] = [m.to_dict() for m in site.media.order_by('sort_order')]
    data['audio_guides'] = [a.to_dict() for a in site.audio_guides.order_by('sort_order')]
    return jsonify({'code': 0, 'data': data})


@site_bp.route('/sites', methods=['POST'])
def create_site():
    """新增遗址"""
    body = request.get_json()
    site = Site(
        name=body['name'],
        description=body.get('description', ''),
        longitude=body['longitude'],
        latitude=body['latitude'],
        category=body.get('category', ''),
        icon=body.get('icon', ''),
        cover_image=body.get('cover_image', ''),
        sort_order=body.get('sort_order', 0),
    )
    db.session.add(site)
    db.session.commit()
    return jsonify({'code': 0, 'data': site.to_dict()}), 201


@site_bp.route('/sites/<int:site_id>', methods=['PUT'])
def update_site(site_id):
    """更新遗址"""
    site = Site.query.get_or_404(site_id)
    body = request.get_json()
    for field in ['name', 'description', 'longitude', 'latitude', 'category', 'icon', 'cover_image', 'sort_order']:
        if field in body:
            setattr(site, field, body[field])
    db.session.commit()
    return jsonify({'code': 0, 'data': site.to_dict()})


@site_bp.route('/sites/<int:site_id>', methods=['DELETE'])
def delete_site(site_id):
    """删除遗址"""
    site = Site.query.get_or_404(site_id)
    db.session.delete(site)
    db.session.commit()
    return jsonify({'code': 0, 'msg': '已删除'})
