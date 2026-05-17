# 简历分析系统 Docker 部署文档

## 1. 文档说明

### 1.1 文档目的

本文档用于说明简历分析系统在 Docker 环境下的开发、构建、部署、运行、更新、备份和故障排查流程。

本文档主要面向：

- 后端开发人员
- 前端开发人员
- 部署运维人员
- 项目维护人员
- 项目评审人员

### 1.2 系统部署架构

本项目采用前后端分离架构：

- 前端：Vue 3 + Vite + TypeScript + Element Plus
- 后端：Python FastAPI
- 数据库：PostgreSQL
- AI 服务：DeepSeek API
- 容器管理：Docker + Docker Compose
- 反向代理：Nginx
- 部署目标：个人云服务器

------

## 2. Docker 部署目标

Docker 化部署需要实现以下目标：

1. 开发环境和生产环境尽量保持一致。
2. 降低 Python、Node.js、PostgreSQL 等运行环境安装复杂度。
3. 支持一键启动前端、后端、数据库等服务。
4. 支持在个人云服务器上快速部署。
5. 支持数据持久化，避免容器删除导致数据丢失。
6. 支持后续扩展 Redis、Worker、HTTPS、备份任务等能力。

------

## 3. 服务组成

## 3.1 开发环境服务

开发环境建议包含以下服务：

| 服务名   | 说明                       | 默认端口 |
| -------- | -------------------------- | -------- |
| frontend | Vue 3 Vite 开发服务        | 5173     |
| backend  | FastAPI 后端服务           | 8000     |
| db       | PostgreSQL 数据库          | 5432     |
| redis    | Redis 缓存和任务队列，可选 | 6379     |

开发环境访问地址：

```text
前端：http://localhost:5173
后端：http://localhost:8000
API 文档：http://localhost:8000/docs
数据库：localhost:5432
```

## 3.2 生产环境服务

生产环境建议包含以下服务：

| 服务名   | 说明                         | 是否对外暴露 |
| -------- | ---------------------------- | ------------ |
| nginx    | 统一入口，代理前端和后端 API | 是，80/443   |
| frontend | 前端构建产物或静态资源服务   | 否           |
| backend  | FastAPI 后端 API 服务        | 否           |
| db       | PostgreSQL 数据库            | 否           |
| redis    | Redis，可选                  | 否           |
| worker   | 异步任务 Worker，可选        | 否           |

生产环境访问地址：

```text
前端页面：https://your-domain.com
后端接口：https://your-domain.com/api
```

------

## 4. 推荐目录结构

项目根目录建议如下：

```text
resume-analyzer/
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── deploy/
│   ├── nginx/
│   │   ├── nginx.dev.conf
│   │   └── nginx.prod.conf
│   └── scripts/
│       ├── backup_db.sh
│       ├── restore_db.sh
│       ├── deploy.sh
│       └── init_server.sh
├── storage/
│   └── resumes/
├── backups/
├── logs/
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .env.dev
├── .env.prod
├── .gitignore
└── README.md
```

说明：

- `backend`：后端 FastAPI 项目。
- `frontend`：前端 Vue 项目。
- `deploy/nginx`：Nginx 配置。
- `deploy/scripts`：部署、备份、恢复脚本。
- `storage/resumes`：用户上传简历文件。
- `backups`：数据库备份文件。
- `logs`：应用日志目录，可选。

------

## 5. 环境变量设计

## 5.1 环境变量文件

建议使用以下环境变量文件：

```text
.env.example  # 示例配置，可提交到仓库
.env.dev      # 开发环境配置，不建议提交
.env.prod     # 生产环境配置，禁止提交
```

### 5.2 .env.example 示例

```text
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

# Frontend
VITE_APP_TITLE=简历分析系统
VITE_API_BASE_URL=http://localhost:8000/api

# Admin Init
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=change-me-immediately
```

## 5.3 生产环境配置要求

生产环境 `.env.prod` 必须满足：

1. `APP_DEBUG=false`。
2. 使用强随机 `APP_SECRET_KEY`。
3. 使用强随机 `JWT_SECRET_KEY`。
4. 修改默认数据库密码。
5. 配置真实 DeepSeek API Key。
6. 不允许提交到 Git 仓库。
7. 不在日志中打印环境变量。

------

