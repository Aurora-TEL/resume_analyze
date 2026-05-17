# 简历分析系统后端 API 接口设计文档

## 1. 文档说明

### 1.1 文档目的

本文档用于定义简历分析系统后端 API 接口规范，包括接口路径、请求方法、鉴权规则、请求参数、响应格式、错误码、分页规范和接口模块划分。

本文档主要面向：

- 后端开发人员
- 前端开发人员
- 测试人员
- 项目评审人员
- 后续维护人员

### 1.2 技术背景

系统采用前后端分离架构：

- 前端：Vue 3 + Vite + TypeScript + Element Plus
- 后端：Python FastAPI
- 数据库：PostgreSQL
- AI 服务：DeepSeek API
- 部署：Docker + Docker Compose + Nginx

前端通过 Axios 调用后端 RESTful API。后端返回统一 JSON 格式。

------

## 2. API 设计原则

### 2.1 RESTful 风格

接口路径使用资源名表示，HTTP 方法表示操作类型。

| HTTP 方法 | 用途         | 示例                            |
| --------- | ------------ | ------------------------------- |
| GET       | 查询资源     | GET /api/resumes                |
| POST      | 创建资源     | POST /api/resumes/upload        |
| PUT       | 全量更新资源 | PUT /api/users/me               |
| PATCH     | 局部更新资源 | PATCH /api/resumes/{resume_id}  |
| DELETE    | 删除资源     | DELETE /api/resumes/{resume_id} |

### 2.2 接口前缀

所有业务接口统一使用 `/api` 前缀。

示例：

```text
/api/auth/login
/api/resumes
/api/jobs
/api/analysis/tasks
```

### 2.3 版本管理

一期可暂不在路径中加入版本号。

后续如需要版本化，可调整为：

```text
/api/v1/auth/login
/api/v1/resumes
```

### 2.4 数据格式

普通接口使用 JSON 请求和响应。

文件上传接口使用 `multipart/form-data`。

### 2.5 时间格式

时间统一使用 ISO 8601 格式。

示例：

```text
2026-05-07T10:30:00+08:00
```

------

## 3. 统一响应格式

### 3.1 成功响应格式

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {}
}
```

字段说明：

| 字段    | 类型                  | 说明       |
| ------- | --------------------- | ---------- |
| success | boolean               | 是否成功   |
| code    | integer               | 业务状态码 |
| message | string                | 响应消息   |
| data    | object / array / null | 响应数据   |

### 3.2 失败响应格式

```json
{
  "success": false,
  "code": 40001,
  "message": "参数错误",
  "data": null
}
```

### 3.3 分页响应格式

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "page_size": 10,
    "pages": 10
  }
}
```

分页字段说明：

| 字段      | 类型    | 说明       |
| --------- | ------- | ---------- |
| items     | array   | 当前页数据 |
| total     | integer | 总记录数   |
| page      | integer | 当前页码   |
| page_size | integer | 每页数量   |
| pages     | integer | 总页数     |

------

## 4. 鉴权设计

### 4.1 鉴权方式

系统采用 JWT Bearer Token 鉴权。

前端登录成功后保存 `access_token`，后续请求在 Header 中携带：

```text
Authorization: Bearer {access_token}
```

### 4.2 无需登录接口

以下接口无需登录：

- 用户注册
- 用户登录
- 健康检查

### 4.3 需要登录接口

除公开接口外，其余业务接口均需要登录。

### 4.4 管理员接口

管理员接口需要满足：

1. 用户已登录。
2. 用户角色为 `admin`。

管理员接口统一使用 `/api/admin` 前缀。

------

## 5. 通用请求参数规范

### 5.1 分页参数

列表接口统一支持：

| 参数      | 类型    | 必填 | 默认值 | 说明     |
| --------- | ------- | ---- | ------ | -------- |
| page      | integer | 否   | 1      | 页码     |
| page_size | integer | 否   | 10     | 每页数量 |

限制：

- page 最小值为 1。
- page_size 最小值为 1。
- page_size 最大值建议为 100。

### 5.2 排序参数

部分列表接口可支持：

| 参数    | 类型   | 必填 | 示例       | 说明       |
| ------- | ------ | ---- | ---------- | ---------- |
| sort_by | string | 否   | created_at | 排序字段   |
| order   | string | 否   | desc       | asc / desc |

