import os
# 设置离线模式，必须在导入任何HuggingFace相关库之前设置
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

import gradio as gr
from ui.css import custom_css
from ui.gradio_app import create_gradio_ui

if __name__ == "__main__":
    demo = create_gradio_ui()
    print("\n🚀 Launching RAG Assistant...")
    
    # 使用简单的启动配置，避免网络检查问题
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=False,
        show_error=True,
        inbrowser=True
    )