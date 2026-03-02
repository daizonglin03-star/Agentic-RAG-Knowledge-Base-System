#!/usr/bin/env python3
"""
配置验证脚本：检查环境变量配置是否正确
"""
import sys
import os

# 添加 project 目录到路径
project_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'project')
sys.path.insert(0, project_dir)

try:
    import config
except ImportError as e:
    print(f"❌ 无法导入 config 模块: {e}")
    print("请确保在项目根目录运行此脚本")
    sys.exit(1)


def validate_oss_config():
    """验证OSS配置"""
    print("🔍 验证 OSS 配置...")
    print("-" * 60)
    
    required_keys = ["endpoint", "bucket", "access_key", "secret_key"]
    missing_keys = []
    empty_keys = []
    
    for key in required_keys:
        if key not in config.OSS_CONFIG:
            missing_keys.append(key)
        elif not config.OSS_CONFIG[key]:
            empty_keys.append(key)
    
    if missing_keys:
        print(f"❌ 缺少配置项: {', '.join(missing_keys)}")
        return False
    
    if empty_keys:
        print(f"⚠️  配置项为空: {', '.join(empty_keys)}")
        print("   请在 .env 文件中填入真实的配置")
        return False
    
    print(f"✅ OSS 配置完整")
    print(f"   Endpoint: {config.OSS_CONFIG['endpoint']}")
    print(f"   Bucket: {config.OSS_CONFIG['bucket']}")
    print(f"   Access Key: {config.OSS_CONFIG['access_key'][:10]}...")
    return True


def validate_mineru_config():
    """验证MineRU配置"""
    print("\n🔍 验证 MineRU 配置...")
    print("-" * 60)
    
    required_keys = ["api_url", "api_key"]
    missing_keys = []
    empty_keys = []
    
    for key in required_keys:
        if key not in config.MINERU_CONFIG:
            missing_keys.append(key)
        elif not config.MINERU_CONFIG[key]:
            empty_keys.append(key)
    
    if missing_keys:
        print(f"❌ 缺少配置项: {', '.join(missing_keys)}")
        return False
    
    if empty_keys:
        print(f"⚠️  配置项为空: {', '.join(empty_keys)}")
        print("   请在 .env 文件中填入真实的配置")
        return False
    
    print(f"✅ MineRU 配置完整")
    print(f"   API URL: {config.MINERU_CONFIG['api_url']}")
    print(f"   API Key: {config.MINERU_CONFIG['api_key'][:20]}...")
    return True


def validate_web_search_config():
    """验证网络搜索配置（可选）"""
    print("\n🔍 验证网络搜索配置（可选）...")
    print("-" * 60)
    
    if not config.ENABLE_WEB_SEARCH:
        print("ℹ️  网络搜索功能未启用")
        return True
    
    api_key = config.WEB_SEARCH_CONFIG.get("api_key", "")
    
    if not api_key:
        print("⚠️  网络搜索已启用但 API Key 为空")
        print("   请在 .env 文件中配置 TAVILY_API_KEY")
        return False
    
    print(f"✅ Tavily API Key 已配置")
    print(f"   API Key: {api_key[:20]}...")
    return True


def validate_env_file():
    """验证 .env 文件是否存在"""
    print("🔍 验证 .env 文件...")
    print("-" * 60)
    
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    
    if not os.path.exists(env_path):
        print("❌ .env 文件不存在")
        print("\n请执行以下步骤:")
        print("  1. cp .env.example .env")
        print("  2. 编辑 .env 文件，填入真实的 API Keys")
        return False
    
    print("✅ .env 文件存在")
    return True


def main():
    """主验证函数"""
    print("=" * 60)
    print("🚀 配置验证工具")
    print("=" * 60)
    print()
    
    all_valid = True
    
    # 验证 .env 文件
    if not validate_env_file():
        all_valid = False
        print("\n" + "=" * 60)
        print("⚠️  请先创建并配置 .env 文件")
        print("=" * 60)
        sys.exit(1)
    
    # 验证各项配置
    if not validate_oss_config():
        all_valid = False
    
    if not validate_mineru_config():
        all_valid = False
    
    if not validate_web_search_config():
        all_valid = False
    
    print("\n" + "=" * 60)
    
    if all_valid:
        print("✅ 所有配置验证通过！")
        print("=" * 60)
        print("\n下一步:")
        print("  python project/app.py  # 启动应用")
    else:
        print("❌ 配置验证失败")
        print("=" * 60)
        print("\n请修复上述问题:")
        print("  1. 确保 .env 文件存在")
        print("  2. 填入所有必需的 API Keys")
        print("  3. 参考 docs/SECURITY_SETUP.md 获取详细说明")
        sys.exit(1)


if __name__ == "__main__":
    main()
