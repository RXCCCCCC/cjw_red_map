# 程家湾红色资源数字地图

> 江西省上饶市程家湾红色资源数字化展示平台——前后端 + 3D Tiles 一体化项目

## 技术栈

| 层      | 技术                                                                    |
| ------- | ----------------------------------------------------------------------- |
| 前端    | Vue 3 (Composition API) · Vite · Pinia · Tailwind CSS · Vant · CesiumJS |
| 后端    | Flask · SQLAlchemy · PyMySQL                                            |
| 数据库  | **MySQL** >= 5.7（必须）                                                |
| 3D 数据 | CesiumJS 3D Tiles（存放于 `backend/static/tiles/`）                     |

---

## 项目目录结构

```
cjw_red_map/
├── backend/                        # Flask 后端
│   ├── app/
│   │   ├── __init__.py             # App factory：创建 Flask 实例、注册蓝图
│   │   ├── config.py               # 数据库与路径配置（⚠️ 需修改 MySQL 密码）
│   │   ├── models.py               # ORM 模型：Site / Media / AudioGuide
│   │   ├── seeds.py                # 初始种子数据（由 sync_seeds.py 自动生成）
│   │   ├── utils.py                # 通用工具函数
│   │   └── routes/
│   │       ├── site.py             # /api/sites      地标 CRUD
│   │       ├── media.py            # /api/media       媒体 CRUD
│   │       ├── audio_guide.py      # /api/audio-guides 语音导览
│   │       ├── tiles.py            # /tiles/*         3D Tiles 静态代理
│   │       └── upload.py           # /api/upload      文件上传
│   ├── static/tiles/               # 3D Tiles 数据（较大，建议 Git LFS 或对象存储）
│   ├── uploads/                    # 用户上传的图片/媒体文件
│   ├── init_db.py                  # 初始化/重建数据库（⚠️ 会清空数据，谨慎使用）
│   ├── run.py                      # Flask 开发服务器启动入口
│   ├── sync_seeds.py               # 从本地 DB 导出并重写 seeds.py
│   ├── export_db.py                # 生成 SQL 备份（可选）
│   └── requirements.txt            # Python 依赖
├── frontend/                       # Vue 3 前端
│   ├── src/
│   │   ├── main.js                 # 入口
│   │   ├── App.vue                 # 根组件
│   │   ├── api/index.js            # Axios 封装
│   │   ├── components/
│   │   │   ├── CesiumViewer.vue    # 3D 场景（Cesium + 地标渲染）
│   │   │   ├── MapContainer.vue    # Leaflet 平面地图（备用）
│   │   │   ├── AudioPlayer.vue     # 语音导览播放器
│   │   │   ├── NavBar.vue          # 导航栏
│   │   │   ├── SiteCard.vue        # 地标缩略卡片
│   │   │   └── SitePopup.vue       # 地标弹窗
│   │   ├── views/
│   │   │   ├── HomeView.vue        # 首页
│   │   │   ├── MapView.vue         # 地图浏览
│   │   │   ├── SiteDetail.vue      # 地标详情
│   │   │   ├── Model3DView.vue     # 3D 模型展示
│   │   │   └── AboutView.vue       # 关于页
│   │   ├── stores/                 # Pinia 状态管理
│   │   ├── router/                 # Vue Router
│   │   └── styles/                 # 全局样式
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── docs/                           # 开发文档
│   ├── 开发日志.md
│   ├── 开发路线规划.md
│   └── 程家湾地图开发随记.md
└── README.md
```

---

## 快速启动（本地开发）

### 前置要求

- **Node.js** >= 16（推荐 18+）
- **Python** >= 3.8
- **MySQL** >= 5.7 或 MariaDB >= 10.3（**必须**，本项目不使用 SQLite）

### 1. 配置 MySQL

确保 MySQL 服务已启动，然后配置数据库连接：

**方式一：使用 .env 文件（推荐）**

```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，修改 DB_PASSWORD 为你的 MySQL 密码
```

`.env` 文件示例：

```bash
# backend/.env
SECRET_KEY=cjw-red-map-secret-2026

DB_USER=root
DB_PASSWORD=你的MySQL密码        # ← 填写你的实际密码
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=cjw_red_map
```

> ⚠️ **重要**：`.env` 文件已被 `.gitignore` 忽略，不会提交到 Git，确保密码安全。

**方式二：通过系统环境变量设置（适用于生产环境）**

```powershell
# Windows PowerShell
$env:DB_PASSWORD = "你的MySQL密码"
```

```bash
# Linux / macOS
export DB_PASSWORD="你的MySQL密码"
```

### 2. 启动后端

