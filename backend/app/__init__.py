from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Flask 应用工厂"""
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # 跨域
    CORS(app, resources={r"/api/*": {"origins": "*"}, r"/tiles/*": {"origins": "*"}})

    # 数据库
    db.init_app(app)

    # 注册蓝图
    from app.routes.site import site_bp
    from app.routes.media import media_bp
    from app.routes.audio_guide import audio_guide_bp
    from app.routes.tiles import tiles_bp

    app.register_blueprint(site_bp, url_prefix='/api')
    app.register_blueprint(media_bp, url_prefix='/api')
    app.register_blueprint(audio_guide_bp, url_prefix='/api')
    app.register_blueprint(tiles_bp)

    return app
