# 程家湾红色资源数字地图

这是程家湾红色资源数字地图项目源码（前后端 + 3D Tiles 数据）。

## 概览
- 前端：Vue 3 + Vite + Pinia + Tailwind + Vant，CesiumJS 加载 3D Tiles
- 后端：Flask + SQLAlchemy (MySQL)，提供 REST API 与 3D Tiles 静态代理
- 数据：`backend/static/tiles/`（本地存放 3D Tiles），建议使用外部对象存储或 Git LFS

## 目录结构（简化）
```
cjw_red_map/
├── backend/                 # Flask 后端
│   ├── app/
│   ├── static/tiles/        # 3D Tiles
│   ├── requirements.txt
│   └── run.py
├── frontend/                # Vue 前端
├── 开发路线规划.md
└── 程家湾地图开发随记.md
```

## 快速启动（开发）

### 前置要求
- **Node.js** >= 16.x（推荐 18.x）
- **Python** >= 3.8
- **MySQL** >= 5.7 或 MariaDB >= 10.3

### 后端部署

#### 1. 配置数据库连接
编辑 `backend/app/config.py` 或设置环境变量：

```python
# backend/app/config.py（可选：直接修改默认值）
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')  # 修改为你的密码
DB_NAME = os.getenv('DB_NAME', 'cjw_red_map')
```

或通过环境变量（推荐生产环境）：

```bash
# Windows PowerShell
$env:DB_PASSWORD="your_password"
$env:DB_HOST="localhost"

# Linux/Mac
export DB_PASSWORD="your_password"
export DB_HOST="localhost"
```

#### 2. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

#### 3. 初始化数据库（首次部署）
```bash
python init_db.py
```

该脚本会自动：
- 创建数据库（如不存在）
- 创建所有表结构（Sites, Media, AudioGuides）
- 插入 7 个初始红色地标数据

**⚠️ 注意**：`init_db.py` 会清空现有数据！如需保留数据，请先备份。

#### 4. 启动后端
```bash
python run.py
# Flask 默认监听 http://127.0.0.1:5000
# API 文档：http://127.0.0.1:5000/api/sites
```

### 前端部署
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

---

## 数据库管理

### 方式一：使用 init_db.py（推荐）
**优点**：跨平台、不依赖 mysqldump、数据结构清晰可维护

```bash
cd backend
python init_db.py  # 重建数据库并插入种子数据
```

所有初始地标数据存放在 `backend/app/seeds.py`，可直接编辑后运行 `init_db.py` 同步。

### 方式二：SQL 导出/导入（可选）
如需导出当前数据库为 SQL 文件（用于分享或迁移）：

```bash
cd backend
python export_db.py  # 生成 database_backup.sql
```

他人导入 SQL 文件：

```bash
# 1. 创建空数据库
mysql -u root -p -e "CREATE DATABASE cjw_red_map CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. 导入数据
mysql -u root -p cjw_red_map < database_backup.sql
```

---

## 项目部署到 GitHub

### 需要上传的内容
✅ **代码**：`backend/`、`frontend/`（全部代码）  
✅ **数据库初始化脚本**：`backend/init_db.py`、`backend/app/seeds.py`  
✅ **3D Tiles**：`backend/static/tiles/`（如文件较大，建议使用 Git LFS 或改用对象存储）  
✅ **文档**：`README.md`、`docs/`

❌ **不要上传**：
- `.env`（环境变量配置文件，包含密码）
- `backend/__pycache__/`、`frontend/node_modules/`
- `database_backup.sql`（如果包含敏感数据）
- `backend/uploads/`（用户上传的媒体文件，建议用对象存储）

### 配置 .gitignore

在项目根目录创建 `.gitignore`：

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
venv/
.venv/

# Node.js
node_modules/
dist/
*.local

# 环境变量和敏感配置
.env
*.env
backend/app/config_local.py

# 数据库备份
*.sql
database_backup*.sql

# 用户上传文件
backend/uploads/
!backend/uploads/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# 操作系统
.DS_Store
Thumbs.db
```

### 部署流程

1. **提交代码到 GitHub**

```bash
git init
git add .
git commit -m "初始提交：程家湾红色地图项目"
git branch -M main
git remote add origin https://github.com/your-username/cjw-red-map.git
git push -u origin main
```

2. **他人克隆并部署**

```bash
# 克隆仓库
git clone https://github.com/your-username/cjw-red-map.git
cd cjw-red-map

# 后端部署
cd backend
pip install -r requirements.txt
# 修改 config.py 中的数据库密码
python init_db.py  # 自动创建数据库和初始数据
python run.py

# 前端部署（新开终端）
cd ../frontend
npm install
npm run dev
```

---

## 生产环境建议

- **数据库**：使用云数据库（如阿里云 RDS、腾讯云 CDB）或自建 MySQL 并定期备份
- **敏感配置**：通过环境变量管理密码，不要硬编码在 `config.py`
- **3D Tiles**：使用对象存储（如 OSS、COS）托管大文件，避免 Git 仓库过大
- **HTTPS**：生产环境必须启用 HTTPS（使用 Nginx + Let's Encrypt）
- **进程管理**：使用 Gunicorn + Supervisor 或 Docker 部署后端