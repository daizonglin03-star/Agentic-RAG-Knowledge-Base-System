"""
网络搜索工具
使用 Tavily API 进行网络搜索
Tavily 是专为 AI 应用设计的搜索 API，国内可直接访问
"""
from typing import Dict, List, Optional
import config

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False
    print("警告: tavily-python 未安装，请运行: pip install tavily-python")


class WebSearchClient:
    """网络搜索客户端（使用 Tavily API）"""
    
    def __init__(self):
        self.api_key = config.WEB_SEARCH_CONFIG.get("api_key", "")
        self.max_results = config.WEB_SEARCH_CONFIG.get("max_results", 5)
        self.search_depth = config.WEB_SEARCH_CONFIG.get("search_depth", "basic")
        
        if TAVILY_AVAILABLE and self.api_key:
            try:
                self.client = TavilyClient(api_key=self.api_key)
            except Exception as e:
                print(f"初始化 Tavily 客户端失败: {e}")
                self.client = None
        else:
            self.client = None
    
    def search(self, query: str) -> Dict:
        """
        执行搜索查询
        
        Args:
            query: 搜索查询字符串
            
        Returns:
            包含搜索结果的字典
        """
        if not TAVILY_AVAILABLE:
            return {
                "success": False,
                "error": "Tavily 未安装，请运行: pip install tavily-python"
            }
        
        if not self.api_key:
            return {
                "success": False,
                "error": "请在 config.py 中配置 Tavily API Key"
            }
        
        if not self.client:
            return {
                "success": False,
                "error": "Tavily 客户端初始化失败"
            }
        
        try:
            # 调用 Tavily 搜索
            response = self.client.search(
                query=query,
                max_results=self.max_results,
                search_depth=self.search_depth,
                include_answer=True,  # 包含 AI 生成的答案摘要
                include_raw_content=False  # 不包含原始 HTML
            )
            
            # 格式化结果
            return self._format_results(response, query)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"搜索失败: {str(e)}"
            }
    
    def _format_results(self, response: Dict, query: str) -> Dict:
        """格式化搜索结果"""
        try:
            # 提取搜索结果
            results = response.get("results", [])
            answer = response.get("answer", "")
            
            # 格式化引用
            citations = []
            for item in results[:self.max_results]:
                citations.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("content", "")
                })
            
            return {
                "success": True,
                "query": query,
                "answer": answer,
                "citations": citations,
                "total_results": len(citations)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"格式化结果失败: {str(e)}",
                "raw_response": response
            }
    
    def format_for_llm(self, search_result: Dict) -> str:
        """
        将搜索结果格式化为适合 LLM 使用的文本
        
        Args:
            search_result: 搜索结果字典
            
        Returns:
            格式化的文本字符串
        """
        if not search_result.get("success"):
            return f"搜索失败: {search_result.get('error', '未知错误')}"
        
        formatted_text = f"网络搜索结果 (查询: {search_result['query']}):\n\n"
        
        # 添加 AI 生成的答案摘要
        if search_result.get("answer"):
            formatted_text += f"搜索摘要:\n{search_result['answer']}\n\n"
        
        # 添加引用来源
        if search_result.get("citations"):
            formatted_text += "相关来源:\n"
            for i, citation in enumerate(search_result["citations"], 1):
                formatted_text += f"\n{i}. {citation['title']}\n"
                formatted_text += f"   链接: {citation['url']}\n"
                if citation.get("snippet"):
                    formatted_text += f"   摘要: {citation['snippet'][:200]}...\n"
        
        return formatted_text


# 创建全局实例
web_search_client = WebSearchClient()
