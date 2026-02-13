"""文件上传路由：处理媒体文件（图片/音频/视频）的上传并返回可访问 URL"""
import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {
    'image': {'jpg', 'jpeg', 'png', 'gif', 'webp'},
    'audio': {'mp3', 'ogg', 'wav', 'm4a', 'flac'},
    'video': {'mp4', 'webm', 'mov'},
}
ALL_ALLOWED = set()
for exts in ALLOWED_EXTENSIONS.values():
    ALL_ALLOWED |= exts


def _allowed_file(filename):
    """检查文件扩展名是否在白名单中"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALL_ALLOWED


def _detect_type(filename):
    """根据扩展名推断媒体类型"""
    ext = filename.rsplit('.', 1)[1].lower()
    for media_type, exts in ALLOWED_EXTENSIONS.items():
        if ext in exts:
            return media_type
    return 'image'


def _ensure_upload_dir(app):
    """确保上传目录存在"""
    upload_dir = app.config.get('UPLOAD_DIR', os.path.join(app.root_path, '..', 'uploads'))
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir


@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    上传单个文件
    - form-data 字段: file (必选), title (可选)
    - 返回: { code: 0, data: { url, type, filename, title } }
    """
    if 'file' not in request.files:
        return jsonify({'code': 1, 'msg': '缺少文件字段 file'}), 400

    f = request.files['file']
    if f.filename == '':
        return jsonify({'code': 1, 'msg': '未选择文件'}), 400

    if not _allowed_file(f.filename):
        return jsonify({'code': 1, 'msg': f'不支持的文件类型，允许: {", ".join(sorted(ALL_ALLOWED))}'}), 400

    upload_dir = _ensure_upload_dir(current_app)

    # 使用 UUID 避免文件名冲突，保留原始扩展名
    ext = f.filename.rsplit('.', 1)[1].lower()
    safe_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    save_path = os.path.join(upload_dir, safe_name)
    f.save(save_path)

    media_type = _detect_type(f.filename)
    title = request.form.get('title', f.filename)

    # 返回相对 URL，前端通过 /uploads/<filename> 访问
    url = f'/uploads/{safe_name}'

    return jsonify({
        'code': 0,
        'data': {
            'url': url,
            'type': media_type,
            'filename': safe_name,
            'original_name': f.filename,
            'title': title,
        }
    }), 201


@upload_bp.route('/upload/batch', methods=['POST'])
def upload_files():
    """
    批量上传文件
    - form-data 字段: files (多个), title (可选)
    - 返回: { code: 0, data: [...] }
    """
    files = request.files.getlist('files')
    if not files:
        return jsonify({'code': 1, 'msg': '缺少文件字段 files'}), 400

    upload_dir = _ensure_upload_dir(current_app)
    results = []

    for f in files:
        if f.filename == '' or not _allowed_file(f.filename):
            continue
        ext = f.filename.rsplit('.', 1)[1].lower()
        safe_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
        save_path = os.path.join(upload_dir, safe_name)
        f.save(save_path)
        results.append({
            'url': f'/uploads/{safe_name}',
            'type': _detect_type(f.filename),
            'filename': safe_name,
            'original_name': f.filename,
        })

    return jsonify({'code': 0, 'data': results}), 201
