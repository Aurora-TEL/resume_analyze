# Docker 开发环境配置文档

## 1. 文档说明

### 1.1 文档目的

本文档用于说明简历分析系统后端开发环境的 Docker 配置流程，包括项目目录创建、后端基础服务初始化、依赖安装、环境变量配置、Docker Compose 启动和基础验证。

本文档主要面向：

- 后端开发人员
- 部署运维人员
- 项目维护人员
- 初次搭建开发环境的开发者

### 1.2 配置目标

完成本文档步骤后，开发环境应满足以下目标：

1. 可以通过 Docker 启动 FastAPI 后端服务。
2. 可以通过 Docker 启动 PostgreSQL 数据库服务。
3. 后端服务可以通过环境变量读取配置。
4. 后端健康检查接口可以正常访问。
5. FastAPI Swagger API 文档可以正常访问。
6. 项目具备后续接入 SQLAlchemy、Alembic、用户认证和业务接口的基础结构。

---

## 2. 前置条件

在开始之前，请确保本机已经安装：

| 工具 | 说明 |
|---|---|
| Docker | 用于运行容器 |
| Docker Compose Plugin | 用于编排多个服务 |
| Git | 可选，用于代码版本管理 |
| 代码编辑器 | 推荐 VS Code 或 PyCharm |

检查 Docker 是否安装成功：

```bash
docker --version
docker compose version
```

如果可以正常输出版本号，说明 Docker 环境可用。

---

## 3. 推荐项目目录结构

项目根目录建议命名为：

```text
resume-analyzer
```

完成本阶段配置后，目录结构如下：

```text
resume-analyzer/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── storage/
│   └── resumes/
│       └── .gitkeep
├── docker-compose.yml
├── .env.example
├── .env.dev
└── .gitignore
```

目录说明：

| 路径 | 说明 |
|---|---|
| `backend/` | 后端 FastAPI 项目目录 |
| `backend/app/main.py` | FastAPI 应用入口 |
| `backend/Dockerfile` | 后端镜像构建文件 |
| `backend/requirements.txt` | Python 依赖列表 |
| `storage/resumes/` | 用户上传简历文件存储目录 |
| `docker-compose.yml` | 开发环境容器编排文件 |
| `.env.example` | 环境变量示例文件，可提交到仓库 |
| `.env.dev` | 本地开发环境变量文件，不建议提交 |
| `.gitignore` | Git 忽略规则 |

---

# 4. 创建 Docker 开发环境

## 4.1 创建项目目录

在终端执行：

```bash
mkdir resume-analyzer
cd resume-analyzer
```

创建后端目录和上传文件目录：

```bash
mkdir -p backend/app
mkdir -p storage/resumes
```

---

## 4.2 创建 FastAPI 应用入口

创建文件：

```text
backend/app/main.py
```

写入以下内容：

```python
from fastapi import FastAPI

app = FastAPI(
    title="简历分析系统 API",
    description="Resume Analyzer Backend API",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "success": True,
        "code": 0,
        "message": "ok",
        "data": {
            "status": "healthy"
        }
    }
```

说明：

1. `FastAPI(...)` 用于创建后端应用。
2. `/health` 是健康检查接口，用于确认服务是否正常启动。
3. 后续所有业务接口都会注册到该 FastAPI 应用中。

---

## 4.3 创建后端 Dockerfile

创建文件：

```text
backend/Dockerfile
```

写入以下内容：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

说明：

1. 使用 `python:3.11-slim` 作为基础镜像。
2. 工作目录设置为 `/app`。
3. 安装 `libpq-dev`，用于支持 PostgreSQL 相关依赖。
4. 复制并安装 Python 依赖。
5. 暴露容器内部 `8000` 端口。
6. 默认使用 Uvicorn 启动 FastAPI。

---

# 5. 安装 FastAPI、SQLAlchemy、Alembic、Pydantic 等依赖

## 5.1 创建 requirements.txt

创建文件：

```text
backend/requirements.txt
```

写入以下内容：

```text
fastapi
uvicorn[standard]

sqlalchemy
alembic
psycopg2-binary

pydantic
pydantic-settings

python-jose[cryptography]
passlib[bcrypt]

python-multipart
python-docx
pypdf

httpx
```

## 5.2 依赖说明

