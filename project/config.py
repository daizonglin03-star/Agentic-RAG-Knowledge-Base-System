import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# --- Directory Configuration ---
MARKDOWN_DIR = "markdown_docs"
PARENT_STORE_PATH = "parent_store"
QDRANT_DB_PATH = "qdrant_db"

# --- Qdrant Configuration ---
CHILD_COLLECTION = "document_child_chunks"
SPARSE_VECTOR_NAME = "sparse"

# --- Model Configuration ---
# 使用更小的本地模型，避免网络问题
DENSE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SPARSE_MODEL = "Qdrant/bm25"
LLM_MODEL = "qwen3:4b-instruct-2507-q4_K_M"
LLM_TEMPERATURE = 0.1

# --- Offline Mode Configuration ---
# 离线模式设置，当无法访问网络时使用
OFFLINE_MODE = True  # 设置为True启用离线模式
FALLBACK_TO_SIMPLE_SPARSE = True  # 如果BM25不可用，回退到简单方法

# --- Text Splitter Configuration ---
CHILD_CHUNK_SIZE = 300
CHILD_CHUNK_OVERLAP = 50
MIN_PARENT_SIZE = 1000
MAX_PARENT_SIZE = 10000
HEADERS_TO_SPLIT_ON = [
    ("#", "H1"),
    ("##", "H2"),
    ("###", "H3")
]

# --- OSS Configuration ---
OSS_CONFIG = {
    "endpoint": os.getenv("OSS_ENDPOINT", "https://oss-cn-beijing.aliyuncs.com"),
    "bucket": os.getenv("OSS_BUCKET", ""),
    "access_key": os.getenv("OSS_ACCESS_KEY", ""),
    "secret_key": os.getenv("OSS_SECRET_KEY", ""),
}

# --- MineRU Configuration ---
# 请根据你的MineRU服务提供商填入正确的API地址
# 常见的可能地址：
# - https://openxlab.org.cn/api/v1/mineru/process
# - https://api.openxlab.org.cn/v1/process  
# - 或者联系你的服务提供商获取正确地址
MINERU_CONFIG = {
    "api_url": os.getenv("MINERU_API_URL", "https://mineru.net/api/v4/extract/task"),
    "api_key": os.getenv("MINERU_API_KEY", ""),
    "timeout": int(os.getenv("MINERU_TIMEOUT", "300")),
}

# --- Web Search Configuration ---
# 网络搜索配置（使用 Tavily API）
# Tavily 是专为 AI 应用设计的搜索 API，国内可直接访问
# 获取 API Key: https://tavily.com/
WEB_SEARCH_CONFIG = {
    "api_key": os.getenv("TAVILY_API_KEY", ""),
    "max_results": int(os.getenv("WEB_SEARCH_MAX_RESULTS", "5")),
    "search_depth": os.getenv("WEB_SEARCH_DEPTH", "basic"),
}

# 是否启用联网搜索功能（默认关闭）
ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "False").lower() == "true"