### 5.3 搜索参数

部分列表接口可支持：

| 参数    | 类型   | 必填 | 说明       |
| ------- | ------ | ---- | ---------- |
| keyword | string | 否   | 关键词搜索 |

------

## 6. 错误码设计

| 错误码 | 含义                  | HTTP 状态码 | 说明                     |
| ------ | --------------------- | ----------- | ------------------------ |
| 0      | success               | 200         | 成功                     |
| 40000  | bad_request           | 400         | 请求错误                 |
| 40001  | validation_error      | 422         | 参数校验失败             |
| 40100  | unauthorized          | 401         | 未登录或 Token 无效      |
| 40101  | token_expired         | 401         | Token 已过期             |
| 40300  | forbidden             | 403         | 无访问权限               |
| 40400  | not_found             | 404         | 资源不存在               |
| 40900  | conflict              | 409         | 资源冲突，例如邮箱已存在 |
| 41300  | file_too_large        | 413         | 文件过大                 |
| 41500  | unsupported_file_type | 415         | 文件类型不支持           |
| 42900  | too_many_requests     | 429         | 请求过于频繁             |
| 50000  | internal_error        | 500         | 系统内部错误             |
| 50010  | ai_service_error      | 500         | AI 服务调用失败          |
| 50011  | ai_response_invalid   | 500         | AI 返回格式错误          |
| 50300  | service_unavailable   | 503         | 服务暂不可用             |

------

## 7. 用户认证接口

## 7.1 用户注册

### 基本信息

```text
POST /api/auth/register
```

是否需要登录：否

### 请求参数

```json
{
  "email": "user@example.com",
  "password": "Password123",
  "nickname": "张三"
}
```

| 参数     | 类型   | 必填 | 说明            |
| -------- | ------ | ---- | --------------- |
| email    | string | 是   | 邮箱            |
| password | string | 是   | 密码，至少 8 位 |
| nickname | string | 否   | 昵称            |

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "user_id": "uuid",
    "email": "user@example.com",
    "nickname": "张三",
    "role": "user",
    "access_token": "jwt-token",
    "token_type": "bearer"
  }
}
```

### 业务规则

1. 邮箱必须唯一。
2. 密码必须加密存储。
3. 注册成功后默认角色为 `user`。
4. 注册成功后可直接返回 Token。

------

## 7.2 用户登录

### 基本信息

```text
POST /api/auth/login
```

是否需要登录：否

### 请求参数

```json
{
  "email": "user@example.com",
  "password": "Password123"
}
```

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "jwt-token",
    "token_type": "bearer",
    "expires_in": 86400,
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "nickname": "张三",
      "role": "user"
    }
  }
}
```

### 业务规则

1. 校验邮箱和密码。
2. 用户状态必须为 `active`。
3. 登录成功后更新 `last_login_at`。
4. 登录失败应返回统一错误，不暴露具体账号是否存在。

------

## 7.3 获取当前用户信息

### 基本信息

```text
GET /api/auth/me
```

是否需要登录：是

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "nickname": "张三",
    "phone": "138****0000",
    "target_position": "Python 后端开发工程师",
    "target_city": "北京",
    "work_years": 1.5,
    "role": "user",
    "status": "active"
  }
}
```

------

## 7.4 退出登录

### 基本信息

```text
POST /api/auth/logout
```

是否需要登录：是

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "退出成功",
  "data": null
}
```

说明：

一期可由前端删除本地 Token 完成退出。后端接口可保留，用于后续 Token 黑名单扩展。

------

## 8. 用户中心接口

## 8.1 更新当前用户信息

### 基本信息

```text
PUT /api/users/me
```

是否需要登录：是

### 请求参数