| 依赖 | 用途 |
|---|---|
| `fastapi` | 后端 Web 框架 |
| `uvicorn[standard]` | FastAPI ASGI 运行服务 |
| `sqlalchemy` | ORM 数据库操作 |
| `alembic` | 数据库迁移管理 |
| `psycopg2-binary` | PostgreSQL 数据库驱动 |
| `pydantic` | 请求和响应数据校验 |
| `pydantic-settings` | 环境变量和配置读取 |
| `python-jose[cryptography]` | JWT Token 生成与校验 |
| `passlib[bcrypt]` | 用户密码加密 |
| `python-multipart` | 文件上传支持 |
| `python-docx` | DOCX 简历解析 |
| `pypdf` | PDF 简历解析 |
| `httpx` | 调用 DeepSeek API |

---

# 6. 配置 .env.dev

## 6.1 创建 .env.example

`.env.example` 是环境变量示例文件，可以提交到代码仓库，用于说明项目需要哪些配置项。

在项目根目录创建：

```text
.env.example
```

写入以下内容：

```env
# App
APP_ENV=dev
APP_DEBUG=true
APP_SECRET_KEY=change-me

# Backend
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:5173

# Database
POSTGRES_DB=resume_analyzer
POSTGRES_USER=resume_user
POSTGRES_PASSWORD=resume_pass
DATABASE_URL=postgresql+psycopg2://resume_user:resume_pass@db:5432/resume_analyzer

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
JWT_SECRET_KEY=change-me
JWT_EXPIRE_MINUTES=1440

# DeepSeek
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

# Upload
UPLOAD_DIR=/app/storage/resumes
MAX_UPLOAD_SIZE_MB=10
```

---

## 6.2 创建 .env.dev

`.env.dev` 是本地开发环境使用的真实配置文件，不建议提交到 Git 仓库。

执行：

```bash
cp .env.example .env.dev
```

然后编辑：

```bash
nano .env.dev
```

也可以使用 VS Code 打开编辑：

```bash
code .env.dev
```

开发阶段建议配置如下：

```env
APP_ENV=dev
APP_DEBUG=true
APP_SECRET_KEY=dev-secret-key

BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:5173

POSTGRES_DB=resume_analyzer
POSTGRES_USER=resume_user
POSTGRES_PASSWORD=resume_pass
DATABASE_URL=postgresql+psycopg2://resume_user:resume_pass@db:5432/resume_analyzer

REDIS_URL=redis://redis:6379/0

JWT_SECRET_KEY=dev-jwt-secret-key
JWT_EXPIRE_MINUTES=1440

DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

UPLOAD_DIR=/app/storage/resumes
MAX_UPLOAD_SIZE_MB=10
```

说明：

1. `DATABASE_URL` 中的主机名使用 `db`，因为后端容器会通过 Docker Compose 服务名访问数据库。
2. `DEEPSEEK_API_KEY` 开发初期可以先占位，后续测试 AI 调用时必须替换为真实 Key。
3. `UPLOAD_DIR=/app/storage/resumes` 对应容器内部路径。
4. 本地目录 `./storage/resumes` 会挂载到容器内部 `/app/storage/resumes`。

---

# 7. 创建 docker-compose.yml

## 7.1 创建开发环境 Compose 文件

在项目根目录创建：

```text
docker-compose.yml
```

写入以下内容：

```yaml
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
      - ./storage/resumes:/app/storage/resumes
    ports:
      - "8000:8000"
    env_file:
      - .env.dev
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data_dev:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data_dev:
```

## 7.2 服务说明

| 服务 | 说明 |
|---|---|
| `backend` | FastAPI 后端服务 |
| `db` | PostgreSQL 数据库服务 |
| `postgres_data_dev` | PostgreSQL 开发数据持久化卷 |

## 7.3 backend 服务说明

```yaml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

说明：

1. `--host 0.0.0.0` 表示容器外部可以访问该服务。
2. `--port 8000` 表示服务运行在 8000 端口。
3. `--reload` 表示代码修改后自动重启服务，适合开发环境。

---

# 8. 创建 .gitignore

在项目根目录创建：

```text
.gitignore
```

写入以下内容：

```gitignore
.env.dev
.env.prod

__pycache__/
*.pyc
*.pyo
*.pyd

.venv/
venv/

data/
logs/
backups/

