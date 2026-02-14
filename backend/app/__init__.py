from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Flask 应用工厂"""
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # 跨域（包含上传和 uploads 静态目录）
    CORS(app, resources={
        r"/api/*": {"origins": "*"},
        r"/tiles/*": {"origins": "*"},
        r"/uploads/*": {"origins": "*"},
    })

    # 数据库
    db.init_app(app)

    # 注册蓝图
    from app.routes.site import site_bp
    from app.routes.media import media_bp
    from app.routes.audio_guide import audio_guide_bp
    from app.routes.tiles import tiles_bp
    from app.routes.upload import upload_bp
    from app.routes.route_paths import route_paths_bp

    app.register_blueprint(site_bp, url_prefix='/api')
    app.register_blueprint(media_bp, url_prefix='/api')
    app.register_blueprint(audio_guide_bp, url_prefix='/api')
    app.register_blueprint(tiles_bp)
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(route_paths_bp, url_prefix='/api')

    # 提供 /uploads/<filename> 静态访问（上传的媒体文件）
    import os
    from flask import send_from_directory
    upload_dir = app.config.get('UPLOAD_DIR', os.path.join(app.root_path, '..', 'uploads'))
    os.makedirs(upload_dir, exist_ok=True)

    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(upload_dir, filename)

    return app
