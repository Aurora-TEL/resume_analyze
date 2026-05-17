# DeepSeek Prompt 模板设计文档

## 1. 文档说明

### 1.1 文档目的

本文档用于定义简历分析系统中 DeepSeek API 的 Prompt 模板设计方案，覆盖简历解析、岗位解析、简历评分、岗位匹配度分析、关键词分析、优化建议生成和简历改写示例生成等核心 AI 场景。

本文档主要面向：

- 后端开发人员
- AI 服务封装开发人员
- Prompt 模板维护人员
- 测试人员
- 管理后台维护人员

### 1.2 设计目标

Prompt 模板设计需要满足以下目标：

1. 输出结构稳定，便于后端解析和入库。
2. 尽量减少模型自由发挥，避免生成无法校验的长文本。
3. 所有输出优先使用 JSON 格式。
4. 对无法判断的信息返回 `null`、空数组或“不确定”，不得编造。
5. 所有评分、匹配度和建议必须可解释。
6. 简历优化建议必须基于用户已有内容，不得引导用户虚构经历。
7. 支持后续通过数据库表 `prompt_templates` 进行版本化管理。

### 1.3 适用模型

一期建议使用：

```text
DeepSeek Chat 模型
```

后端通过统一 AI 服务层封装模型调用，不建议业务模块直接调用 DeepSeek API。

------

## 2. 通用 Prompt 设计规范

### 2.1 通用系统角色设定

所有简历分析类 Prompt 建议使用以下系统角色作为基础约束：

```text
你是一名专业的中文简历分析顾问、招聘 JD 分析专家和职业发展顾问。
你需要基于用户提供的简历文本和岗位描述进行结构化分析。
你的回答必须客观、谨慎、可执行，不得编造用户不存在的经历、技能、数据、项目或证书。
如果输入信息不足，请返回 null、空数组或“不确定”，并在说明中指出缺失信息。
除非特别要求，必须返回合法 JSON，不要输出 Markdown、解释性前言或代码块标记。
```

### 2.2 通用输入变量

| 变量名                   | 说明                         |
| ------------------------ | ---------------------------- |
| `resume_text`            | 简历原始文本                 |
| `resume_structured_data` | 已解析的结构化简历数据，可选 |
| `job_text`               | 岗位描述原文                 |
| `job_structured_data`    | 已解析的结构化岗位数据，可选 |
| `target_position`        | 用户目标岗位，可选           |
| `user_profile`           | 用户基础信息，可选           |
| `language`               | 输出语言，默认 `zh-CN`       |
| `schema_version`         | 输出 JSON 结构版本           |

### 2.3 通用输出要求

所有 Prompt 输出必须满足：

1. 只返回 JSON 对象。
2. 不要使用 Markdown 代码块。
3. 不要输出 JSON 之外的解释文字。
4. 字段名使用英文小写加下划线。
5. 数组字段即使无内容也返回空数组。
6. 数字评分必须在约定区间内。
7. 不确定的信息返回 `null` 或“不确定”。
8. 所有建议必须明确指出依据来源。

### 2.4 通用安全与合规约束

所有 Prompt 必须包含以下约束：

```text
禁止编造用户未提供的工作经历、项目经历、技能、学历、证书、奖项、数据指标或公司名称。
如果建议用户补充某项内容，必须使用“建议确认后补充”或“如果属实可补充”的表达。
不要输出歧视性、攻击性或不适合招聘场景的内容。
不要泄露或重复输出过多个人敏感信息，例如完整手机号、身份证号、详细住址等。
```

------

## 3. Prompt 模板总览

| scene               | 模板名称               | 使用场景                     | 是否需要岗位描述 |
| ------------------- | ---------------------- | ---------------------------- | ---------------- |
| `resume_parse`      | 简历结构化解析模板     | 上传简历后提取结构化信息     | 否               |
| `job_parse`         | 岗位描述结构化解析模板 | 新建岗位描述后提取岗位要求   | 是               |
| `resume_score`      | 简历评分模板           | 对简历进行基础质量评分       | 否，可选         |
| `job_match`         | 岗位匹配度分析模板     | 分析简历与岗位适配程度       | 是               |
| `keyword_analysis`  | 关键词覆盖分析模板     | 分析 JD 关键词与简历覆盖情况 | 是               |
| `resume_suggestion` | 简历优化建议模板       | 生成分模块修改建议           | 可选，建议提供   |
| `rewrite_example`   | 简历改写示例模板       | 对简历句子或经历生成改写示例 | 可选，建议提供   |
| `full_analysis`     | 完整分析报告模板       | 一次性生成完整报告           | 是               |

------

# 4. 简历结构化解析 Prompt

## 4.1 使用场景

当用户上传 PDF、DOCX 或 TXT 简历后，后端先将文件解析为纯文本，再调用该 Prompt 将简历文本转换为结构化 JSON。

适用接口或任务：

```text
POST /api/resumes/upload
POST /api/resumes/{resume_id}/parse
```

适用模板场景：

```text
resume_parse
```

## 4.2 输入变量

```json
{
  "resume_text": "{{resume_text}}",
  "target_position": "{{target_position}}",
  "language": "zh-CN",
  "schema_version": "1.0"
}
```

## 4.3 Prompt 模板