```json
{
  "nickname": "张三",
  "phone": "13800000000",
  "target_position": "Python 后端开发工程师",
  "target_city": "上海",
  "work_years": 2.0
}
```

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "更新成功",
  "data": {
    "id": "uuid",
    "nickname": "张三",
    "target_position": "Python 后端开发工程师",
    "target_city": "上海",
    "work_years": 2.0
  }
}
```

------

## 8.2 修改密码

### 基本信息

```text
PUT /api/users/me/password
```

是否需要登录：是

### 请求参数

```json
{
  "old_password": "OldPassword123",
  "new_password": "NewPassword123"
}
```

### 业务规则

1. 必须校验旧密码。
2. 新密码不少于 8 位。
3. 修改成功后可要求用户重新登录。

------

## 9. 简历接口

## 9.1 上传简历

### 基本信息

```text
POST /api/resumes/upload
```

是否需要登录：是

Content-Type：`multipart/form-data`

### 请求参数

| 参数  | 类型   | 必填 | 说明                       |
| ----- | ------ | ---- | -------------------------- |
| file  | file   | 是   | 简历文件                   |
| title | string | 否   | 简历名称，不传则使用文件名 |

支持文件类型：

- PDF
- DOCX
- TXT

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "上传成功",
  "data": {
    "resume_id": "uuid",
    "title": "Python 后端开发简历",
    "file_name": "resume.pdf",
    "file_type": "pdf",
    "file_size": 204800,
    "parse_status": "success"
  }
}
```

### 业务规则

1. 文件大小不得超过系统配置上限。
2. 文件类型必须在允许范围内。
3. 文件保存到服务器持久化目录。
4. 解析文本保存到 `raw_text`。
5. 解析失败时保留文件记录，并返回 `parse_status = failed`。

------

## 9.2 获取简历列表

### 基本信息

```text
GET /api/resumes
```

是否需要登录：是

### Query 参数

| 参数      | 类型    | 必填 | 说明         |
| --------- | ------- | ---- | ------------ |
| page      | integer | 否   | 页码         |
| page_size | integer | 否   | 每页数量     |
| keyword   | string  | 否   | 简历名称搜索 |
| status    | string  | 否   | 状态筛选     |

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "title": "Python 后端开发简历",
        "file_name": "resume.pdf",
        "file_type": "pdf",
        "file_size": 204800,
        "parse_status": "success",
        "version": 1,
        "is_default": true,
        "created_at": "2026-05-07T10:30:00+08:00"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

说明：

列表接口不返回 `raw_text` 和完整 `structured_data`，避免大字段影响性能。

------

## 9.3 获取简历详情

### 基本信息

```text
GET /api/resumes/{resume_id}
```

是否需要登录：是

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "id": "uuid",
    "title": "Python 后端开发简历",
    "file_name": "resume.pdf",
    "file_type": "pdf",
    "file_size": 204800,
    "raw_text": "简历解析文本...",
    "structured_data": {},
    "parse_status": "success",
    "version": 1,
    "is_default": true,
    "created_at": "2026-05-07T10:30:00+08:00",
    "updated_at": "2026-05-07T10:30:00+08:00"
  }
}
```

### 业务规则

1. 只能查看当前用户自己的简历。
2. 管理员查看用户简历应走管理后台接口，并记录操作日志。

------

## 9.4 更新简历信息

### 基本信息

```text
PATCH /api/resumes/{resume_id}
```

是否需要登录：是

### 请求参数

```json
{
  "title": "后端开发工程师简历",
  "is_default": true
}
```

### 业务规则

1. 用户只能修改自己的简历。
2. 设置某份简历为默认时，需要取消该用户其他默认简历。

------

## 9.5 删除简历

### 基本信息

```text
DELETE /api/resumes/{resume_id}
```

是否需要登录：是

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "删除成功",
  "data": null
}
```

### 业务规则

1. 默认采用软删除。
2. 删除后普通列表不再展示。
3. 可根据策略同步删除原始文件。

------

## 9.6 重新解析简历

### 基本信息

```text
POST /api/resumes/{resume_id}/parse
```

是否需要登录：是

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "解析完成",
  "data": {
    "resume_id": "uuid",
    "parse_status": "success"
  }
}
```

------

## 10. 岗位描述接口

## 10.1 创建岗位描述

### 基本信息

```text
POST /api/jobs
```

是否需要登录：是

### 请求参数

```json
{
  "title": "Python 后端开发工程师",
  "company_name": "某某科技有限公司",
  "industry": "互联网",
  "location": "上海",
  "salary_range": "15k-25k",
  "description_text": "岗位职责：负责后端 API 开发..."
}
```

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "创建成功",
  "data": {
    "job_id": "uuid",
    "title": "Python 后端开发工程师",
    "parse_status": "success"
  }
}
```