```bash
cd backend
python -m venv .venv
# Windows：
.\venv\Scripts\Activate.ps1
# Linux/macOS：
# source .venv/bin/activate

pip install -r requirements.txt
python init_db.py          # ⚠️ 首次运行：创建数据库 + 表 + 种子数据（会清空已有数据！）
python run.py              # Flask 启动于 http://127.0.0.1:5000
```

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
# 打开浏览器访问 http://localhost:5173
```

### 4. 验证

- 浏览器打开 http://localhost:5173 ，应可看到 3D 地图与 8 个红色地标
- 后端 API 验证：访问 http://127.0.0.1:5000/api/sites ，应返回 `{"code": 0, "data": [...]}`

---

## 数据库管理与数据同步

### 初始化数据库

```bash
cd backend
python init_db.py
```

该脚本会：创建 `cjw_red_map` 数据库（如不存在）→ 清空所有表 → 重建表结构 → 插入 `seeds.py` 中的种子数据。

> ⚠️ **警告**：`init_db.py` 会执行 `db.drop_all()`，运行前请备份重要数据！

### 数据同步流程（确保多人一致）

当你在本地通过编辑界面修改了地标坐标、描述或上传了图片后，这些改动只存在于你的本地 MySQL 和 `uploads/` 目录。为了让他人部署时看到相同数据，请执行：

```bash
cd backend
# 第 1 步：从本地 MySQL 自动导出并更新 seeds.py
python sync_seeds.py

# 第 2 步：提交到 Git
git add app/seeds.py
git add ../backend/uploads/        # 如果有新增/修改的图片
git commit -m "sync: 更新地标数据与媒体"
git push
```

### SQL 备份（可选）

```bash
cd backend
python export_db.py     # 在当前目录生成 database_backup.sql
```

---

## 他人从 GitHub 克隆后能否看到完全一样的效果？

**结论：可以做到一致，但需要满足以下条件。**

| 条件                    | 说明                                                                                                  |
| ----------------------- | ----------------------------------------------------------------------------------------------------- |
| ✅ 地标位置、名称、描述 | 只要你在推送前运行了 `python sync_seeds.py` 并提交了 `seeds.py`，他人运行 `init_db.py` 后数据完全一致 |
| ✅ 图片/媒体            | 只要 `backend/uploads/` 目录已提交到 Git（或媒体已上传到对象存储），图片可正常加载                    |
| ✅ 3D Tiles             | 已包含在 `backend/static/tiles/` 中，克隆后即可使用                                                   |
| ⚠️ MySQL 密码           | 每台机器的 MySQL 密码不同，他人需创建 `.env` 文件并配置 `DB_PASSWORD`（见"快速启动"章节）             |
| ⚠️ Cesium Token         | 如果 Cesium Ion Token 过期或无效，3D 场景可能无法加载地球底图（需配置自己的 Token）                   |

**总结**：只要你每次修改数据后执行 `sync_seeds.py` → 提交 `seeds.py` + `uploads/` → 推送，他人克隆后只需：

1. 创建 `.env` 文件并配置 MySQL 密码（`cp .env.example .env`，然后修改 `DB_PASSWORD`）
2. 运行 `python init_db.py`
3. 启动前后端

即可看到与你完全相同的地标位置、图片和 3D 场景。

---

## .gitignore 建议

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/

# Node.js
node_modules/
dist/

# 环境变量（不要提交密码）
.env

# 数据库备份
*.sql

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

> 注意：`backend/uploads/` 目前允许提交（演示用途）。生产环境建议迁移到对象存储（OSS/COS），详见 `docs/图片同步方案.md`。

---

## API 概览

| 方法   | 路径                  | 说明                             |
| ------ | --------------------- | -------------------------------- |
| GET    | `/api/sites`          | 获取所有地标                     |
| GET    | `/api/sites/:id`      | 获取单个地标详情（含媒体与导览） |
| POST   | `/api/sites`          | 新增地标                         |
| PUT    | `/api/sites/:id`      | 更新地标                         |
| DELETE | `/api/sites/:id`      | 删除地标                         |
| GET    | `/api/media/:site_id` | 获取某地标的媒体列表             |
| POST   | `/api/upload`         | 上传文件                         |
| GET    | `/uploads/:filename`  | 访问已上传的媒体文件             |
| GET    | `/tiles/*`            | 3D Tiles 静态代理                |

所有 API 返回格式：`{"code": 0, "data": ...}` 或 `{"code": 0, "msg": "..."}`。

---

## 生产环境建议

- **数据库**：使用云 MySQL（阿里云 RDS / 腾讯云 CDB），通过环境变量配置连接
- **敏感信息**：密码、Token 等通过环境变量管理，不硬编码在代码中
- **媒体文件**：迁移到对象存储（OSS/COS/S3），避免 Git 仓库膨胀
- **HTTPS**：使用 Nginx 反向代理 + Let's Encrypt 证书
- **进程管理**：使用 Gunicorn + Supervisor 或 Docker 部署 Flask

---

## 文档

- [开发日志](docs/开发日志.md) — 每次功能变更的详细记录
- [开发路线规划](docs/开发路线规划.md) — 项目规划与里程碑
- [开发随记](docs/程家湾地图开发随记.md) — 技术探索笔记
- [图片同步方案](docs/图片同步方案.md) — 媒体文件分发策略对比