## 6. 后端 Dockerfile 设计

后端 Dockerfile 建议放在：

```text
backend/Dockerfile
```

示例：

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

RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

说明：

1. 使用 `python:3.11-slim` 作为基础镜像。
2. 安装 PostgreSQL 相关依赖。
3. 使用非 root 用户运行应用。
4. 生产环境可改用 Gunicorn + Uvicorn Worker。

生产环境启动命令可选：

```text
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000
```

------

## 7. 前端 Dockerfile 设计

前端 Dockerfile 建议放在：

```text
frontend/Dockerfile
```

示例：

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

说明：

1. 第一阶段使用 Node.js 构建前端静态资源。
2. 第二阶段使用 Nginx 托管静态资源。
3. 如果生产环境统一使用根目录的 Nginx 容器，也可以只构建 dist 文件，再由统一 Nginx 托管。

------

## 8. 开发环境 docker-compose.yml

开发环境文件：

```text
docker-compose.yml
```

示例：

```yaml
services:
  frontend:
    image: node:20-alpine
    working_dir: /app
    volumes:
      - ./frontend:/app
      - frontend_node_modules:/app/node_modules
    command: sh -c "npm install && npm run dev -- --host 0.0.0.0"
    ports:
      - "5173:5173"
    env_file:
      - .env.dev
    depends_on:
      - backend

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

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "6379:6379"

volumes:
  postgres_data_dev:
  frontend_node_modules:
```

说明：

1. 开发环境将前后端代码挂载到容器，便于热更新。
2. 前端使用 Vite Dev Server。
3. 后端使用 Uvicorn reload 模式。
4. PostgreSQL 数据通过 volume 持久化。
5. Redis 一期可保留，也可暂时注释。

------

## 9. 生产环境 docker-compose.prod.yml

生产环境文件：

```text
docker-compose.prod.yml
```

示例：

```yaml
services:
  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"  //https 
      - "443:443"  // nginx
    volumes:
      - ./deploy/nginx/nginx.prod.conf:/etc/nginx/conf.d/default.conf:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
      - ./storage/resumes:/var/www/resumes:ro
      - ./logs/nginx:/var/log/nginx
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    restart: unless-stopped
    command: gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000
    volumes:
      - ./storage/resumes:/app/storage/resumes
      - ./logs/backend:/app/logs
    env_file:
      - .env.prod
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
      - ./data/postgres:/var/lib/postgresql/data
      - ./backups:/backups
    expose:
      - "5432"

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    expose:
      - "6379"

volumes: {}
```

说明：

1. 生产环境只对外暴露 Nginx 的 80 和 443 端口。
2. Backend、PostgreSQL、Redis 不直接暴露公网端口。
3. PostgreSQL 数据挂载到宿主机目录。
4. 用户上传简历挂载到宿主机目录。
5. 生产环境建议提前执行前端构建，生成 `frontend/dist`。

------

## 10. Nginx 配置

## 10.1 生产环境 Nginx 配置

配置文件建议放在：

```text
deploy/nginx/nginx.prod.conf
```

示例：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 10m;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 60s;
        proxy_read_timeout 120s;
        proxy_send_timeout 120s;
    }
}
```

说明：

1. `/` 访问前端页面。
2. `/api/` 转发到后端服务。
3. `try_files` 用于支持 Vue 前端路由。
4. `client_max_body_size` 需要与后端上传限制保持一致。
5. AI 分析可能耗时较长，因此适当增加 proxy timeout。

## 10.2 HTTPS 配置示例

如果已经申请证书，可以配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    client_max_body_size 10m;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 60s;
        proxy_read_timeout 120s;
        proxy_send_timeout 120s;
    }
}
```

------

## 11. 本地开发流程

## 11.1 准备配置文件

复制环境变量示例：

```bash
cp .env.example .env.dev
```

修改 `.env.dev` 中的配置，至少包括：

```text
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
DATABASE_URL
JWT_SECRET_KEY
DEEPSEEK_API_KEY
VITE_API_BASE_URL
```

## 11.2 启动开发环境

```bash
docker compose --env-file .env.dev up --build
```

后台启动：

```bash
docker compose --env-file .env.dev up -d --build
```

## 11.3 查看服务状态

```bash
docker compose ps
```

## 11.4 查看日志

查看全部日志：