```text
你是一名专业的中文简历解析专家。请从用户提供的简历原文中提取结构化信息。

你必须遵守以下规则：
1. 只根据简历原文提取信息，不得编造。
2. 如果某字段在简历中不存在，请返回 null 或空数组。
3. 保留原文中的关键信息，但可进行轻微清洗，例如去除多余空格、统一日期格式。
4. 日期尽量转换为 YYYY-MM 或 YYYY-MM-DD；如果无法判断，保留原文。
5. 手机号、邮箱等敏感信息可以提取，但不要额外扩写。
6. 输出必须是合法 JSON，不要输出 Markdown 或解释文字。

请按照以下 JSON 结构返回：

{
  "schema_version": "1.0",
  "basic_info": {
    "name": null,
    "gender": null,
    "email": null,
    "phone": null,
    "location": null,
    "target_position": null,
    "work_years": null,
    "personal_website": null,
    "github": null,
    "linkedin": null
  },
  "education": [
    {
      "school": null,
      "degree": null,
      "major": null,
      "start_date": null,
      "end_date": null,
      "description": []
    }
  ],
  "work_experience": [
    {
      "company": null,
      "position": null,
      "department": null,
      "start_date": null,
      "end_date": null,
      "responsibilities": [],
      "achievements": [],
      "technologies": []
    }
  ],
  "project_experience": [
    {
      "name": null,
      "role": null,
      "start_date": null,
      "end_date": null,
      "background": null,
      "responsibilities": [],
      "achievements": [],
      "technologies": [],
      "project_scale": null
    }
  ],
  "skills": {
    "programming_languages": [],
    "frameworks": [],
    "databases": [],
    "tools": [],
    "cloud_or_devops": [],
    "domain_skills": [],
    "soft_skills": [],
    "other_skills": []
  },
  "certificates": [],
  "awards": [],
  "languages": [],
  "self_evaluation": null,
  "other_sections": [
    {
      "title": null,
      "content": []
    }
  ],
  "parse_quality": {
    "is_readable": true,
    "missing_core_sections": [],
    "possible_parse_errors": [],
    "confidence": 0.0
  }
}

简历原文如下：
{{resume_text}}

用户目标岗位，可选：
{{target_position}}
```

## 4.4 输出字段说明

| 字段                 | 说明         |
| -------------------- | ------------ |
| `basic_info`         | 基础信息     |
| `education`          | 教育经历     |
| `work_experience`    | 工作经历     |
| `project_experience` | 项目经历     |
| `skills`             | 技能分类     |
| `certificates`       | 证书         |
| `awards`             | 奖项         |
| `parse_quality`      | 解析质量判断 |

## 4.5 后端校验规则

1. 返回内容必须能被 JSON 解析。
2. `schema_version` 必须存在。
3. `parse_quality.confidence` 必须为 0 到 1 之间的数字。
4. `education`、`work_experience`、`project_experience`、`certificates`、`awards` 必须是数组。
5. 如果模型返回 Markdown 代码块，后端应先尝试提取 JSON。

------

# 5. 岗位描述结构化解析 Prompt

## 5.1 使用场景

当用户创建岗位描述后，系统调用该 Prompt 解析岗位职责、技能要求、经验要求、关键词等内容。

适用接口或任务：

```text
POST /api/jobs
POST /api/jobs/{job_id}/parse
```

适用模板场景：

```text
job_parse
```

## 5.2 输入变量

```json
{
  "job_title": "{{job_title}}",
  "company_name": "{{company_name}}",
  "industry": "{{industry}}",
  "job_text": "{{job_text}}",
  "language": "zh-CN",
  "schema_version": "1.0"
}
```

## 5.3 Prompt 模板

```text
你是一名专业的招聘岗位 JD 解析专家。请从用户提供的岗位描述中提取结构化岗位要求。

你必须遵守以下规则：
1. 只基于岗位描述原文提取信息，不得编造。
2. 将岗位要求拆分为必备技能、加分技能、软技能、经验要求、学历要求和关键词。
3. 如果岗位描述中没有明确说明某项要求，请返回 null 或空数组。
4. 关键词应优先提取对简历筛选有影响的技术、工具、业务领域、经验年限、学历和能力要求。
5. 输出必须是合法 JSON，不要输出 Markdown 或解释文字。

请按照以下 JSON 结构返回：

{
  "schema_version": "1.0",
  "job_basic_info": {
    "title": null,
    "company_name": null,
    "industry": null,
    "location": null,
    "salary_range": null,
    "seniority_level": null,
    "employment_type": null
  },
  "core_responsibilities": [],
  "required_skills": [],
  "preferred_skills": [],
  "technical_skills": {
    "programming_languages": [],
    "frameworks": [],
    "databases": [],
    "tools": [],
    "cloud_or_devops": [],
    "testing": [],
    "other": []
  },
  "soft_skills": [],
  "experience_requirement": {
    "years_min": null,
    "years_max": null,
    "description": null
  },
  "education_requirement": {
    "degree": null,
    "major": null,
    "description": null
  },
  "industry_background_requirement": [],
  "certification_requirement": [],
  "keywords": [
    {
      "keyword": null,
      "category": null,
      "importance": "medium",
      "evidence": null
    }
  ],
  "priority_weights": {
    "skills": 0.35,
    "experience": 0.25,
    "projects": 0.20,
    "education": 0.10,
    "soft_skills": 0.10
  },
  "parse_quality": {
    "is_complete_jd": true,
    "missing_sections": [],
    "confidence": 0.0
  }
}

岗位基本信息：
岗位名称：{{job_title}}
公司名称：{{company_name}}
行业：{{industry}}

岗位描述原文如下：
{{job_text}}
```