------

## 10.2 获取岗位描述列表

### 基本信息

```text
GET /api/jobs
```

是否需要登录：是

### Query 参数

| 参数      | 类型    | 必填 | 说明           |
| --------- | ------- | ---- | -------------- |
| page      | integer | 否   | 页码           |
| page_size | integer | 否   | 每页数量       |
| keyword   | string  | 否   | 岗位或公司搜索 |

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "title": "Python 后端开发工程师",
        "company_name": "某某科技有限公司",
        "industry": "互联网",
        "location": "上海",
        "parse_status": "success",
        "created_at": "2026-05-07T10:30:00+08:00"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

------

## 10.3 获取岗位描述详情

### 基本信息

```text
GET /api/jobs/{job_id}
```

是否需要登录：是

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "id": "uuid",
    "title": "Python 后端开发工程师",
    "company_name": "某某科技有限公司",
    "industry": "互联网",
    "location": "上海",
    "salary_range": "15k-25k",
    "description_text": "岗位职责：负责后端 API 开发...",
    "structured_data": {
      "required_skills": ["Python", "FastAPI", "PostgreSQL"],
      "keywords": ["Python", "RESTful API", "Docker"]
    },
    "parse_status": "success"
  }
}
```

------

## 10.4 更新岗位描述

### 基本信息

```text
PUT /api/jobs/{job_id}
```

是否需要登录：是

### 请求参数

```json
{
  "title": "高级 Python 后端开发工程师",
  "company_name": "某某科技有限公司",
  "industry": "互联网",
  "location": "上海",
  "salary_range": "20k-30k",
  "description_text": "更新后的岗位描述..."
}
```

### 业务规则

更新岗位描述正文后，应重新解析岗位结构化信息。

------

## 10.5 删除岗位描述

### 基本信息

```text
DELETE /api/jobs/{job_id}
```

是否需要登录：是

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "删除成功",
  "data": null
}
```

------

## 10.6 重新解析岗位描述

### 基本信息

```text
POST /api/jobs/{job_id}/parse
```

是否需要登录：是

------

## 11. 分析任务接口

## 11.1 创建分析任务

### 基本信息

```text
POST /api/analysis/tasks
```

是否需要登录：是

### 请求参数

```json
{
  "resume_id": "uuid",
  "job_description_id": "uuid",
  "task_type": "full_analysis"
}
```

| 参数               | 类型   | 必填 | 说明                                 |
| ------------------ | ------ | ---- | ------------------------------------ |
| resume_id          | string | 是   | 简历 ID                              |
| job_description_id | string | 否   | 岗位描述 ID                          |
| task_type          | string | 是   | resume_score/job_match/full_analysis |

### 响应示例：同步模式

```json
{
  "success": true,
  "code": 0,
  "message": "分析完成",
  "data": {
    "task_id": "uuid",
    "status": "success",
    "report_id": "uuid"
  }
}
```

### 响应示例：异步模式

```json
{
  "success": true,
  "code": 0,
  "message": "任务已创建",
  "data": {
    "task_id": "uuid",
    "status": "pending"
  }
}
```

### 业务规则

1. 用户只能选择自己的简历和岗位描述。
2. `job_match` 和 `full_analysis` 建议必须提供岗位描述。
3. 任务创建后记录到 `analysis_tasks` 表。
4. 一期可同步执行，后续可改为异步执行。
5. AI 调用失败时任务状态更新为 `failed`。

------

## 11.2 获取分析任务状态

### 基本信息

```text
GET /api/analysis/tasks/{task_id}
```

