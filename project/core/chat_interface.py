from langchain_core.messages import HumanMessage

class ChatInterface:
    
    def __init__(self, rag_system):
        self.rag_system = rag_system
        
    def chat(self, message, history, enable_web_search=False):

        if not self.rag_system.agent_graph:
            return "⚠️ System not initialized!"
        
        # 如果搜索开关状态改变，需要重新初始化系统
        if enable_web_search != self.rag_system.enable_web_search:
            self.rag_system.enable_web_search = enable_web_search
            self.rag_system.initialize()
            
        try:
            result = self.rag_system.agent_graph.invoke(
                {"messages": [HumanMessage(content=message.strip())]},
                self.rag_system.get_config()
            )
            return result["messages"][-1].content
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def clear_session(self):
        self.rag_system.reset_thread()