## 5.4 输出字段说明

| 字段                    | 说明                 |
| ----------------------- | -------------------- |
| `core_responsibilities` | 岗位核心职责         |
| `required_skills`       | 必备技能             |
| `preferred_skills`      | 加分技能             |
| `technical_skills`      | 技术能力分类         |
| `keywords`              | 关键词列表           |
| `priority_weights`      | 匹配分析可参考的权重 |
| `parse_quality`         | JD 完整性判断        |

## 5.5 后端校验规则

1. `keywords` 必须是数组。
2. `importance` 只能是 `high`、`medium`、`low`。
3. `priority_weights` 中各项权重建议总和为 1，若偏差过大，后端可使用默认权重覆盖。
4. `experience_requirement.years_min` 和 `years_max` 必须为数字或 null。

------

# 6. 简历基础评分 Prompt

## 6.1 使用场景

用于不依赖特定岗位或弱依赖目标岗位的简历基础质量评分。

适用任务类型：

```text
resume_score
```

适用模板场景：

```text
resume_score
```

## 6.2 评分维度

总分 100 分，建议维度如下：

| 维度       | 分值 | 说明                                               |
| ---------- | ---- | -------------------------------------------------- |
| 信息完整性 | 20   | 是否包含教育、经历、项目、技能、联系方式等核心信息 |
| 结构清晰度 | 15   | 模块是否清楚，层级是否合理                         |
| 表达专业度 | 20   | 是否使用专业、具体、结果导向的表达                 |
| 经历含金量 | 20   | 工作与项目经历是否体现能力和成果                   |
| 技能匹配度 | 15   | 技能是否与目标岗位相关                             |
| 量化成果   | 10   | 是否有数据化结果、指标或业务影响                   |

## 6.3 输入变量

```json
{
  "resume_text": "{{resume_text}}",
  "resume_structured_data": {{resume_structured_data}},
  "target_position": "{{target_position}}",
  "language": "zh-CN",
  "schema_version": "1.0"
}
```

## 6.4 Prompt 模板

```text
你是一名专业的中文简历评估专家。请基于用户提供的简历内容，对简历基础质量进行评分。

评分总分为 100 分，必须严格按照以下维度评分：
1. completeness 信息完整性：20 分
2. structure 结构清晰度：15 分
3. professional_expression 表达专业度：20 分
4. experience_quality 经历含金量：20 分
5. skill_relevance 技能相关度：15 分
6. quantified_results 量化成果：10 分

你必须遵守以下规则：
1. 评分必须基于简历已有内容，不得臆测。
2. 每个维度必须给出得分、扣分原因和改进建议。
3. 总分必须等于各维度得分之和。
4. 如果目标岗位为空，则技能相关度按简历内部目标方向和技能一致性评分。
5. 输出必须是合法 JSON，不要输出 Markdown 或解释文字。

请按照以下 JSON 结构返回：

{
  "schema_version": "1.0",
  "total_score": 0,
  "grade": null,
  "score_breakdown": {
    "completeness": {
      "score": 0,
      "max_score": 20,
      "reason": null,
      "deductions": [],
      "suggestions": []
    },
    "structure": {
      "score": 0,
      "max_score": 15,
      "reason": null,
      "deductions": [],
      "suggestions": []
    },
    "professional_expression": {
      "score": 0,
      "max_score": 20,
      "reason": null,
      "deductions": [],
      "suggestions": []
    },
    "experience_quality": {
      "score": 0,
      "max_score": 20,
      "reason": null,
      "deductions": [],
      "suggestions": []
    },
    "skill_relevance": {
      "score": 0,
      "max_score": 15,
      "reason": null,
      "deductions": [],
      "suggestions": []
    },
    "quantified_results": {
      "score": 0,
      "max_score": 10,
      "reason": null,
      "deductions": [],
      "suggestions": []
    }
  },
  "main_strengths": [],
  "main_problems": [],
  "priority_suggestions": [
    {
      "priority": "high",
      "module": null,
      "problem": null,
      "suggestion": null,
      "expected_impact": null
    }
  ],
  "risk_notes": []
}

评分等级规则：
- 90-100：excellent
- 80-89：good
- 70-79：fair
- 60-69：weak
- 0-59：poor

简历结构化数据：
{{resume_structured_data}}

简历原文：
{{resume_text}}

目标岗位，可选：
{{target_position}}
```

## 6.5 后端校验规则

1. `total_score` 必须为 0 到 100 的数字。
2. 各维度得分不能超过对应 `max_score`。
3. 各维度得分之和应等于 `total_score`，误差超过 1 分时以后端重新求和为准。
4. `priority` 只能是 `high`、`medium`、`low`。
5. `grade` 只能是 `excellent`、`good`、`fair`、`weak`、`poor`。