是否需要登录：是

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "task_id": "uuid",
    "task_type": "full_analysis",
    "status": "running",
    "progress": 60,
    "error_message": null,
    "report_id": null,
    "created_at": "2026-05-07T10:30:00+08:00",
    "started_at": "2026-05-07T10:30:05+08:00",
    "finished_at": null
  }
}
```

### 业务规则

1. 用户只能查询自己的任务。
2. 如果任务成功且报告已生成，返回 `report_id`。
3. 前端可通过该接口轮询任务状态。

------

## 11.3 获取分析任务列表

### 基本信息

```text
GET /api/analysis/tasks
```

是否需要登录：是

### Query 参数

| 参数      | 类型    | 必填 | 说明     |
| --------- | ------- | ---- | -------- |
| page      | integer | 否   | 页码     |
| page_size | integer | 否   | 每页数量 |
| status    | string  | 否   | 任务状态 |
| task_type | string  | 否   | 任务类型 |

------

## 11.4 取消分析任务，可选

### 基本信息

```text
POST /api/analysis/tasks/{task_id}/cancel
```

是否需要登录：是

### 业务规则

1. 只有 pending 或 running 状态任务可以取消。
2. 同步执行模式下该接口可暂不实现。
3. 异步任务模式下可更新状态为 `canceled`。

------

## 12. 分析报告接口

## 12.1 获取报告列表

### 基本信息

```text
GET /api/reports
```

是否需要登录：是

### Query 参数

| 参数               | 类型    | 必填 | 说明       |
| ------------------ | ------- | ---- | ---------- |
| page               | integer | 否   | 页码       |
| page_size          | integer | 否   | 每页数量   |
| resume_id          | string  | 否   | 按简历筛选 |
| job_description_id | string  | 否   | 按岗位筛选 |

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "task_id": "uuid",
        "resume_title": "Python 后端开发简历",
        "job_title": "Python 后端开发工程师",
        "total_score": 82,
        "match_score": 76,
        "summary": "简历整体较完整，但岗位关键词覆盖仍有提升空间。",
        "created_at": "2026-05-07T10:30:00+08:00"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

------

## 12.2 获取报告详情

### 基本信息

```text
GET /api/reports/{report_id}
```

是否需要登录：是

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "id": "uuid",
    "task_id": "uuid",
    "resume_id": "uuid",
    "job_description_id": "uuid",
    "total_score": 82,
    "match_score": 76,
    "summary": "简历整体较完整，但岗位关键词覆盖仍有提升空间。",
    "report_data": {
      "total_score": 82,
      "match_score": 76,
      "score_breakdown": {
        "completeness": 18,
        "structure": 13,
        "professional_expression": 16,
        "experience_quality": 17,
        "skill_match": 11,
        "quantified_results": 7
      },
      "strengths": [],
      "weaknesses": [],
      "matched_keywords": [],
      "missing_keywords": [],
      "suggestions": [],
      "rewrite_examples": [],
      "risk_notes": []
    },
    "model_provider": "deepseek",
    "model_name": "deepseek-chat",
    "created_at": "2026-05-07T10:30:00+08:00"
  }
}
```

### 业务规则

1. 用户只能查看自己的报告。
2. 报告详情包含完整 `report_data`。
3. 列表接口只返回摘要字段。

------

## 12.3 删除报告，可选

### 基本信息

```text
DELETE /api/reports/{report_id}
```

是否需要登录：是

说明：

一期可不提供报告删除功能，或者只允许用户删除自己的报告展示记录。

------

## 13. Dashboard 工作台接口

## 13.1 获取用户工作台统计

### 基本信息

```text
GET /api/dashboard/summary
```

