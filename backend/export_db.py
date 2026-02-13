"""数据库导出脚本：生成 SQL 文件供他人导入"""
import subprocess
import os
from datetime import datetime
from app.config import Config


def export_database():
    """使用 mysqldump 导出数据库到 SQL 文件"""
    output_file = os.path.join('..', 'database_backup.sql')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_with_time = os.path.join('..', f'database_backup_{timestamp}.sql')
    
    # mysqldump 命令
    cmd = [
        'mysqldump',
        '-h', Config.DB_HOST,
        '-P', str(Config.DB_PORT),
        '-u', Config.DB_USER,
        f'-p{Config.DB_PASSWORD}',
        '--default-character-set=utf8mb4',
        '--single-transaction',
        '--routines',
        '--triggers',
        '--events',
        Config.DB_NAME
    ]
    
    print(f'🚀 开始导出数据库 {Config.DB_NAME}...')
    
    try:
        # 导出到文件
        with open(output_file, 'w', encoding='utf8') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f'❌ 导出失败: {result.stderr}')
                return False
        
        # 同时生成带时间戳的备份
        import shutil
        shutil.copy(output_file, output_with_time)
        
        file_size = os.path.getsize(output_file) / 1024  # KB
        print(f'✅ 数据库已导出到: {output_file} ({file_size:.1f} KB)')
        print(f'✅ 时间戳备份: {output_with_time}')
        print('\n📋 使用说明：')
        print('   他人可通过以下命令导入数据库：')
        print(f'   mysql -u root -p {Config.DB_NAME} < database_backup.sql')
        return True
    
    except FileNotFoundError:
        print('❌ 错误：未找到 mysqldump 命令')
        print('   请确保 MySQL 已安装并添加到系统 PATH 环境变量')
        print('   或者使用 init_db.py 来重建数据库（推荐）')
        return False
    except Exception as e:
        print(f'❌ 导出过程出错: {e}')
        return False


if __name__ == '__main__':
    print('='*60)
    print('程家湾红色地图 - 数据库导出工具')
    print('='*60)
    print(f'数据库: {Config.DB_NAME}@{Config.DB_HOST}:{Config.DB_PORT}')
    print('')
    
    export_database()
    
    print('\n💡 提示：')
    print('   推荐使用 init_db.py + seeds.py 方式分发数据库，')
    print('   可跨平台且不依赖 mysqldump 工具。')