------

# 7. 岗位匹配度分析 Prompt

## 7.1 使用场景

用于分析一份简历与目标岗位描述之间的匹配程度，并输出匹配项、缺失项、风险项和强化建议。

适用任务类型：

```text
job_match
full_analysis
```

适用模板场景：

```text
job_match
```

## 7.2 匹配维度

建议总匹配度为 100%，维度如下：

| 维度             | 权重 | 说明                               |
| ---------------- | ---- | ---------------------------------- |
| 技能匹配         | 30%  | 必备技能、技术栈、工具匹配情况     |
| 工作经验匹配     | 20%  | 年限、岗位职责、工作内容匹配情况   |
| 项目经验匹配     | 20%  | 项目类型、复杂度、成果与岗位相关性 |
| 行业背景匹配     | 10%  | 行业经验或业务理解匹配情况         |
| 关键词覆盖       | 10%  | JD 核心关键词在简历中的覆盖情况    |
| 软技能与学历证书 | 10%  | 沟通协作、学历、证书等匹配情况     |

## 7.3 输入变量

```json
{
  "resume_text": "{{resume_text}}",
  "resume_structured_data": {{resume_structured_data}},
  "job_text": "{{job_text}}",
  "job_structured_data": {{job_structured_data}},
  "language": "zh-CN",
  "schema_version": "1.0"
}
```

## 7.4 Prompt 模板

```text
你是一名专业的招聘匹配分析专家。请基于用户简历和目标岗位描述，分析简历与岗位之间的匹配程度。

你必须遵守以下规则：
1. 匹配分析必须同时参考简历内容和岗位描述。
2. 不得因为简历没有写出某项技能就直接认定用户完全不会，只能判断“简历未体现”。
3. 缺失项应区分“明确缺失”和“未体现，需确认”。
4. 优化建议必须基于真实经历，不得建议用户虚构技能或项目。
5. 总体匹配度为 0 到 100 的数字。
6. 输出必须是合法 JSON，不要输出 Markdown 或解释文字。

请按照以下 JSON 结构返回：

{
  "schema_version": "1.0",
  "overall_match_score": 0,
  "match_level": null,
  "dimension_scores": {
    "skill_match": {
      "score": 0,
      "weight": 0.30,
      "reason": null,
      "matched_items": [],
      "missing_items": [],
      "uncertain_items": []
    },
    "work_experience_match": {
      "score": 0,
      "weight": 0.20,
      "reason": null,
      "matched_items": [],
      "missing_items": [],
      "uncertain_items": []
    },
    "project_experience_match": {
      "score": 0,
      "weight": 0.20,
      "reason": null,
      "matched_items": [],
      "missing_items": [],
      "uncertain_items": []
    },
    "industry_background_match": {
      "score": 0,
      "weight": 0.10,
      "reason": null,
      "matched_items": [],
      "missing_items": [],
      "uncertain_items": []
    },
    "keyword_coverage_match": {
      "score": 0,
      "weight": 0.10,
      "reason": null,
      "matched_items": [],
      "missing_items": [],
      "uncertain_items": []
    },
    "soft_skill_education_match": {
      "score": 0,
      "weight": 0.10,
      "reason": null,
      "matched_items": [],
      "missing_items": [],
      "uncertain_items": []
    }
  },
  "matched_requirements": [
    {
      "requirement": null,
      "resume_evidence": null,
      "strength_level": "medium"
    }
  ],
  "missing_requirements": [
    {
      "requirement": null,
      "importance": "high",
      "missing_type": "not_shown",
      "explanation": null,
      "suggestion": null
    }
  ],
  "risk_items": [
    {
      "risk": null,
      "severity": "medium",
      "reason": null,
      "mitigation": null
    }
  ],
  "enhancement_opportunities": [
    {
      "module": null,
      "current_issue": null,
      "recommendation": null,
      "expected_impact": null
    }
  ],
  "summary": null
}

match_level 规则：
- 85-100：high_match
- 70-84：medium_high_match
- 55-69：medium_match
- 40-54：low_match
- 0-39：not_recommended

missing_type 取值：
- explicit_gap：岗位明确要求，但简历明显不满足
- not_shown：简历未体现，需要用户确认是否具备
- weak_evidence：简历有相关内容，但证据较弱

简历结构化数据：
{{resume_structured_data}}

简历原文：
{{resume_text}}

岗位结构化数据：
{{job_structured_data}}

岗位描述原文：
{{job_text}}
```

## 7.5 后端校验规则

1. `overall_match_score` 必须为 0 到 100。
2. `dimension_scores.*.score` 必须为 0 到 100。
3. `missing_type` 必须是 `explicit_gap`、`not_shown`、`weak_evidence`。
4. `severity` 和 `importance` 只能是 `high`、`medium`、`low`。

------

# 8. 关键词分析 Prompt

## 8.1 使用场景

用于从岗位描述中提取关键词，并检查简历中的覆盖情况，帮助用户优化简历关键词表达。

适用模板场景：

```text
keyword_analysis
```

## 8.2 输入变量

```json
{
  "resume_text": "{{resume_text}}",
  "job_text": "{{job_text}}",
  "job_structured_data": {{job_structured_data}},
  "language": "zh-CN",
  "schema_version": "1.0"
}
```