是否需要登录：是

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "resume_count": 3,
    "job_count": 5,
    "analysis_count": 12,
    "latest_report": {
      "id": "uuid",
      "total_score": 82,
      "match_score": 76,
      "created_at": "2026-05-07T10:30:00+08:00"
    }
  }
}
```

------

## 14. 管理后台接口

## 14.1 获取用户列表

### 基本信息

```text
GET /api/admin/users
```

是否需要登录：是

是否需要管理员权限：是

### Query 参数

| 参数      | 类型    | 必填 | 说明           |
| --------- | ------- | ---- | -------------- |
| page      | integer | 否   | 页码           |
| page_size | integer | 否   | 每页数量       |
| keyword   | string  | 否   | 邮箱或昵称搜索 |
| status    | string  | 否   | 用户状态       |

------

## 14.2 获取用户详情

### 基本信息

```text
GET /api/admin/users/{user_id}
```

是否需要管理员权限：是

------

## 14.3 更新用户状态

### 基本信息

```text
PATCH /api/admin/users/{user_id}/status
```

是否需要管理员权限：是

### 请求参数

```json
{
  "status": "disabled"
}
```

### 业务规则

1. 管理员不能禁用自己。
2. 操作需要写入管理员操作日志。

------

## 14.4 获取简历记录列表

### 基本信息

```text
GET /api/admin/resumes
```

是否需要管理员权限：是

### Query 参数

| 参数         | 类型    | 必填 | 说明     |
| ------------ | ------- | ---- | -------- |
| page         | integer | 否   | 页码     |
| page_size    | integer | 否   | 每页数量 |
| user_id      | string  | 否   | 用户 ID  |
| parse_status | string  | 否   | 解析状态 |

说明：

管理员列表接口默认不返回完整简历原文。

------

## 14.5 管理员查看简历详情

### 基本信息

```text
GET /api/admin/resumes/{resume_id}
```

是否需要管理员权限：是

### 业务规则

1. 管理员查看简历原文必须记录操作日志。
2. 可根据系统配置决定是否允许管理员查看完整简历原文。

------

## 14.6 获取分析任务列表

### 基本信息

```text
GET /api/admin/analysis-tasks
```

是否需要管理员权限：是

### Query 参数

| 参数      | 类型    | 必填 | 说明     |
| --------- | ------- | ---- | -------- |
| page      | integer | 否   | 页码     |
| page_size | integer | 否   | 每页数量 |
| status    | string  | 否   | 任务状态 |
| task_type | string  | 否   | 任务类型 |
| user_id   | string  | 否   | 用户 ID  |

------

## 14.7 获取 API 调用日志

### 基本信息

```text
GET /api/admin/api-logs
```

是否需要管理员权限：是

### Query 参数

| 参数       | 类型    | 必填 | 说明           |
| ---------- | ------- | ---- | -------------- |
| page       | integer | 否   | 页码           |
| page_size  | integer | 否   | 每页数量       |
| scene      | string  | 否   | 调用场景       |
| status     | string  | 否   | success/failed |
| start_time | string  | 否   | 开始时间       |
| end_time   | string  | 否   | 结束时间       |

------

## 14.8 获取 Prompt 模板列表

### 基本信息

```text
GET /api/admin/prompt-templates
```

是否需要管理员权限：是

------

## 14.9 创建 Prompt 模板

### 基本信息

```text
POST /api/admin/prompt-templates
```

是否需要管理员权限：是

### 请求参数

```json
{
  "name": "完整分析报告模板",
  "scene": "full_analysis",
  "content": "你是专业简历分析助手...",
  "description": "用于生成完整简历分析报告"
}
```

------

## 14.10 更新 Prompt 模板

### 基本信息

```text
PUT /api/admin/prompt-templates/{template_id}
```

是否需要管理员权限：是

### 业务规则

1. 修改 Prompt 模板应生成新版本或更新版本号。
2. 操作需要记录管理员操作日志。

------

## 14.11 启用或停用 Prompt 模板

### 基本信息

```text
PATCH /api/admin/prompt-templates/{template_id}/status
```

是否需要管理员权限：是

### 请求参数

```json
{
  "status": "inactive"
}
```

------

## 14.12 获取后台统计数据

### 基本信息

```text
GET /api/admin/dashboard/summary
```

是否需要管理员权限：是

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "data": {
    "user_count": 100,
    "resume_count": 230,
    "job_count": 180,
    "analysis_task_count": 520,
    "today_api_call_count": 36,
    "failed_task_count": 4
  }
}
```

------

## 15. 文件访问接口设计

## 15.1 下载原始简历文件，可选

### 基本信息

```text
GET /api/resumes/{resume_id}/download
```

是否需要登录：是

### 业务规则

1. 普通用户只能下载自己的简历。
2. 管理员下载用户简历需要记录操作日志。
3. 文件路径不得直接暴露给前端。
4. 后端应通过安全方式读取文件并返回。

------

## 16. 健康检查接口

## 16.1 服务健康检查

### 基本信息

```text
GET /api/health
```

是否需要登录：否

### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "ok",
  "data": {
    "service": "resume-analyzer-backend",
    "status": "healthy",
    "version": "1.0.0"
  }
}
```

------

## 17. 前端调用约定

### 17.1 Axios Base URL

开发环境：

```text
VITE_API_BASE_URL=http://localhost:8000/api
```

生产环境：

```text
VITE_API_BASE_URL=/api
```

### 17.2 Token 处理

前端登录后保存 Token。

推荐保存位置：

- localStorage，开发简单。
- httpOnly Cookie，安全性更好，后续可升级。

一期建议：

```text
localStorage + Axios 请求拦截器
```

Axios 请求拦截器统一添加：

```text
Authorization: Bearer {token}
```

### 17.3 统一错误处理

前端应对以下错误统一处理：

| 错误  | 前端处理               |
| ----- | ---------------------- |
| 401   | 清除 Token，跳转登录页 |
| 403   | 提示无权限             |
| 404   | 提示资源不存在         |
| 413   | 提示文件过大           |
| 415   | 提示文件类型不支持     |
| 500   | 提示系统异常           |
| 50010 | 提示 AI 服务暂不可用   |

------

## 18. 接口安全要求

### 18.1 权限校验

所有用户资源接口必须校验资源归属。

示例：

用户访问：

```text
GET /api/resumes/{resume_id}
```

后端必须校验：

```text
resume.user_id == current_user.id
```

### 18.2 防止敏感信息泄露

接口响应不得返回：

- password_hash
- DeepSeek API Key
- 服务器绝对文件路径
- 系统内部堆栈
- 未脱敏的敏感日志

### 18.3 文件上传安全

文件上传接口必须校验：

1. 文件后缀。
2. MIME 类型。
3. 文件大小。
4. 文件名安全性。
5. 文件保存路径。

### 18.4 AI 调用安全

AI 分析接口应注意：

1. 用户输入内容需要作为数据处理，不应覆盖系统 Prompt。
2. Prompt 应明确要求不得编造经历。
3. 日志不记录完整简历和完整岗位描述。
4. 控制输入长度，避免超长请求。

------

## 19. FastAPI 路由文件建议

后端路由文件建议如下：

```text
backend/app/api/auth.py
backend/app/api/users.py
backend/app/api/resumes.py
backend/app/api/jobs.py
backend/app/api/analysis.py
backend/app/api/reports.py
backend/app/api/dashboard.py
backend/app/api/admin.py
backend/app/api/health.py
```

在 `main.py` 中统一注册：

```python
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(resume_router, prefix="/api/resumes", tags=["Resumes"])
app.include_router(job_router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(analysis_router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(report_router, prefix="/api/reports", tags=["Reports"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
app.include_router(health_router, prefix="/api/health", tags=["Health"])
```

------

## 20. MVP 接口范围

一期 MVP 必须实现以下接口：

### 认证与用户

1. POST /api/auth/register
2. POST /api/auth/login
3. GET /api/auth/me
4. PUT /api/users/me

### 简历

1. POST /api/resumes/upload
2. GET /api/resumes
3. GET /api/resumes/{resume_id}
4. DELETE /api/resumes/{resume_id}

### 岗位

1. POST /api/jobs
2. GET /api/jobs
3. GET /api/jobs/{job_id}
4. DELETE /api/jobs/{job_id}

### 分析与报告

1. POST /api/analysis/tasks
2. GET /api/analysis/tasks/{task_id}
3. GET /api/reports
4. GET /api/reports/{report_id}

### 工作台

1. GET /api/dashboard/summary

### 管理后台

1. GET /api/admin/users
2. GET /api/admin/analysis-tasks
3. GET /api/admin/api-logs
4. GET /api/admin/prompt-templates
5. POST /api/admin/prompt-templates
6. PUT /api/admin/prompt-templates/{template_id}

### 健康检查

1. GET /api/health

------

## 21. 后续扩展接口

后续可扩展：

1. 报告导出 PDF。
2. 简历在线编辑。
3. 简历版本对比。
4. 求职信生成。
5. 模拟面试问题生成。
6. 多模型切换。
7. 用户调用次数限制。
8. 会员或付费接口。
9. 企业端批量简历筛选。

------

## 22. 总结

本文档定义了简历分析系统后端 API 的整体设计方案。系统采用统一 JSON 响应格式、JWT 鉴权、RESTful 接口风格和清晰的模块划分。

一期开发应优先实现用户认证、简历上传、岗位描述、分析任务、分析报告和基础管理后台接口，确保前端能够完成完整业务闭环。后续可根据功能扩展逐步增加异步任务、报告导出、多模型支持和更复杂的管理能力。