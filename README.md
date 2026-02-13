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
### 后端
1. 进入后端目录并创建数据库（首次运行）：

```bash
cd backend
# 修改 backend/app/config.py 中的 DB_* 配置为你的 MySQL 凭证（或设置环境变量）
python init_db.py
```

2. 启动后端：

```bash
python run.py
# Flask 默认监听 127.0.0.1:5000
```

### 前端
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```