## 8.3 Prompt 模板

```text
你是一名 ATS 关键词分析专家和招聘 JD 分析专家。请从岗位描述中提取关键筛选词，并判断这些关键词是否已在简历中体现。

你必须遵守以下规则：
1. 关键词必须来自岗位描述或由岗位描述明确推导，不得随意扩展。
2. 判断覆盖时，需要区分完全覆盖、部分覆盖、同义表达覆盖和未覆盖。
3. 对未覆盖关键词，不得直接建议用户加入，除非提示“如果真实具备可补充”。
4. 关键词建议应服务于简历表达优化，而不是关键词堆砌。
5. 输出必须是合法 JSON，不要输出 Markdown 或解释文字。

请按照以下 JSON 结构返回：

{
  "schema_version": "1.0",
  "coverage_rate": 0,
  "keyword_summary": {
    "total_keywords": 0,
    "covered_count": 0,
    "partially_covered_count": 0,
    "missing_count": 0
  },
  "keywords": [
    {
      "keyword": null,
      "category": null,
      "importance": "medium",
      "coverage_status": "missing",
      "resume_evidence": null,
      "jd_evidence": null,
      "suggestion": null
    }
  ],
  "covered_keywords": [],
  "partially_covered_keywords": [],
  "missing_keywords": [
    {
      "keyword": null,
      "importance": "high",
      "reason": null,
      "safe_usage_suggestion": null
    }
  ],
  "synonym_suggestions": [
    {
      "jd_keyword": null,
      "resume_expression": null,
      "suggested_expression": null,
      "reason": null
    }
  ],
  "keyword_usage_advice": [
    {
      "module": null,
      "advice": null,
      "example": null,
      "risk_note": null
    }
  ],
  "risk_notes": []
}

coverage_status 取值：
- covered：简历中明确覆盖
- partially_covered：简历中部分体现
- synonym_covered：使用了同义表达
- missing：简历中未体现

关键词 category 建议取值：
- technical_skill
- framework
- database
- tool
- domain
- responsibility
- soft_skill
- education
- certificate
- experience
- other

简历原文：
{{resume_text}}

岗位结构化数据：
{{job_structured_data}}

岗位描述原文：
{{job_text}}
```

## 8.4 后端校验规则

1. `coverage_rate` 必须为 0 到 100。
2. `coverage_status` 必须在枚举范围内。
3. `keyword_summary.total_keywords` 应等于关键词数组长度。
4. 不允许输出“建议直接加入某技能”这类高风险建议，应转为“如果真实具备可补充”。

------

# 9. 简历优化建议 Prompt

## 9.1 使用场景

用于基于简历评分、岗位匹配度、关键词分析结果，生成具体、可执行的简历优化建议。

适用模板场景：

```text
resume_suggestion
```

## 9.2 输入变量

```json
{
  "resume_text": "{{resume_text}}",
  "resume_structured_data": {{resume_structured_data}},
  "job_text": "{{job_text}}",
  "job_structured_data": {{job_structured_data}},
  "score_result": {{score_result}},
  "match_result": {{match_result}},
  "keyword_result": {{keyword_result}},
  "language": "zh-CN",
  "schema_version": "1.0"
}
```

## 9.3 Prompt 模板

```text
你是一名专业的简历优化顾问。请基于用户简历、目标岗位、简历评分结果、岗位匹配结果和关键词分析结果，生成具体、可执行的简历优化建议。

你必须遵守以下规则：
1. 建议必须具体到简历模块、问题、修改方向和示例表达方式。
2. 不得建议用户编造不存在的经历、项目、技能、证书或数据。
3. 对用户未明确提供但可能有的信息，必须使用“如果属实可补充”或“建议确认后补充”。
4. 优先输出影响投递成功率最大的建议。
5. 建议应按 high、medium、low 优先级分组。
6. 输出必须是合法 JSON，不要输出 Markdown 或解释文字。

请按照以下 JSON 结构返回：

{
  "schema_version": "1.0",
  "overall_strategy": null,
  "suggestions": [
    {
      "priority": "high",
      "module": null,
      "problem": null,
      "evidence": null,
      "suggestion": null,
      "how_to_modify": null,
      "example_direction": null,
      "expected_impact": null,
      "risk_note": null
    }
  ],
  "module_suggestions": {
    "basic_info": [],
    "summary_or_self_evaluation": [],
    "skills": [],
    "work_experience": [],
    "project_experience": [],
    "education": [],
    "certificates_awards": [],
    "format_and_structure": []
  },
  "high_priority_actions": [
    {
      "action": null,
      "reason": null,
      "estimated_effort": "medium",
      "expected_benefit": "medium"
    }
  ],
  "keyword_optimization_advice": [
    {
      "keyword": null,
      "current_status": null,
      "safe_addition_method": null,
      "note": null
    }
  ],
  "content_to_reduce_or_remove": [
    {
      "content_type": null,
      "reason": null,
      "suggestion": null
    }
  ],
  "risk_notes": []
}

estimated_effort 取值：low、medium、high
expected_benefit 取值：low、medium、high

简历结构化数据：
{{resume_structured_data}}

简历原文：
{{resume_text}}

岗位结构化数据：
{{job_structured_data}}

岗位描述原文：
{{job_text}}

简历评分结果：
{{score_result}}

岗位匹配结果：
{{match_result}}

关键词分析结果：
{{keyword_result}}
```

