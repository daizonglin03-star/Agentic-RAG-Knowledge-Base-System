# 📓 示例 Notebook 目录

本目录包含项目的 Jupyter Notebook 示例。

## 📚 可用的 Notebooks

### Agentic_Rag_For_Dummies.ipynb
**主要教程 Notebook**

这是项目的核心教程，展示了如何从零开始构建一个 Agentic RAG 系统。

**内容包括:**
- 📖 RAG 系统基础概念
- 🔧 环境配置和依赖安装
- 📄 文档处理和分块策略
- 🔍 向量数据库设置（Qdrant）
- 🤖 LangGraph Agent 构建
- 💬 对话记忆和查询改写
- 🎯 完整的端到端示例

**适合人群:**
- RAG 初学者
- 想要理解 Agentic RAG 工作原理的开发者
- 需要快速原型的研究人员

**运行方式:**
```bash
# 本地运行
jupyter notebook examples/Agentic_Rag_For_Dummies.ipynb

# 或在 Google Colab 中打开
# 点击 README 中的 "Open in Colab" 按钮
```

---

### pdf_to_md.ipynb
**PDF 转 Markdown 工具**

演示如何将 PDF 文档转换为 Markdown 格式。

**功能:**
- 📄 PDF 文件读取
- 🔄 转换为 Markdown
- 💾 保存转换结果
- 🧹 文本清理和格式化

**使用场景:**
- 批量处理 PDF 文档
- 准备文档用于 RAG 系统
- 文档格式转换

**运行方式:**
```bash
jupyter notebook examples/pdf_to_md.ipynb
```

---

## 🚀 快速开始

### 1. 安装 Jupyter
```bash
pip install jupyter notebook
```

### 2. 启动 Jupyter
```bash
# 从项目根目录启动
jupyter notebook

# 或直接打开特定 notebook
jupyter notebook examples/Agentic_Rag_For_Dummies.ipynb
```

### 3. 在 Google Colab 中运行

点击主 README 中的 "Open in Colab" 按钮，或访问:
```
https://colab.research.google.com/
```
然后上传 notebook 文件。

---

## 📋 使用建议

### 学习路径

1. **初学者**
   - 从 `Agentic_Rag_For_Dummies.ipynb` 开始
   - 按顺序运行所有单元格
   - 理解每个步骤的作用

2. **进阶用户**
   - 修改参数和配置
   - 尝试不同的模型
   - 添加自定义功能

3. **文档处理**
   - 使用 `pdf_to_md.ipynb` 处理文档
   - 准备自己的数据集

### 最佳实践

1. **环境准备**
   ```bash
   # 确保依赖已安装
   pip install -r requirements_clean.txt
   
   # 配置环境变量
   cp .env.example .env
   # 编辑 .env 文件
   ```

2. **数据准备**
   - 将 PDF 文件放在 `docs/` 目录
   - 运行转换 notebook
   - 检查转换结果

3. **运行主 Notebook**
   - 按顺序执行单元格
   - 注意观察输出
   - 根据需要调整参数

---

## 🔧 故障排查

### 常见问题

**1. 模块导入错误**
```bash
# 确保在正确的环境中
pip install -r requirements_clean.txt
```

**2. 路径问题**
```python
# 在 notebook 中添加
import sys
sys.path.append('../project')
```

**3. 内存不足**
- 减少批处理大小
- 使用更小的模型
- 在 Colab 中使用 GPU

**4. API 配置问题**
```bash
# 验证配置
python scripts/validate_config.py
```

---

## 📊 Notebook 对比

| Notebook | 难度 | 时长 | 用途 |
|----------|------|------|------|
| `Agentic_Rag_For_Dummies.ipynb` | 初级-中级 | 30-60分钟 | 学习 RAG 系统 |
| `pdf_to_md.ipynb` | 初级 | 10-20分钟 | 文档转换 |

---

## 🎯 下一步

完成 Notebook 学习后:

1. **部署应用**
   ```bash
   python project/app.py
   ```

2. **自定义开发**
   - 修改 `project/` 目录中的代码
   - 添加新功能
   - 优化性能

3. **生产部署**
   - 参考 `project/Dockerfile`
   - 配置生产环境
   - 设置监控和日志

---

## 📚 相关资源

- **主文档**: [../README.md](../README.md)
- **配置指南**: [../docs/SECURITY_SETUP.md](../docs/SECURITY_SETUP.md)
- **快速开始**: [../QUICK_START.md](../QUICK_START.md)

---

**提示**: 建议在学习 Notebook 的同时阅读相关文档，以获得更全面的理解。
