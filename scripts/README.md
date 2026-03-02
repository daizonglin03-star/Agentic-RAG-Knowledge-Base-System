# 🛠️ 脚本工具目录

本目录包含项目的实用脚本和工具。

## 🔒 安全检查工具

### check_security.sh
安全检查脚本，用于验证项目是否包含敏感信息。

**使用方法:**
```bash
./scripts/check_security.sh
```

**检查内容:**
- .env 文件是否存在
- .gitignore 是否正确配置
- 代码中是否有硬编码密钥
- python-dotenv 是否安装

---

### cleanup_project.sh
项目清理脚本，删除临时文件和敏感信息。

**使用方法:**
```bash
./scripts/cleanup_project.sh
```

**清理内容:**
- 敏感文件（.env, *_secret.py）
- macOS 系统文件（.DS_Store, ._*）
- Python 缓存（__pycache__, *.pyc）
- 临时文件（*.tmp, *.bak, *.log）
- Jupyter 检查点

---

## ⚙️ 配置工具

### validate_config.py
配置验证脚本，检查环境变量配置是否正确。

**使用方法:**
```bash
python scripts/validate_config.py
```

**验证内容:**
- .env 文件是否存在
- OSS 配置是否完整
- MineRU 配置是否完整
- Tavily API 配置（可选）

---

## 🚀 启动工具

### start_offline.py
离线模式启动脚本。

**使用方法:**
```bash
python scripts/start_offline.py
```

**功能:**
- 在离线环境下启动应用
- 使用本地模型
- 禁用网络功能

---

## 📥 下载工具

### download_models.py
模型下载脚本，用于预下载所需的模型。

**使用方法:**
```bash
python scripts/download_models.py
```

**下载内容:**
- Sentence Transformers 模型
- BM25 稀疏向量模型

---

## 🔧 使用建议

### 开发流程

1. **首次设置**
   ```bash
   # 1. 配置环境变量
   cp .env.example .env
   # 编辑 .env 文件
   
   # 2. 验证配置
   python scripts/validate_config.py
   
   # 3. 下载模型（可选）
   python scripts/download_models.py
   ```

2. **日常开发**
   ```bash
   # 提交前检查
   ./scripts/check_security.sh
   ./scripts/cleanup_project.sh
   ```

3. **离线使用**
   ```bash
   # 启动离线模式
   python scripts/start_offline.py
   ```

### 提交前检查

```bash
# 运行所有检查
./scripts/check_security.sh && \
./scripts/cleanup_project.sh && \
python scripts/validate_config.py && \
echo "✅ 准备就绪，可以提交！"
```

---

## 📝 脚本说明

| 脚本 | 类型 | 用途 | 频率 |
|------|------|------|------|
| `check_security.sh` | Shell | 安全检查 | 提交前 |
| `cleanup_project.sh` | Shell | 清理项目 | 提交前 |
| `validate_config.py` | Python | 验证配置 | 首次设置/配置更改后 |
| `start_offline.py` | Python | 离线启动 | 离线环境 |
| `download_models.py` | Python | 下载模型 | 首次设置 |

---

## ⚠️ 注意事项

1. **权限问题**: 如果脚本无法执行，运行 `chmod +x scripts/*.sh`
2. **路径问题**: 所有脚本都应该从项目根目录运行
3. **Python 路径**: Python 脚本会自动添加 project 目录到路径

---

**提示**: 如果遇到问题，请查看 [../docs/](../docs/) 目录中的相关文档。