## 9.4 建议生成原则

优化建议应遵循以下优先级：

1. 先解决与目标岗位强相关的硬技能缺口。
2. 再优化项目和工作经历中的职责、方法、结果表达。
3. 再补充量化成果、项目规模、业务影响。
4. 最后调整格式、结构、措辞和冗余内容。

## 9.5 后端校验规则

1. `suggestions` 必须是数组。
2. `priority` 必须为 `high`、`medium`、`low`。
3. `risk_note` 中应包含不虚构经历的提示，尤其是涉及技能补充时。
4. 如果建议数量过多，前端可优先展示 `high_priority_actions`。

------

# 10. 简历改写示例 Prompt

## 10.1 使用场景

用于对简历中的问题句子、工作经历或项目经历提供改写示例。

适用模板场景：

```text
rewrite_example
```

## 10.2 输入变量

```json
{
  "resume_text": "{{resume_text}}",
  "selected_sentences": {{selected_sentences}},
  "target_position": "{{target_position}}",
  "job_text": "{{job_text}}",
  "rewrite_style": "professional_result_oriented",
  "language": "zh-CN",
  "schema_version": "1.0"
}
```

## 10.3 改写风格枚举

| rewrite_style                  | 说明           |
| ------------------------------ | -------------- |
| `professional_result_oriented` | 专业、结果导向 |
| `concise`                      | 简洁精炼       |
| `ats_friendly`                 | 关键词友好     |
| `junior_candidate`             | 适合初级求职者 |
| `senior_candidate`             | 适合高级候选人 |

## 10.4 Prompt 模板

```text
你是一名专业的中文简历改写顾问。请对用户提供的简历句子或经历描述生成改写示例。

你必须遵守以下规则：
1. 不得编造用户未提供的工具、数据、成果、公司、岗位、证书或项目背景。
2. 如果原句缺少数据或结果，只能用“可补充方向”提示，不要直接生成虚假数字。
3. 改写应更专业、具体、结果导向，并尽量贴合目标岗位。
4. 每条改写都必须说明原句问题和改写理由。
5. 输出必须是合法 JSON，不要输出 Markdown 或解释文字。

请按照以下 JSON 结构返回：

{
  "schema_version": "1.0",
  "rewrite_style": "professional_result_oriented",
  "examples": [
    {
      "original": null,
      "issue": null,
      "rewritten": null,
      "rewrite_reason": null,
      "missing_information": [],
      "optional_enhancement": null,
      "risk_note": null
    }
  ],
  "general_rewrite_tips": []
}

改写要求：
- 尽量使用“动作 + 方法/工具 + 对象 + 结果/影响”的结构。
- 对技术类岗位，优先体现技术栈、职责边界、性能、效率、稳定性、业务价值等信息。
- 对缺少量化结果的句子，不要虚构数字，而是提示用户可以补充哪些指标。

待改写句子或段落：
{{selected_sentences}}

完整简历上下文：
{{resume_text}}

目标岗位：
{{target_position}}

岗位描述：
{{job_text}}

改写风格：
{{rewrite_style}}
```

## 10.5 输出示例

```json
{
  "schema_version": "1.0",
  "rewrite_style": "professional_result_oriented",
  "examples": [
    {
      "original": "负责后台接口开发",
      "issue": "表达过于笼统，缺少技术栈、接口范围和结果说明。",
      "rewritten": "参与后台 API 接口开发，负责用户认证、简历上传和分析任务等模块的接口设计与实现，并配合前端完成联调。",
      "rewrite_reason": "补充了职责范围、业务模块和协作场景，使表达更具体。",
      "missing_information": ["接口数量", "性能指标", "上线结果"],
      "optional_enhancement": "如果属实，可补充接口数量、响应时间优化效果或上线后的使用情况。",
      "risk_note": "不要添加未真实参与的模块或不存在的数据指标。"
    }
  ],
  "general_rewrite_tips": [
    "优先使用具体动词，例如设计、实现、优化、排查、沉淀。",
    "每段经历尽量体现技术方法和最终结果。"
  ]
}
```

## 10.6 后端校验规则

1. `examples` 必须是数组。
2. `original` 必须来自用户输入的句子或段落。
3. `rewritten` 不应包含明显虚构的数字或工具。
4. 如果模型生成了不可靠数字，后端可追加风险提示或要求重新生成。

------

# 11. 完整分析报告 Prompt

## 11.1 使用场景

用于一次性生成完整分析报告，适合 `full_analysis` 任务。该模板会综合输出简历评分、岗位匹配、关键词覆盖、优势、问题、优化建议和改写示例。

适用任务类型：

```text
full_analysis
```

适用模板场景：

```text
full_analysis
```

## 11.2 输入变量

```json
{
  "resume_text": "{{resume_text}}",
  "resume_structured_data": {{resume_structured_data}},
  "job_text": "{{job_text}}",
  "job_structured_data": {{job_structured_data}},
  "language": "zh-CN",
  "schema_version": "1.0"
}
```

## 11.3 Prompt 模板

