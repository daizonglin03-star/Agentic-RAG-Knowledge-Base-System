# 📁 项目结构说明

本文档描述了项目的目录结构和文件组织方式。

## 🌳 目录树

```
agentic-rag-for-dummies/
├── 📄 README.md                    # 项目主文档
├── 📄 QUICK_START.md               # 5分钟快速开始指南
├── 📄 LICENSE                      # 开源许可证
├── 📄 .env.example                 # 环境变量模板
├── 📄 .gitignore                   # Git 忽略规则
├── 📄 requirements.txt             # Python 依赖（Anaconda 格式）
├── 📄 requirements_clean.txt       # Python 依赖（清理版，推荐）
│
├── 📂 project/                     # 核心应用代码
│   ├── 📄 app.py                   # 主应用入口（Gradio UI）
│   ├── 📄 config.py                # 配置文件（使用环境变量）
│   ├── 📄 Dockerfile               # Docker 部署配置
│   │
│   ├── 📄 document_chunker.py      # 文档分块处理
│   ├── 📄 util.py                  # PDF 转 Markdown 工具
│   ├── 📄 word_utils.py            # Word 文档处理
│   ├── 📄 mineru_utils.py          # MineRU API 集成
│   ├── 📄 oss_utils.py             # 阿里云 OSS 工具
│   ├── 📄 mcp_search.py            # 网络搜索工具（Tavily）
│   │
│   ├── 📂 core/                    # 核心功能模块
│   │   ├── chat_interface.py       # 聊天接口
│   │   ├── document_manager.py     # 文档管理
│   │   └── rag_system.py           # RAG 系统核心
│   │
│   ├── 📂 db/                      # 数据库管理
│   │   ├── vector_db_manager.py    # Qdrant 向量数据库
│   │   └── parent_store_manager.py # 父块存储管理
│   │
│   ├── 📂 rag_agent/               # LangGraph Agent
│   │   ├── graph.py                # Agent 图定义
│   │   ├── nodes.py                # Agent 节点
│   │   ├── edges.py                # Agent 边（路由）
│   │   ├── graph_state.py          # 状态管理
│   │   ├── prompts.py              # 提示词模板
│   │   ├── schemas.py              # 数据模式
│   │   └── tools.py                # Agent 工具
│   │
│   └── 📂 ui/                      # 用户界面
│       ├── gradio_app.py           # Gradio 应用
│       └── css.py                  # 样式定义
│
├── 📂 scripts/                     # 实用脚本工具
│   ├── 📄 README.md                # 脚本说明文档
│   ├── 🔧 check_security.sh        # 安全检查脚本
│   ├── 🔧 cleanup_project.sh       # 项目清理脚本
│   ├── 🐍 validate_config.py       # 配置验证脚本
│   ├── 🐍 download_models.py       # 模型下载脚本
│   └── 🐍 start_offline.py         # 离线模式启动
│
├── 📂 docs/                        # 文档目录
│   ├── 📄 README.md                # 文档索引
│   │
│   ├── 📖 用户文档
│   │   ├── SECURITY_SETUP.md       # 安全配置指南
│   │   ├── OFFLINE_SETUP.md        # 离线模式配置
│   │   ├── TAVILY_SETUP.md         # Tavily API 配置
│   │   ├── SEARCH_README.md        # 搜索功能说明
│   │   ├── QUICK_START_SEARCH.md   # 搜索快速开始
│   │   └── WORD_SUPPORT.md         # Word 文档支持
│   │
│   ├── 📖 开发文档
│   │   ├── PROJECT_README.md       # 项目详细说明
│   │   ├── MINERU_UPGRADE.md       # MineRU 升级指南
│   │   └── FINAL_SUMMARY.md        # 项目总结
│   │
│   └── 📖 开源准备
│       ├── PRE_COMMIT_CHECKLIST.md         # 提交前检查
│       ├── GITHUB_RELEASE_CHECKLIST.md     # GitHub 发布清单
│       ├── SECURITY_MIGRATION.md           # 安全迁移说明
│       ├── SECURITY_CLEANUP_SUMMARY.md     # 安全清理总结
│       └── PROJECT_CLEANUP_COMPLETE.md     # 清理完成报告
│
├── 📂 examples/                    # 示例 Notebooks
│   ├── 📄 README.md                # 示例说明文档
│   ├── 📓 Agentic_Rag_For_Dummies.ipynb  # 主教程 Notebook
│   └── 📓 pdf_to_md.ipynb          # PDF 转换示例
│
└── 📂 assets/                      # 静态资源
    ├── 🖼️ logo.png                 # 项目 Logo
    ├── 🖼️ demo.gif                 # 演示动图
    └── 🖼️ agentic_rag_workflow.png # 工作流程图
```

