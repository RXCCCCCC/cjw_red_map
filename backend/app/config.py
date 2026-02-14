import os
from pathlib import Path

# 加载 .env 文件（如果存在）
try:
    from dotenv import load_dotenv
    # 从 backend/.env 加载环境变量
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    # 如果未安装 python-dotenv，提示用户安装
    print("⚠️  未安装 python-dotenv，请运行：pip install python-dotenv")
    print("⚠️  或通过系统环境变量配置数据库连接")


class Config:
    """Flask 应用配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cjw-red-map-secret-2026')

    # MySQL 数据库配置（从环境变量读取，默认值仅作占位）
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')  # ⚠️ 必须在 .env 中配置
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'cjw_red_map')

    # 检查必需的环境变量
    if not DB_PASSWORD:
        raise ValueError(
            "❌ 数据库密码未配置！\n"
            "请在 backend/.env 文件中设置 DB_PASSWORD=你的MySQL密码\n"
            "或通过环境变量设置：export DB_PASSWORD=你的密码"
        )

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        "?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 3D Tiles 数据目录 (放置在 backend/static/tiles)
    TILES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'tiles')

    # 上传文件目录
    UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