```text
你是一名专业的中文简历分析顾问、招聘 JD 分析专家和职业发展顾问。请基于用户简历和目标岗位描述，生成完整简历分析报告。

你必须遵守以下规则：
1. 所有判断必须基于简历和岗位描述，不得编造。
2. 分数必须可解释，建议必须可执行。
3. 不得建议用户虚构经历、技能、项目、证书或数据。
4. 如果某项能力未在简历体现，应表述为“简历未体现”或“建议确认后补充”。
5. 输出必须是合法 JSON，不要输出 Markdown 或解释文字。

请按照以下 JSON 结构返回：

{
  "schema_version": "1.0",
  "total_score": 0,
  "match_score": 0,
  "summary": null,
  "score_breakdown": {
    "completeness": 0,
    "structure": 0,
    "professional_expression": 0,
    "experience_quality": 0,
    "skill_match": 0,
    "quantified_results": 0
  },
  "match_breakdown": {
    "skill_match": 0,
    "work_experience_match": 0,
    "project_experience_match": 0,
    "industry_background_match": 0,
    "keyword_coverage_match": 0,
    "soft_skill_education_match": 0
  },
  "strengths": [
    {
      "strength": null,
      "evidence": null,
      "related_job_requirement": null
    }
  ],
  "weaknesses": [
    {
      "weakness": null,
      "evidence": null,
      "impact": null
    }
  ],
  "keyword_analysis": {
    "coverage_rate": 0,
    "matched_keywords": [],
    "missing_keywords": [],
    "partially_covered_keywords": [],
    "keyword_suggestions": []
  },
  "matched_requirements": [],
  "missing_requirements": [],
  "risk_items": [
    {
      "risk": null,
      "severity": "medium",
      "reason": null,
      "suggestion": null
    }
  ],
  "suggestions": [
    {
      "priority": "high",
      "module": null,
      "problem": null,
      "suggestion": null,
      "expected_impact": null,
      "risk_note": null
    }
  ],
  "rewrite_examples": [
    {
      "original": null,
      "issue": null,
      "rewritten": null,
      "rewrite_reason": null,
      "missing_information": [],
      "risk_note": null
    }
  ],
  "next_actions": [
    {
      "priority": "high",
      "action": null,
      "reason": null
    }
  ],
  "risk_notes": [
    "建议仅补充真实具备的技能、经历和数据，不要为匹配岗位而虚构内容。"
  ]
}

评分要求：
1. total_score 为简历基础质量分，范围 0-100。
2. match_score 为岗位匹配度，范围 0-100。
3. score_breakdown 中各项按以下满分评分：
   - completeness：20
   - structure：15
   - professional_expression：20
   - experience_quality：20
   - skill_match：15
   - quantified_results：10
4. match_breakdown 中各项为 0-100 的维度匹配分。

简历结构化数据：
{{resume_structured_data}}

简历原文：
{{resume_text}}

岗位结构化数据：
{{job_structured_data}}

岗位描述原文：
{{job_text}}
```

## 11.4 后端校验规则

1. `total_score` 和 `match_score` 必须为 0 到 100。
2. `score_breakdown` 中各维度不得超过对应满分。
3. `suggestions`、`rewrite_examples`、`risk_notes` 必须是数组。
4. 如果 `rewrite_examples.original` 不是来自简历原文，应丢弃该条或重新请求。
5. `summary` 建议限制在 200 字以内，便于报告列表展示。

------

# 12. Prompt 模板数据库初始化建议

## 12.1 prompt_templates 初始化数据

系统初始化时，可向 `prompt_templates` 表写入以下默认模板：

```json
[
  {
    "name": "简历结构化解析模板",
    "scene": "resume_parse",
    "version": 1,
    "status": "active",
    "description": "将简历原文解析为结构化 JSON"
  },
  {
    "name": "岗位描述结构化解析模板",
    "scene": "job_parse",
    "version": 1,
    "status": "active",
    "description": "将岗位描述解析为职责、技能、关键词等结构化信息"
  },
  {
    "name": "简历评分模板",
    "scene": "resume_score",
    "version": 1,
    "status": "active",
    "description": "对简历基础质量进行 100 分制评分"
  },
  {
    "name": "岗位匹配分析模板",
    "scene": "job_match",
    "version": 1,
    "status": "active",
    "description": "分析简历与岗位之间的匹配度和差距"
  },
  {
    "name": "关键词分析模板",
    "scene": "keyword_analysis",
    "version": 1,
    "status": "active",
    "description": "分析 JD 关键词在简历中的覆盖情况"
  },
  {
    "name": "简历优化建议模板",
    "scene": "resume_suggestion",
    "version": 1,
    "status": "active",
    "description": "生成具体可执行的简历修改建议"
  },
  {
    "name": "简历改写示例模板",
    "scene": "rewrite_example",
    "version": 1,
    "status": "active",
    "description": "对简历句子或段落生成改写示例"
  },
  {
    "name": "完整分析报告模板",
    "scene": "full_analysis",
    "version": 1,
    "status": "active",
    "description": "一次性生成完整简历分析报告"
  }
]
```

## 12.2 模板选择逻辑

后端构建 Prompt 时建议按以下规则选择模板：

