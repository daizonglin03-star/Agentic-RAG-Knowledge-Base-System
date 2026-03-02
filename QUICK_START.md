# 🚀 快速开始指南

## 5 分钟快速设置

### 1️⃣ 克隆项目
```bash
git clone <your-repo-url>
cd agentic-rag-for-dummies
```

### 2️⃣ 配置环境变量
```bash
# 复制模板
cp .env.example .env

# 编辑配置文件
nano .env  # 或使用你喜欢的编辑器
```

在 `.env` 中填入你的真实配置：
```bash
# 必填项
OSS_ACCESS_KEY=your-access-key-here
OSS_SECRET_KEY=your-secret-key-here
OSS_BUCKET=your-bucket-name
MINERU_API_KEY=your-mineru-api-key-here

# 可选项（联网搜索）
TAVILY_API_KEY=your-tavily-api-key-here
ENABLE_WEB_SEARCH=False
```

### 3️⃣ 安装依赖
```bash
# 推荐：使用清理后的依赖列表
pip install -r requirements_clean.txt

# 或者如果你使用 Anaconda
pip install -r requirements.txt
```

### 4️⃣ 验证配置
```bash
python project/validate_config.py
```

### 5️⃣ 运行应用
```bash
python project/app.py
```

打开浏览器访问: `http://127.0.0.1:7860`

---

## 📝 获取 API Keys

### 阿里云 OSS
1. 访问 [阿里云控制台](https://oss.console.aliyun.com/)
2. 创建 Bucket 或使用现有的
3. 在 AccessKey 管理中创建密钥对

### MineRU API
1. 访问 [MineRU 官网](https://mineru.net/)
2. 注册账号并获取 API Key

### Tavily Search API（可选）
1. 访问 [Tavily](https://tavily.com/)
2. 注册免费账号（每月 1000 次搜索）
3. 获取 API Key

---

## 🔧 故障排查

### 配置未生效
```bash
# 检查 .env 文件是否存在
ls -la .env

# 检查 python-dotenv 是否安装
pip show python-dotenv

# 运行安全检查
./check_security.sh
```

### 依赖安装失败
```bash
# 升级 pip
pip install --upgrade pip

# 使用清理后的依赖列表
pip install -r requirements_clean.txt
```

### API 调用失败
```bash
# 验证配置
python project/validate_config.py

# 检查网络连接
ping oss-cn-beijing.aliyuncs.com
```

---

## 📚 更多文档

- [完整文档](README.md)
- [安全配置指南](project/SECURITY_SETUP.md)
- [提交前检查清单](PRE_COMMIT_CHECKLIST.md)
- [项目清理报告](PROJECT_CLEANUP_COMPLETE.md)

---

## ⚡ 一键设置（高级）

```bash
# 自动化设置脚本
cp .env.example .env && \
echo "请编辑 .env 文件填入真实的 API Keys" && \
read -p "按 Enter 继续..." && \
pip install -r requirements_clean.txt && \
python project/validate_config.py && \
echo "✅ 设置完成！运行 'python project/app.py' 启动应用"
```

---

**需要帮助？** 查看 [SECURITY_SETUP.md](project/SECURITY_SETUP.md) 获取详细说明。