```bash
docker compose logs -f
```

查看后端日志：

```bash
docker compose logs -f backend
```

查看前端日志：

```bash
docker compose logs -f frontend
```

## 11.5 执行数据库迁移

```bash
docker compose exec backend alembic upgrade head
```

## 11.6 访问系统

```text
前端：http://localhost:5173
后端：http://localhost:8000
API 文档：http://localhost:8000/docs
```

------

## 12. 生产部署流程

## 12.1 云服务器准备

推荐服务器配置：

| 配置项 | 建议                 |
| ------ | -------------------- |
| CPU    | 2 核及以上           |
| 内存   | 2 GB 起步，推荐 4 GB |
| 磁盘   | 40 GB 起步           |
| 系统   | Ubuntu LTS           |
| 端口   | 22、80、443          |

## 12.2 安装基础软件

服务器需要安装：

- Docker
- Docker Compose Plugin
- Git
- Certbot，可选

安装后检查：

```bash
docker --version
docker compose version
git --version
```

## 12.3 拉取项目代码

```bash
git clone your-repository-url resume-analyzer
cd resume-analyzer
```

## 12.4 创建生产环境配置

```bash
cp .env.example .env.prod
```

修改 `.env.prod`：

```text
APP_ENV=prod
APP_DEBUG=false
POSTGRES_PASSWORD=强密码
JWT_SECRET_KEY=强随机字符串
DEEPSEEK_API_KEY=真实 API Key
VITE_API_BASE_URL=/api
```

## 12.5 创建数据目录

```bash
mkdir -p data/postgres
mkdir -p storage/resumes
mkdir -p backups
mkdir -p logs/backend
mkdir -p logs/nginx
```

## 12.6 构建前端静态文件

方式一：本地构建后上传服务器。

```bash
cd frontend
npm install
npm run build
```

方式二：在服务器上构建。

```bash
cd frontend
npm install
npm run build
cd ..
```

也可以通过 Docker 构建前端镜像后复制 dist，后续可进一步自动化。

## 12.7 启动生产环境

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --build
```

## 12.8 执行数据库迁移

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml exec backend alembic upgrade head
```

## 12.9 创建默认管理员

如果后端提供初始化命令，可执行：

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml exec backend python -m app.scripts.create_admin
```

如果项目采用自动初始化方式，则首次启动时根据 `.env.prod` 中的 `ADMIN_EMAIL` 和 `ADMIN_PASSWORD` 创建管理员。

## 12.10 检查服务状态

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml ps
```

查看日志：

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml logs -f backend
```

------

## 13. 域名与 HTTPS 配置

## 13.1 域名解析

将域名 A 记录解析到服务器公网 IP。

示例：

```text
your-domain.com -> 服务器公网 IP
```

## 13.2 HTTP 验证

启动 Nginx 后，先通过 HTTP 访问：

```text
http://your-domain.com
```

确认页面可正常打开。

## 13.3 申请 HTTPS 证书

如果使用 Certbot，可在宿主机执行：

```bash
sudo certbot certonly --standalone -d your-domain.com
```

申请成功后，证书路径通常为：

```text
/etc/letsencrypt/live/your-domain.com/fullchain.pem
/etc/letsencrypt/live/your-domain.com/privkey.pem
```

然后修改 Nginx 配置为 HTTPS 配置，并重启 Nginx 容器。

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml restart nginx
```

## 13.4 证书续期

Certbot 通常会配置自动续期。可以手动测试：

```bash
sudo certbot renew --dry-run
```

续期后需要重载或重启 Nginx。

------

## 14. 数据持久化设计

## 14.1 需要持久化的数据

| 数据            | 建议路径          |
| --------------- | ----------------- |
| PostgreSQL 数据 | ./data/postgres   |
| 用户上传简历    | ./storage/resumes |
| 数据库备份      | ./backups         |
| 后端日志        | ./logs/backend    |
| Nginx 日志      | ./logs/nginx      |

## 14.2 注意事项

1. 不要将 `data/postgres` 提交到 Git 仓库。
2. 不要将用户上传文件提交到 Git 仓库。
3. 不要将备份文件提交到公开仓库。
4. 服务器迁移时，需要同时迁移数据库和上传文件。

------

## 15. 数据库备份与恢复

## 15.1 手动备份