## 📋 目录说明

### 根目录文件

| 文件 | 说明 |
|------|------|
| `README.md` | 项目主文档，包含项目介绍、功能特性、安装使用等 |
| `QUICK_START.md` | 5分钟快速开始指南 |
| `LICENSE` | 开源许可证 |
| `.env.example` | 环境变量配置模板 |
| `.gitignore` | Git 忽略规则 |
| `requirements_clean.txt` | Python 依赖清单（推荐使用） |
| `requirements.txt` | Python 依赖清单（Anaconda 格式） |

### 📂 project/ - 核心应用

包含所有应用代码，按功能模块组织：

- **主文件**: `app.py`（应用入口）、`config.py`（配置管理）
- **工具模块**: 文档处理、OSS 存储、网络搜索等
- **core/**: 核心功能（聊天、文档管理、RAG 系统）
- **db/**: 数据库管理（向量数据库、父块存储）
- **rag_agent/**: LangGraph Agent 实现
- **ui/**: Gradio 用户界面

### 📂 scripts/ - 实用工具

包含开发和维护所需的脚本：

- **安全工具**: 安全检查、项目清理
- **配置工具**: 配置验证
- **启动工具**: 离线模式启动
- **下载工具**: 模型下载

### 📂 docs/ - 文档

所有项目文档的集中存放位置：

- **用户文档**: 配置指南、功能说明
- **开发文档**: 项目说明、升级指南
- **开源准备**: 发布清单、安全文档

### 📂 examples/ - 示例

Jupyter Notebook 示例和教程：

- **主教程**: 完整的 RAG 系统构建教程
- **工具示例**: PDF 转换等实用工具

### 📂 assets/ - 静态资源

项目使用的图片和媒体文件。

## 🎯 文件查找指南

### 我想...

| 需求 | 文件位置 |
|------|----------|
| 快速开始使用 | `QUICK_START.md` |
| 了解项目详情 | `README.md` |
| 配置 API Keys | `docs/SECURITY_SETUP.md` |
| 运行应用 | `project/app.py` |
| 修改配置 | `project/config.py` |
| 验证配置 | `scripts/validate_config.py` |
| 学习 RAG 系统 | `examples/Agentic_Rag_For_Dummies.ipynb` |
| 启用网络搜索 | `docs/TAVILY_SETUP.md` |
| 离线使用 | `docs/OFFLINE_SETUP.md` |
| 准备开源发布 | `docs/GITHUB_RELEASE_CHECKLIST.md` |

## 🔧 开发工作流

### 1. 首次设置
```bash
# 1. 配置环境
cp .env.example .env
# 编辑 .env 文件

# 2. 验证配置
python scripts/validate_config.py

# 3. 安装依赖
pip install -r requirements_clean.txt
```

### 2. 日常开发
```bash
# 运行应用
python project/app.py

# 修改代码
# 编辑 project/ 目录下的文件
```

### 3. 提交前
```bash
# 安全检查
./scripts/check_security.sh

# 清理项目
./scripts/cleanup_project.sh

# 验证配置
python scripts/validate_config.py
```

## 📊 代码统计

| 目录 | 用途 | 文件数 |
|------|------|--------|
| `project/` | 核心代码 | ~20 个 Python 文件 |
| `scripts/` | 工具脚本 | 5 个脚本 |
| `docs/` | 文档 | ~15 个文档 |
| `examples/` | 示例 | 2 个 Notebook |
| `assets/` | 资源 | 3 个图片 |

## 🚀 部署结构

### 开发环境
```
本地开发 → project/app.py → Gradio UI (http://localhost:7860)
```

### 生产环境
```
Docker → project/Dockerfile → 容器化部署
```

## 📝 命名规范

- **Python 文件**: `snake_case.py`
- **文档文件**: `UPPER_SNAKE_CASE.md`
- **脚本文件**: `snake_case.sh` 或 `snake_case.py`
- **目录**: `lowercase/`

## ⚠️ 注意事项

### 不应提交到 Git 的内容

- `.env` - 环境变量配置（包含敏感信息）
- `venv/` - 虚拟环境
- `__pycache__/` - Python 缓存
- `qdrant_db/` - 向量数据库数据
- `markdown_docs/` - 临时文档
- `parent_store/` - 临时存储

这些已在 `.gitignore` 中配置。

### 应该提交的内容

- 所有源代码（`project/`）
- 所有文档（`docs/`、`README.md` 等）
- 所有脚本（`scripts/`）
- 所有示例（`examples/`）
- 配置模板（`.env.example`）
- 依赖清单（`requirements*.txt`）

---

**最后更新**: 2026-03-02  
**项目大小**: ~3MB（不含 venv 和数据）
