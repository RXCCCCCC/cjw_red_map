"""
配置模板 - 部署时请复制此文件为 config.py 并修改敏感信息

使用方法：
1. 将此文件复制为 config.py：
   cp config.example.py config.py

2. 修改其中的数据库密码等敏感信息

3. config.py 已被 .gitignore 忽略，不会提交到版本库
"""
import os


class Config:
    """Flask 应用配置"""
    
    # ========== 数据库配置 ==========
    # 请修改以下配置为你的 MySQL 实际信息
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'YOUR_PASSWORD_HERE')  # ⚠️ 修改此处！
    DB_NAME = os.getenv('DB_NAME', 'cjw_red_map')
    
    # SQLAlchemy 连接字符串
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        '?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # 设为 True 可查看 SQL 日志
    
    # ========== Flask 配置 ==========
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')  # ⚠️ 生产环境必须修改
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # ========== 文件上传配置 ==========
    UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4', 'avi'}
    
    # ========== 3D Tiles 配置 ==========
    TILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'tiles')
    
    # ========== CORS 配置 ==========
    # 生产环境请修改为实际前端域名
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')


# 生产环境配置示例
class ProductionConfig(Config):
    """生产环境配置（通过环境变量覆盖敏感信息）"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    # 生产环境必须通过环境变量设置以下内容：
    # - DB_PASSWORD
    # - SECRET_KEY
    # - CORS_ORIGINS


# 开发环境配置
class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # 打印 SQL


# 根据环境变量选择配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': Config
}
