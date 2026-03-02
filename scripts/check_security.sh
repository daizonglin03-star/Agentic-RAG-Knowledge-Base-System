#!/bin/bash

# 安全检查脚本 - 检查是否有硬编码的敏感信息

echo "🔍 开始安全检查..."
echo ""

# 检查是否存在 .env 文件
if [ -f ".env" ]; then
    echo "✅ 发现 .env 文件"
    if grep -q "your-.*-here" .env; then
        echo "⚠️  警告: .env 文件包含占位符，请填入真实配置"
    else
        echo "✅ .env 文件已配置"
    fi
else
    echo "❌ 未找到 .env 文件"
    echo "   请运行: cp .env.example .env"
fi

echo ""

# 检查 .gitignore 是否包含 .env
if grep -q "^\.env$" .gitignore; then
    echo "✅ .gitignore 已排除 .env 文件"
else
    echo "❌ .gitignore 未排除 .env 文件"
fi

echo ""

# 检查代码中是否有硬编码的密钥（排除文档和虚拟环境）
echo "🔍 检查硬编码密钥..."
FOUND_KEYS=$(grep -r --exclude-dir={venv,node_modules,.git,__pycache__} \
    --exclude={"*.md","*.sh","*.example"} \
    -E "(LTAI[A-Za-z0-9]{20,}|tvly-[A-Za-z0-9]{20,}|eyJ0eXAi[A-Za-z0-9_-]{100,})" \
    . 2>/dev/null || true)

if [ -z "$FOUND_KEYS" ]; then
    echo "✅ 未发现硬编码密钥"
else
    echo "❌ 发现可能的硬编码密钥:"
    echo "$FOUND_KEYS"
fi

echo ""

# 检查 python-dotenv 是否安装
if pip show python-dotenv > /dev/null 2>&1; then
    echo "✅ python-dotenv 已安装"
else
    echo "❌ python-dotenv 未安装"
    echo "   请运行: pip install python-dotenv"
fi

echo ""
echo "🔍 安全检查完成"
echo ""
echo "📚 下一步:"
echo "   1. 如果没有 .env 文件: cp .env.example .env"
echo "   2. 编辑 .env 文件，填入真实的 API Keys"
echo "   3. 运行验证: python project/validate_config.py"
