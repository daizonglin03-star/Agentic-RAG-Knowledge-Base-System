from typing import List
from langchain_core.tools import tool
from db.parent_store_manager import ParentStoreManager
from mcp_search import web_search_client
import config

class ToolFactory:
    
    def __init__(self, collection, enable_web_search=False):
        self.collection = collection
        self.parent_store_manager = ParentStoreManager()
        self.enable_web_search = enable_web_search
    
    def _search_child_chunks(self, query: str, limit: int) -> str:
        """Search for the top K most relevant child chunks.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
        """
        try:
            results = self.collection.similarity_search(query, k=limit, score_threshold=0.3)
            if not results:
                return "NO_RELEVANT_CHUNKS"

            return "\n\n".join([
                f"Parent ID: {doc.metadata.get('parent_id', '')}\n"
                f"File Name: {doc.metadata.get('source', '')}\n"
                f"Content: {doc.page_content.strip()}"
                for doc in results
            ])            

        except Exception as e:
            return f"RETRIEVAL_ERROR: {str(e)}"
    
    def _retrieve_many_parent_chunks(self, parent_ids: List[str]) -> str:
        """Retrieve full parent chunks by their IDs.
    
        Args:
            parent_ids: List of parent chunk IDs to retrieve
        """
        try:
            ids = [parent_ids] if isinstance(parent_ids, str) else list(parent_ids)
            raw_parents = self.parent_store_manager.load_content_many(ids)
            if not raw_parents:
                return "NO_PARENT_DOCUMENTS"

            return "\n\n".join([
                f"Parent ID: {doc.get('parent_id', 'n/a')}\n"
                f"File Name: {doc.get('metadata', {}).get('source', 'unknown')}\n"
                f"Content: {doc.get('content', '').strip()}"
                for doc in raw_parents
            ])            

        except Exception as e:
            return f"PARENT_RETRIEVAL_ERROR: {str(e)}"
    
    def _retrieve_parent_chunks(self, parent_id: str) -> str:
        """Retrieve full parent chunks by their IDs.
    
        Args:
            parent_id: Parent chunk ID to retrieve
        """
        try:
            parent = self.parent_store_manager.load_content(parent_id)
            if not parent:
                return "NO_PARENT_DOCUMENT"

            return (
                f"Parent ID: {parent.get('parent_id', 'n/a')}\n"
                f"File Name: {parent.get('metadata', {}).get('source', 'unknown')}\n"
                f"Content: {parent.get('content', '').strip()}"
            )          

        except Exception as e:
            return f"PARENT_RETRIEVAL_ERROR: {str(e)}"
    
    def _web_search(self, query: str) -> str:
        """Search the web using Tavily API.
        
        Args:
            query: Search query string
        """
        try:
            if not self.enable_web_search:
                return "WEB_SEARCH_DISABLED: Web search is not enabled."
            
            search_result = web_search_client.search(query)
            
            if not search_result.get("success"):
                return f"WEB_SEARCH_ERROR: {search_result.get('error', 'Unknown error')}"
            
            # 格式化搜索结果供 LLM 使用
            formatted_result = web_search_client.format_for_llm(search_result)
            return formatted_result
            
        except Exception as e:
            return f"WEB_SEARCH_ERROR: {str(e)}"
    
    def create_tools(self) -> List:
        """Create and return the list of tools."""
        search_tool = tool("search_child_chunks")(self._search_child_chunks)
        retrieve_tool = tool("retrieve_parent_chunks")(self._retrieve_parent_chunks)
        
        tools = [search_tool, retrieve_tool]
        
        # 如果启用了联网搜索，添加搜索工具
        if self.enable_web_search:
            web_search_tool = tool("web_search")(self._web_search)
            tools.append(web_search_tool)
        
        return tools