#!/usr/bin/env python3
"""
离线启动脚本
确保在完全离线环境下启动RAG系统
"""
import os
import sys
from pathlib import Path

def setup_offline_environment():
    """设置离线环境变量"""
    
    print("🔧 设置离线环境...")
    
    # 设置所有相关的离线环境变量
    offline_vars = {
        "HF_HUB_OFFLINE": "1",
        "TRANSFORMERS_OFFLINE": "1", 
        "HF_DATASETS_OFFLINE": "1",
        "TOKENIZERS_PARALLELISM": "false",
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "DISABLE_TELEMETRY": "1"
    }
    
    for key, value in offline_vars.items():
        os.environ[key] = value
        print(f"   {key}: {value}")
    
    print("✅ 离线环境设置完成")

def check_offline_models():
    """检查离线模型是否可用"""
    
    print("\n🔍 检查离线模型...")
    
    try:
        # 检查密集嵌入模型
        print("   检查密集嵌入模型...")
        from sentence_transformers import SentenceTransformer
        
        # 强制使用本地文件
        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            local_files_only=True
        )
        test_embedding = model.encode(["测试文本"])
        print(f"   ✅ 密集嵌入模型可用 (维度: {test_embedding.shape[1]})")
        
    except Exception as e:
        print(f"   ❌ 密集嵌入模型不可用: {e}")
        print(f"   💡 请先运行: python download_models.py")
        return False
    
    try:
        # 检查稀疏嵌入模型
        print("   检查稀疏嵌入模型...")
        from fastembed import SparseTextEmbedding
        sparse_model = SparseTextEmbedding(model_name="Qdrant/bm25")
        print(f"   ✅ 稀疏嵌入模型可用")
        
    except Exception as e:
        print(f"   ⚠️  稀疏嵌入模型不可用: {e}")
        print(f"   💡 将使用简单稀疏嵌入回退方案")
    
    return True

def start_application():
    """启动应用程序"""
    
    print("\n🚀 启动RAG应用...")
    
    try:
        # 直接运行app.py的内容
        import gradio as gr
        from ui.css import custom_css
        from ui.gradio_app import create_gradio_ui
        
        demo = create_gradio_ui()
        print("✅ Gradio界面创建成功")
        print("🌐 启动Web服务器...")
        
        # 启动应用
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            debug=False,
            show_error=True,
            inbrowser=True
        )
        
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")
        print("\n💡 故障排除建议:")
        print("1. 确保已预下载所有模型: python download_models.py")
        print("2. 检查依赖是否完整: pip install -r requirements.txt")
        print("3. 确保Ollama服务正在运行: ollama serve")
        print("4. 尝试清除缓存后重新下载模型")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """主函数"""
    
    print("🎯 RAG系统离线启动器")
    print("=" * 80)
    
    # 设置离线环境
    setup_offline_environment()
    
    # 检查模型
    if not check_offline_models():
        print("\n❌ 模型检查失败")
        print("💡 请先在有网络的环境下运行: python download_models.py")
        return
    
    # 启动应用
    if start_application():
        print("\n✅ 应用启动成功!")
    else:
        print("\n❌ 应用启动失败")

if __name__ == "__main__":
    main()