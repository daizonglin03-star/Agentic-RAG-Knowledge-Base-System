import os
import config

# 根据配置设置离线模式
if getattr(config, 'OFFLINE_MODE', True):
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_DATASETS_OFFLINE"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

class SimpleSparseEmbedding:
    """简单的稀疏嵌入实现，用作BM25的回退方案"""
    
    def __init__(self):
        print("⚠️  使用简单稀疏嵌入（BM25回退方案）")
    
    def embed_documents(self, texts):
        """为文档生成简单的稀疏嵌入"""
        embeddings = []
        for text in texts:
            # 简单的词频统计
            words = text.lower().split()
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
            
            # 转换为稀疏向量格式
            indices = []
            values = []
            for i, (word, count) in enumerate(word_counts.items()):
                indices.append(hash(word) % 10000)  # 简单哈希映射
                values.append(float(count))
            
            embeddings.append((indices, values))
        return embeddings
    
    def embed_query(self, text):
        """为查询生成稀疏嵌入"""
        return self.embed_documents([text])[0]

class VectorDbManager:
    __client: QdrantClient
    __dense_embeddings: HuggingFaceEmbeddings
    __sparse_embeddings = None
    
    def __init__(self):
        self.__client = QdrantClient(path=config.QDRANT_DB_PATH)
        
        # 强制使用本地缓存初始化密集嵌入
        try:
            print("🔄 初始化密集嵌入模型...")
            self.__dense_embeddings = HuggingFaceEmbeddings(
                model_name=config.DENSE_MODEL,
                model_kwargs={'local_files_only': True}  # 强制仅使用本地文件
            )
            print("✅ 密集嵌入模型初始化成功")
        except Exception as e:
            print(f"⚠️  本地模式失败，尝试标准模式: {e}")
            try:
                self.__dense_embeddings = HuggingFaceEmbeddings(model_name=config.DENSE_MODEL)
                print("✅ 密集嵌入模型初始化成功（标准模式）")
            except Exception as e2:
                print(f"❌ 密集嵌入模型初始化失败: {e2}")
                raise
        
        # 尝试加载稀疏嵌入，失败时使用回退方案
        self.__sparse_embeddings = self._init_sparse_embeddings()

    def _init_sparse_embeddings(self):
        """初始化稀疏嵌入，支持回退方案"""
        try:
            from langchain_qdrant import FastEmbedSparse
            print("🔄 尝试加载BM25稀疏嵌入...")
            sparse_embeddings = FastEmbedSparse(model_name=config.SPARSE_MODEL)
            print("✅ BM25稀疏嵌入加载成功")
            return sparse_embeddings
        except Exception as e:
            print(f"⚠️  BM25稀疏嵌入加载失败: {e}")
            
            if getattr(config, 'FALLBACK_TO_SIMPLE_SPARSE', True):
                print("🔄 使用简单稀疏嵌入回退方案...")
                return SimpleSparseEmbedding()
            else:
                print("❌ 稀疏嵌入不可用，将仅使用密集嵌入")
                return None

    def create_collection(self, collection_name):
        if not self.__client.collection_exists(collection_name):
            print(f"Creating collection: {collection_name}...")
            
            # 基础向量配置
            vectors_config = qmodels.VectorParams(
                size=len(self.__dense_embeddings.embed_query("test")), 
                distance=qmodels.Distance.COSINE
            )
            
            # 稀疏向量配置（如果可用）
            sparse_vectors_config = None
            if self.__sparse_embeddings is not None:
                sparse_vectors_config = {
                    config.SPARSE_VECTOR_NAME: qmodels.SparseVectorParams()
                }
            
            self.__client.create_collection(
                collection_name=collection_name,
                vectors_config=vectors_config,
                sparse_vectors_config=sparse_vectors_config,
            )
            print(f"✓ Collection created: {collection_name}")
        else:
            print(f"✓ Collection already exists: {collection_name}")

    def delete_collection(self, collection_name):
        try:
            if self.__client.collection_exists(collection_name):
                print(f"Removing existing Qdrant collection: {collection_name}")
                self.__client.delete_collection(collection_name)
        except Exception as e:
            print(f"Warning: could not delete collection {collection_name}: {e}")

    def get_collection(self, collection_name) -> QdrantVectorStore:
        try:
            # 根据稀疏嵌入可用性选择检索模式
            if self.__sparse_embeddings is not None and hasattr(self.__sparse_embeddings, 'embed_query'):
                # 使用混合检索
                return QdrantVectorStore(
                    client=self.__client,
                    collection_name=collection_name,
                    embedding=self.__dense_embeddings,
                    sparse_embedding=self.__sparse_embeddings,
                    retrieval_mode=RetrievalMode.HYBRID,
                    sparse_vector_name=config.SPARSE_VECTOR_NAME
                )
            else:
                # 仅使用密集嵌入
                print("⚠️  仅使用密集嵌入检索（稀疏嵌入不可用）")
                return QdrantVectorStore(
                    client=self.__client,
                    collection_name=collection_name,
                    embedding=self.__dense_embeddings,
                    retrieval_mode=RetrievalMode.DENSE
                )
        except Exception as e:
            print(f"Unable to get collection {collection_name}: {e}")
            return None