```bash
mkdir -p backups

docker compose --env-file .env.prod -f docker-compose.prod.yml exec db \
  pg_dump -U resume_user resume_analyzer > backups/resume_analyzer_$(date +%F_%H%M%S).sql
```

说明：

- `resume_user` 需要与 `.env.prod` 中的 `POSTGRES_USER` 一致。
- `resume_analyzer` 需要与 `.env.prod` 中的 `POSTGRES_DB` 一致。

## 15.2 手动恢复

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml exec -T db \
  psql -U resume_user resume_analyzer < backups/resume_analyzer_2026-05-07_120000.sql
```

恢复前建议：

1. 停止后端服务。
2. 备份当前数据库。
3. 确认恢复文件正确。
4. 恢复后检查数据完整性。

## 15.3 上传文件备份

```bash
tar -czf backups/uploads_$(date +%F_%H%M%S).tar.gz storage/resumes
```

## 15.4 备份脚本示例

文件路径：

```text
deploy/scripts/backup_db.sh
```

示例：

```bash
#!/usr/bin/env bash
set -e

BACKUP_DIR="./backups"
DATE=$(date +%F_%H%M%S)
DB_USER=${POSTGRES_USER:-resume_user}
DB_NAME=${POSTGRES_DB:-resume_analyzer}

mkdir -p "$BACKUP_DIR"

docker compose --env-file .env.prod -f docker-compose.prod.yml exec -T db \
  pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_DIR/resume_analyzer_$DATE.sql"

tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" storage/resumes

find "$BACKUP_DIR" -type f -mtime +7 -delete

echo "Backup completed: $DATE"
```

赋予执行权限：

```bash
chmod +x deploy/scripts/backup_db.sh
```

## 15.5 定时备份

使用 crontab：

```bash
crontab -e
```

添加每日凌晨 3 点备份：

```text
0 3 * * * cd /opt/resume-analyzer && /bin/bash deploy/scripts/backup_db.sh >> logs/backup.log 2>&1
```

------

## 16. 发布更新流程

## 16.1 手动更新流程

```bash
cd /opt/resume-analyzer

git pull

cd frontend
npm install
npm run build
cd ..

docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --build

docker compose --env-file .env.prod -f docker-compose.prod.yml exec backend alembic upgrade head

