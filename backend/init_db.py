"""数据库初始化脚本：建表 + 种子数据"""
import pymysql
from app import create_app, db
from app.config import Config
from app.seeds import seed_data


def ensure_database():
    """如果数据库不存在，则创建"""
    conn = pymysql.connect(
        host=Config.DB_HOST,
        port=int(Config.DB_PORT),
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        charset='utf8mb4',
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.commit()
    cursor.close()
    conn.close()
    print(f'✅ 数据库 {Config.DB_NAME} 已就绪')


if __name__ == '__main__':
    ensure_database()
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print('✅ 数据表已创建')
        seed_data()
        print('✅ 初始化完成')