storage/resumes/*
!storage/resumes/.gitkeep

postgres_data_dev/
```

创建 `.gitkeep` 文件，保留空目录：

```bash
touch storage/resumes/.gitkeep
```

说明：

1. `.env.dev` 和 `.env.prod` 不提交，避免泄露密钥。
2. 用户上传的简历文件不提交。
3. 数据库数据、日志、备份文件不提交。
4. `.gitkeep` 用于让 Git 保留空目录结构。

---

# 9. 启动开发环境

## 9.1 前台启动

在项目根目录执行：

```bash
docker compose --env-file .env.dev up --build
```

说明：

1. `--env-file .env.dev` 表示使用开发环境变量。
2. `up` 表示启动服务。
3. `--build` 表示重新构建镜像。

## 9.2 后台启动

如果希望服务在后台运行：

```bash
docker compose --env-file .env.dev up -d --build
```

---

# 10. 验证开发环境

## 10.1 查看容器状态

执行：

```bash
docker compose --env-file .env.dev ps
```

预期看到：

```text
backend   running
db        running
```

## 10.2 访问健康检查接口

浏览器打开：

```text
http://localhost:8000/health
```

预期返回：

```json
{
  "success": true,
  "code": 0,
  "message": "ok",
  "data": {
    "status": "healthy"
  }
}
```

## 10.3 访问 FastAPI 文档

浏览器打开：

```text
http://localhost:8000/docs
```

如果可以看到 Swagger API 文档，说明 FastAPI 服务启动成功。

---

# 11. 常用开发命令

## 11.1 启动服务

```bash
docker compose --env-file .env.dev up
```

## 11.2 后台启动服务

```bash
docker compose --env-file .env.dev up -d
```

## 11.3 停止服务

```bash
docker compose --env-file .env.dev down
```

## 11.4 重新构建服务

```bash
docker compose --env-file .env.dev up --build
```

## 11.5 查看全部日志

```bash
docker compose --env-file .env.dev logs -f
```

## 11.6 查看后端日志

```bash
docker compose --env-file .env.dev logs -f backend
```

## 11.7 查看数据库日志

```bash
docker compose --env-file .env.dev logs -f db
```

## 11.8 进入后端容器

```bash
docker compose --env-file .env.dev exec backend bash
```

## 11.9 进入数据库容器

```bash
docker compose --env-file .env.dev exec db psql -U resume_user -d resume_analyzer
```

---

# 12. 常见问题

## 12.1 端口 8000 被占用

如果启动时报错端口占用，可以查看占用进程：

```bash
lsof -i :8000
```

或临时修改 `docker-compose.yml`：

```yaml
ports:
  - "8001:8000"
```

然后通过以下地址访问：

```text
http://localhost:8001/health
```

## 12.2 数据库端口 5432 被占用

如果本机已经安装 PostgreSQL，可能会占用 5432 端口。

可以修改为：

```yaml
ports:
  - "5433:5432"
```

容器内部仍然使用 `db:5432`，所以 `DATABASE_URL` 不需要修改。

## 12.3 后端依赖安装失败

可以尝试重新构建：

```bash
docker compose --env-file .env.dev build --no-cache backend
```

然后重新启动：

```bash
docker compose --env-file .env.dev up
```

## 12.4 修改代码后没有自动生效

确认 `docker-compose.yml` 中 backend 服务包含：

```yaml
volumes:
  - ./backend:/app
```

并且启动命令包含：

```bash
--reload
```

---

# 13. 本阶段验收标准

完成本文档后，需要确认以下事项：

- [ ] 项目目录结构创建完成。
- [ ] `backend/app/main.py` 已创建。
- [ ] `backend/Dockerfile` 已创建。
- [ ] `backend/requirements.txt` 已创建。
- [ ] `.env.example` 已创建。
- [ ] `.env.dev` 已创建。
- [ ] `docker-compose.yml` 已创建。
- [ ] `.gitignore` 已创建。
- [ ] Docker Compose 可以正常启动后端和数据库。
- [ ] `http://localhost:8000/health` 可以正常访问。
- [ ] `http://localhost:8000/docs` 可以正常访问。

---

# 14. 下一步工作

完成 Docker 开发环境、依赖安装和 `.env.dev` 配置后，下一步建议继续完成：

1. SQLAlchemy 数据库连接配置。
2. Alembic 初始化。
3. 创建 `users`、`resumes`、`job_descriptions` 等核心数据表。
4. 实现统一响应格式。
5. 实现用户注册和登录接口。
