import os
from flask import Blueprint, send_from_directory, current_app

tiles_bp = Blueprint('tiles', __name__)


@tiles_bp.route('/tiles/<path:filename>')
def serve_tiles(filename):
    """静态代理 3D Tiles 文件，支持跨域"""
    tiles_dir = os.path.abspath(current_app.config['TILES_DIR'])
    response = send_from_directory(tiles_dir, filename)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = _guess_content_type(filename)
    return response


def _guess_content_type(filename):
    """根据扩展名猜测 Content-Type"""
    if filename.endswith('.json'):
        return 'application/json'
    elif filename.endswith('.glb'):
        return 'model/gltf-binary'
    elif filename.endswith('.gltf'):
        return 'model/gltf+json'
    elif filename.endswith('.b3dm'):
        return 'application/octet-stream'
    elif filename.endswith('.pnts'):
        return 'application/octet-stream'
    return 'application/octet-stream'
