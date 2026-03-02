#!/usr/bin/env python3
"""
预下载所有需要的模型，用于离线使用
在有科学上网的环境下运行此脚本一次即可
"""
import os
import sys
from pathlib import Path

def download_models():
    """下载所有需要的模型"""
    
    print("🚀 开始下载模型...")
    print("=" * 80)
    
    # 临时取消离线模式
    original_offline = os.environ.get('HF_HUB_OFFLINE', None)
    if 'HF_HUB_OFFLINE' in os.environ:
        del os.environ['HF_HUB_OFFLINE']
    
    try:
        # 1. 下载密集嵌入模型
        print("📥 下载密集嵌入模型...")
        from sentence_transformers import SentenceTransformer
        
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        print(f"   模型: {model_name}")
        
        model = SentenceTransformer(model_name)
        print(f"✅ 密集嵌入模型下载完成")
        
        # 2. 下载稀疏嵌入模型
        print("\n📥 下载稀疏嵌入模型...")
        from fastembed import SparseTextEmbedding
        
        sparse_model_name = "Qdrant/bm25"
        print(f"   模型: {sparse_model_name}")
        
        sparse_model = SparseTextEmbedding(model_name=sparse_model_name)
        print(f"✅ 稀疏嵌入模型下载完成")
        
        # 3. 测试模型
        print("\n🧪 测试模型...")
        
        # 测试密集嵌入
        test_text = "这是一个测试文本"
        dense_embedding = model.encode([test_text])
        print(f"   密集嵌入维度: {dense_embedding.shape}")
        
        # 测试稀疏嵌入
        sparse_embedding = list(sparse_model.embed([test_text]))
        print(f"   稀疏嵌入生成成功")
        
        print("\n🎉 所有模型下载并测试完成!")
        print("现在可以在离线环境下使用项目了。")
        
    except Exception as e:
        print(f"\n❌ 模型下载失败: {e}")
        print("请确保:")
        print("1. 网络连接正常")
        print("2. 可以访问Hugging Face")
        print("3. 已安装所需依赖")
        return False
        
    finally:
        # 恢复原始离线设置
        if original_offline is not None:
            os.environ['HF_HUB_OFFLINE'] = original_offline
    
    return True

def check_models():
    """检查模型是否已下载"""
    
    print("🔍 检查已下载的模型...")
    print("=" * 80)
    
    # 检查Hugging Face缓存目录
    cache_dir = Path.home() / ".cache" / "huggingface"
    
    if cache_dir.exists():
        print(f"📁 Hugging Face缓存目录: {cache_dir}")
        
        # 检查transformers模型
        transformers_dir = cache_dir / "transformers"
        if transformers_dir.exists():
            models = list(transformers_dir.glob("models--*"))
            print(f"   Transformers模型: {len(models)} 个")
            for model in models[:5]:  # 显示前5个
                model_name = model.name.replace("models--", "").replace("--", "/")
                print(f"     - {model_name}")
        
        # 检查datasets缓存
        datasets_dir = cache_dir / "datasets"
        if datasets_dir.exists():
            datasets = list(datasets_dir.glob("*"))
            print(f"   Datasets: {len(datasets)} 个")
    
    # 检查fastembed缓存
    fastembed_cache = Path.home() / ".cache" / "fastembed"
    if fastembed_cache.exists():
        print(f"📁 FastEmbed缓存目录: {fastembed_cache}")
        models = list(fastembed_cache.glob("*"))
        print(f"   FastEmbed模型: {len(models)} 个")
        for model in models:
            print(f"     - {model.name}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_models()
    else:
        print("📋 模型下载脚本")
        print("在有科学上网的环境下运行此脚本，预下载所有模型")
        print("\n用法:")
        print("  python download_models.py        # 下载模型")
        print("  python download_models.py check  # 检查已下载的模型")
        print()
        
        if input("是否开始下载模型? (y/N): ").lower() == 'y':
            success = download_models()
            if success:
                print("\n✅ 下载完成! 现在可以设置离线模式:")
                print("export HF_HUB_OFFLINE=1")
            else:
                print("\n❌ 下载失败，请检查网络连接")
        else:
            print("取消下载")