#!/bin/bash

# 项目清理脚本 - 删除敏感信息和临时文件

echo "🧹 开始清理项目..."
echo ""

# 1. 删除敏感文件
echo "🔒 删除敏感文件..."
find . -name ".env" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 .env 文件" || echo "  ℹ️  未找到 .env 文件"
find . -name "*.env" ! -name ".env.example" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *.env 文件"
find . -name "*_secret.py" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *_secret.py 文件"
find . -name "*_secrets.py" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *_secrets.py 文件"
find . -name "config_local.py" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 config_local.py 文件"
find . -name "credentials.json" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 credentials.json 文件"

echo ""

# 2. 删除 macOS 系统文件
echo "🍎 删除 macOS 系统文件..."
find . -name ".DS_Store" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 .DS_Store 文件"
find . -name "._*" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 ._* 元数据文件"
find . -name ".AppleDouble" ! -path "./venv/*" -type d -exec rm -rf {} + 2>/dev/null && echo "  ✅ 已删除 .AppleDouble 目录"
find . -name ".LSOverride" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 .LSOverride 文件"

echo ""

# 3. 删除 Python 缓存
echo "🐍 删除 Python 缓存..."
find . -type d -name "__pycache__" ! -path "./venv/*" -exec rm -rf {} + 2>/dev/null && echo "  ✅ 已删除 __pycache__ 目录"
find . -name "*.pyc" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *.pyc 文件"
find . -name "*.pyo" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *.pyo 文件"
find . -name "*.pyd" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *.pyd 文件"

echo ""

# 4. 删除临时文件
echo "🗑️  删除临时文件..."
find . -name "*.tmp" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *.tmp 文件"
find . -name "*.bak" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *.bak 文件"
find . -name "*.swp" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *.swp 文件"
find . -name "*.swo" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *.swo 文件"
find . -name "*~" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *~ 文件"

echo ""

# 5. 删除日志文件
echo "📝 删除日志文件..."
find . -name "*.log" ! -path "./venv/*" -type f -delete 2>/dev/null && echo "  ✅ 已删除 *.log 文件"
find . -type d -name "logs" ! -path "./venv/*" -exec rm -rf {} + 2>/dev/null && echo "  ✅ 已删除 logs 目录"

echo ""

# 6. 删除 Jupyter 检查点
echo "📓 删除 Jupyter 检查点..."
find . -type d -name ".ipynb_checkpoints" ! -path "./venv/*" -exec rm -rf {} + 2>/dev/null && echo "  ✅ 已删除 .ipynb_checkpoints 目录"

echo ""

# 7. 删除 IDE 配置（可选）
read -p "是否删除 IDE 配置文件 (.vscode, .idea)? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    find . -type d -name ".vscode" ! -path "./venv/*" -exec rm -rf {} + 2>/dev/null && echo "  ✅ 已删除 .vscode 目录"
    find . -type d -name ".idea" ! -path "./venv/*" -exec rm -rf {} + 2>/dev/null && echo "  ✅ 已删除 .idea 目录"
else
    echo "  ℹ️  保留 IDE 配置文件"
fi

echo ""

# 8. 统计清理结果
echo "📊 清理统计..."
echo "  项目大小（不含 venv）:"
du -sh . 2>/dev/null | awk '{print "    " $1}'

echo ""
echo "✅ 清理完成！"
echo ""
echo "📋 下一步:"
echo "  1. 检查 .gitignore 是否完整"
echo "  2. 确保 .env.example 存在"
echo "  3. 运行安全检查: ./check_security.sh"
echo "  4. 提交前再次确认没有敏感信息"
