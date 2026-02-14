from flask import Blueprint, request, jsonify
from app import db
from app.models import Route
import json

route_paths_bp = Blueprint('route_paths', __name__)

@route_paths_bp.route('/routes', methods=['GET'])
def get_routes():
    routes = Route.query.order_by(Route.created_at.desc()).all()
    return jsonify({'code': 0, 'data': [r.to_dict() for r in routes]})

@route_paths_bp.route('/routes', methods=['POST'])
def create_route():
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'msg': 'No data provided'}), 400
    
    name = data.get('name')
    points = data.get('points')
    
    if not name or not points:
        return jsonify({'code': 400, 'msg': 'Missing name or points'}), 400
        
    try:
        route = Route(
            name=name,
            description=data.get('description', ''),
            points=points,
            line_color=data.get('line_color', '#FF0000'),
            width=data.get('width', 5),
            is_visible=data.get('is_visible', True)
        )
        db.session.add(route)
        db.session.commit()
        return jsonify({'code': 0, 'msg': 'Route created', 'data': route.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': str(e)}), 500

@route_paths_bp.route('/routes/<int:id>', methods=['DELETE'])
def delete_route(id):
    route = Route.query.get_or_404(id)
    try:
        db.session.delete(route)
        db.session.commit()
        return jsonify({'code': 0, 'msg': 'Route deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': str(e)}), 500