docker compose --env-file .env.prod -f docker-compose.prod.yml ps
```

## 16.2 更新前检查

更新前建议：

1. 备份数据库。
2. 备份上传文件。
3. 确认 `.env.prod` 未被覆盖。
4. 确认数据库迁移文件已经提交。
5. 确认前端构建成功。

## 16.3 回滚策略

如果更新失败，可采用：

1. 回退 Git 到上一个版本。
2. 重新构建并启动容器。
3. 如涉及数据库变更，根据情况执行 Alembic downgrade。
4. 必要时恢复数据库备份。

------

## 17. 常用 Docker 命令

## 17.1 启动服务

```bash
docker compose --env-file .env.dev up -d --build
```

## 17.2 停止服务

```bash
docker compose down
```

## 17.3 查看容器状态

```bash
docker compose ps
```

## 17.4 查看日志

```bash
docker compose logs -f backend
```

## 17.5 进入后端容器

```bash
docker compose exec backend sh
```

## 17.6 进入数据库容器

```bash
docker compose exec db sh
```

## 17.7 执行数据库迁移

```bash
docker compose exec backend alembic upgrade head
```

## 17.8 重启某个服务

```bash
docker compose restart backend
```

## 17.9 重新构建某个服务

```bash
docker compose build backend
```

------

## 18. 日志管理

## 18.1 查看后端日志

```bash
docker compose logs -f backend
```

## 18.2 查看 Nginx 日志

```bash
docker compose logs -f nginx
```

如果挂载了日志目录：

```bash
tail -f logs/nginx/access.log
tail -f logs/nginx/error.log
```

## 18.3 日志安全要求

日志中不得输出：

1. 用户密码。
2. JWT Token。
3. DeepSeek API Key。
4. 完整简历原文。
5. 完整手机号和邮箱。
6. 数据库密码。

------

## 19. 安全配置要求

## 19.1 服务器安全组

生产服务器建议只开放：

| 端口 | 用途  |
| ---- | ----- |
| 22   | SSH   |
| 80   | HTTP  |
| 443  | HTTPS |

不应对公网开放：

- 5432 PostgreSQL
- 6379 Redis
- 8000 Backend
- 5173 Vite Dev Server

## 19.2 Docker 安全

1. 生产环境关闭 debug。
2. 不使用默认弱密码。
3. `.env.prod` 不提交 Git。
4. 数据库和 Redis 不暴露公网端口。
5. 定期更新基础镜像。
6. 上传目录禁止执行脚本。
7. 后端容器尽量使用非 root 用户。

## 19.3 应用安全

1. 后端接口必须校验 JWT。
2. 管理员接口必须校验角色。
3. 文件上传必须校验类型和大小。
4. API Key 只能由后端读取。
5. AI 调用日志不得保存完整隐私内容。

------

## 20. 故障排查

## 20.1 前端打不开

检查项：

1. Nginx 容器是否运行。
2. 前端 `dist` 是否存在。
3. Nginx 配置路径是否正确。
4. 域名是否解析到服务器。
5. 服务器安全组是否开放 80/443。

命令：

```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs nginx
```

## 20.2 API 请求失败

检查项：

1. 后端容器是否运行。
2. Nginx `/api/` 代理是否正确。
3. 后端是否正常连接数据库。
4. `.env.prod` 中 DATABASE_URL 是否正确。
5. CORS 配置是否正确。

## 20.3 数据库连接失败

检查项：

1. db 容器是否运行。
2. POSTGRES_USER、POSTGRES_PASSWORD、POSTGRES_DB 是否一致。
3. DATABASE_URL 中 host 是否为 `db`。
4. 数据库 volume 是否损坏。

命令：

```bash
docker compose -f docker-compose.prod.yml logs db
```

## 20.4 文件上传失败

检查项：

1. Nginx `client_max_body_size` 是否足够。
2. 后端 `MAX_UPLOAD_SIZE_MB` 是否足够。
3. 上传目录是否挂载正确。
4. 后端容器是否有写入权限。
5. 文件类型是否在允许范围内。

## 20.5 AI 分析失败

检查项：

1. DEEPSEEK_API_KEY 是否正确。
2. 服务器是否可以访问 DeepSeek API。
3. 输入文本是否过长。
4. 后端日志中是否有超时或限流错误。
5. Prompt 模板是否存在并启用。

## 20.6 HTTPS 证书失败

检查项：

1. 域名是否正确解析。
2. 80 端口是否可访问。
3. 证书路径是否正确挂载到 Nginx 容器。
4. Nginx 配置中的 server_name 是否正确。
5. 证书是否过期。

------

## 21. MVP 部署建议

一期 MVP 可采用简化部署方案：

```text
Nginx
Backend
PostgreSQL
```

前端构建为静态文件，由 Nginx 托管。

暂缓引入：

- Redis
- Worker
- CI/CD
- 对象存储
- 日志采集系统
- 容器监控系统

MVP 部署重点：

1. 前端能访问。
2. 后端 API 能访问。
3. 数据库能持久化。
4. 简历文件能持久化。
5. DeepSeek API 能正常调用。
6. 数据库能备份和恢复。

------

## 22. 后续优化方向

后续可以逐步优化：

1. 使用 GitHub Actions 自动部署。
2. 使用 Redis + Celery 执行异步 AI 分析。
3. 使用对象存储保存简历文件。
4. 增加 Prometheus + Grafana 监控。
5. 增加 Loki 或 ELK 日志系统。
6. 增加蓝绿部署或滚动发布。
7. 增加数据库定期远程备份。
8. 增加 Nginx Proxy Manager 简化证书管理。

------

## 23. 总结

本文档定义了简历分析系统基于 Docker 和 Docker Compose 的开发与生产部署方案。

开发环境通过 Docker Compose 启动 Vue 前端、FastAPI 后端和 PostgreSQL 数据库，便于快速开发和调试。生产环境通过 Nginx 统一对外提供访问入口，前端静态资源由 Nginx 托管，后端 API 在 Docker 内部网络中运行，PostgreSQL 和上传文件通过宿主机目录持久化。

一期部署应优先保证系统可运行、数据可持久化、配置不泄露、服务可备份和故障可排查。后续可根据系统规模逐步引入异步任务、自动化部署、监控和对象存储。