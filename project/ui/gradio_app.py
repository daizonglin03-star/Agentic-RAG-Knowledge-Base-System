import gradio as gr
from core.chat_interface import ChatInterface
from core.document_manager import DocumentManager
from core.rag_system import RAGSystem
import config

def create_gradio_ui():
    rag_system = RAGSystem()
    rag_system.initialize()
    
    doc_manager = DocumentManager(rag_system)
    chat_interface = ChatInterface(rag_system)
    
    def format_file_list():
        files = doc_manager.get_markdown_files()
        if not files:
            return "📭 No documents available in the knowledge base"
        return "\n".join([f"{f}" for f in files])
    
    def upload_handler(files, progress=gr.Progress()):
        if not files:
            return None, format_file_list()
            
        added, skipped = doc_manager.add_documents(
            files, 
            progress_callback=lambda p, desc: progress(p, desc=desc)
        )
        
        gr.Info(f"✅ Added: {added} | Skipped: {skipped}")
        return None, format_file_list()
    
    def clear_handler():
        doc_manager.clear_all()
        gr.Info(f"🗑️ Removed all documents")
        return format_file_list()
    
    def chat_handler(msg, hist, enable_search):
        return chat_interface.chat(msg, hist, enable_web_search=enable_search)
    
    def clear_chat_handler():
        chat_interface.clear_session()
    
    # 检查网络搜索配置是否完整
    search_configured = bool(config.WEB_SEARCH_CONFIG.get("api_key"))
    
    with gr.Blocks(title="Agentic RAG") as demo:
        
        with gr.Tab("Documents", elem_id="doc-management-tab"):
            gr.Markdown("## Add New Documents")
            gr.Markdown("Upload PDF, Word, or Markdown files. Duplicates will be automatically skipped.")
            
            files_input = gr.File(
                label="Drop PDF or Markdown files here",
                file_count="multiple",
                type="filepath",
                height=200,
                show_label=False
            )
            
            add_btn = gr.Button("Add Documents", variant="primary", size="md")
            
            gr.Markdown("## Current Documents in the Knowledge Base")
            file_list = gr.Textbox(
                value=format_file_list(),
                interactive=False,
                lines = 7,
                max_lines=10,
                elem_id="file-list-box",
                show_label=False
            )
            
            with gr.Row():
                refresh_btn = gr.Button("Refresh", size="md")
                clear_btn = gr.Button("Clear All", variant="stop", size="md")
            
            add_btn.click(
                upload_handler, 
                [files_input], 
                [files_input, file_list], 
                show_progress="corner"
            )
            refresh_btn.click(format_file_list, None, file_list)
            clear_btn.click(clear_handler, None, file_list)
        
        with gr.Tab("Chat"):
            # 添加联网搜索开关
            with gr.Row():
                enable_search_checkbox = gr.Checkbox(
                    label="🌐 启用联网搜索",
                    value=config.ENABLE_WEB_SEARCH,
                    interactive=search_configured,
                    info="通过 Tavily API 获取实时网络信息" if search_configured else "⚠️ 请先在 config.py 中配置 Tavily API Key"
                )
            
            chatbot = gr.Chatbot(
                height=600, 
                placeholder="Ask me anything about your documents!",
                show_label=False
            )
            chatbot.clear(clear_chat_handler)
            
            gr.ChatInterface(
                fn=chat_handler, 
                chatbot=chatbot,
                additional_inputs=[enable_search_checkbox]
            )
    
    return demo