```text
1. 根据 scene 查询 status = active 的模板。
2. 如果存在多个 active 模板，选择 version 最大的模板。
3. 如果没有 active 模板，使用代码内置 fallback 模板。
4. 每次调用时记录 prompt_template_id 到 api_call_logs。
```

------

# 13. AI 响应校验与修复策略

## 13.1 JSON 解析失败

处理流程：

```text
1. 尝试去除 Markdown 代码块。
2. 尝试截取第一个 { 到最后一个 } 之间的内容。
3. 再次 JSON parse。
4. 如果仍失败，记录 ai_response_invalid。
5. 可选：发起一次“修复 JSON 格式”的模型请求。
```

## 13.2 分数异常

校验规则：

1. 分数小于 0 时修正为 0。
2. 分数大于满分时修正为满分。
3. 总分与维度分不一致时，优先使用维度分重新计算。
4. 匹配度必须在 0 到 100 之间。

## 13.3 字段缺失

处理规则：

1. 必填字段缺失时填充默认值。
2. 数组字段缺失时填充空数组。
3. 对象字段缺失时填充默认结构。
4. 关键字段大量缺失时判定为 AI 返回格式错误。

## 13.4 内容安全校验

后端应检查以下风险：

1. 是否出现明显编造的具体数据。
2. 是否建议用户虚构经历。
3. 是否输出与简历或岗位无关的内容。
4. 是否重复输出过多个人敏感信息。
5. 是否包含 Markdown、HTML 或脚本注入风险内容。

------

# 14. 推荐后端代码结构

AI Prompt 相关代码建议放在：

```text
backend/app/services/ai/
├── deepseek_client.py
├── prompt_builder.py
├── response_parser.py
├── response_validator.py
└── prompts/
    ├── resume_parse.py
    ├── job_parse.py
    ├── resume_score.py
    ├── job_match.py
    ├── keyword_analysis.py
    ├── resume_suggestion.py
    ├── rewrite_example.py
    └── full_analysis.py
```

Prompt 构建流程建议：

```text
业务服务
  ↓
读取 Prompt 模板
  ↓
填充输入变量
  ↓
调用 DeepSeek Client
  ↓
解析 JSON
  ↓
校验 Schema
  ↓
保存结构化结果
```

------

# 15. 测试用例建议

## 15.1 简历解析测试

测试场景：

1. 完整中文简历。
2. 缺少联系方式的简历。
3. 缺少项目经历的简历。
4. PDF 解析后段落混乱的简历。
5. 中英文混合技术简历。

重点校验：

- JSON 是否合法。
- 核心字段是否正确提取。
- 未出现的字段是否返回 null 或空数组。

## 15.2 岗位解析测试

测试场景：

1. 标准招聘 JD。
2. 只有岗位职责，没有任职要求。
3. 技术栈复杂的后端岗位。
4. 非技术岗位。
5. 复制自招聘网站、格式杂乱的 JD。

重点校验：

- 必备技能和加分技能是否区分合理。
- 关键词是否来自 JD。
- 经验年限和学历要求是否提取准确。

## 15.3 评分测试

测试场景：

1. 内容完整、表达优秀的简历。
2. 内容很短的简历。
3. 技能堆砌但缺少项目的简历。
4. 有项目但无量化结果的简历。

重点校验：

- 总分是否在合理范围。
- 维度分是否不超过满分。
- 扣分理由是否与简历内容一致。

## 15.4 匹配分析测试

测试场景：

1. 高度匹配的简历与 JD。
2. 技能匹配但经验年限不足。
3. 项目相关但技术栈不完全一致。
4. 简历未体现 JD 核心关键词。

重点校验：

- 是否区分“缺失”和“未体现”。
- 是否给出合理风险项。
- 是否避免过度否定候选人。

## 15.5 改写示例测试

测试场景：

1. 原句非常笼统。
2. 原句缺少技术栈。
3. 原句缺少结果。
4. 原句只有职责没有成果。

重点校验：

- 改写是否更具体。
- 是否虚构数字或经历。
- 是否给出缺失信息提示。

------

# 16. 一期实施建议

一期 MVP 建议优先实现以下模板：

1. `resume_parse`
2. `job_parse`
3. `full_analysis`

原因：

- `resume_parse` 和 `job_parse` 是后续分析的数据基础。
- `full_analysis` 能快速覆盖报告详情页所需的大部分内容。

当系统稳定后，再拆分为更细粒度的独立调用：

1. `resume_score`
2. `job_match`
3. `keyword_analysis`
4. `resume_suggestion`
5. `rewrite_example`

拆分后的优点：

1. 单次 Prompt 更短，输出更稳定。
2. 便于失败重试。
3. 便于单独缓存和复用结果。
4. 便于前端分模块展示加载状态。

------

# 17. 后续扩展方向

后续可以扩展以下 Prompt 能力：

1. 多语言简历分析 Prompt。
2. 英文简历改写 Prompt。
3. 不同行业岗位专用评分 Prompt。
4. 初级、中级、高级候选人差异化评分规则。
5. 面试问题生成 Prompt。
6. 简历版本对比 Prompt。
7. 求职信生成 Prompt。
8. LinkedIn 个人简介优化 Prompt。
9. ATS 友好度检测 Prompt。
10. 管理员 Prompt A/B 测试机制。