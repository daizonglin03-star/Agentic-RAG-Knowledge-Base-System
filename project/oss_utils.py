"""
OSS (Object Storage Service) utilities for file upload and management
"""
import os
import oss2
from pathlib import Path
from typing import Optional
import config
import logging

logger = logging.getLogger(__name__)

class OSSManager:
    """管理OSS文件上传和下载操作"""
    
    def __init__(self):
        print(f"🔧 OSS管理器初始化...")
        print(f"   Endpoint: {config.OSS_CONFIG['endpoint']}")
        print(f"   Bucket: {config.OSS_CONFIG['bucket']}")
        print(f"   Access Key: {config.OSS_CONFIG['access_key'][:8]}...{config.OSS_CONFIG['access_key'][-4:]}")
        
        self.auth = oss2.Auth(
            config.OSS_CONFIG["access_key"], 
            config.OSS_CONFIG["secret_key"]
        )
        self.bucket = oss2.Bucket(
            self.auth, 
            config.OSS_CONFIG["endpoint"], 
            config.OSS_CONFIG["bucket"]
        )
        
        # 测试连接
        try:
            bucket_info = self.bucket.get_bucket_info()
            print(f"✅ OSS连接成功")
            print(f"   存储类型: {bucket_info.storage_class}")
            print(f"   创建时间: {bucket_info.creation_date}")
        except Exception as e:
            print(f"❌ OSS连接失败: {e}")
            raise
    
    def upload_file(self, local_file_path: str, oss_key: Optional[str] = None) -> str:
        """
        上传文件到OSS
        
        Args:
            local_file_path: 本地文件路径
            oss_key: OSS中的文件键名，如果为None则使用文件名
            
        Returns:
            OSS文件的公网访问URL
        """
        local_path = Path(local_file_path)
        if not local_path.exists():
            raise FileNotFoundError(f"本地文件不存在: {local_file_path}")
        
        if oss_key is None:
            oss_key = f"pdfs/{local_path.name}"
        
        file_size = local_path.stat().st_size
        print(f"📤 开始上传文件到OSS...")
        print(f"   本地文件: {local_file_path}")
        print(f"   文件大小: {file_size / 1024:.1f} KB")
        print(f"   OSS键名: {oss_key}")
        
        try:
            # 上传文件
            result = self.bucket.put_object_from_file(oss_key, local_file_path)
            print(f"✅ 文件上传成功")
            print(f"   ETag: {result.etag}")
            logger.info(f"File uploaded successfully: {oss_key}")
            
            # 生成公网访问URL
            url = f"https://{config.OSS_CONFIG['bucket']}.{config.OSS_CONFIG['endpoint'].replace('https://', '')}/{oss_key}"
            print(f"   公网URL: {url}")
            return url
            
        except Exception as e:
            print(f"❌ 文件上传失败: {e}")
            logger.error(f"Failed to upload file to OSS: {e}")
            raise
    
    def delete_file(self, oss_key: str) -> bool:
        """
        删除OSS中的文件
        
        Args:
            oss_key: OSS中的文件键名
            
        Returns:
            删除是否成功
        """
        try:
            print(f"🗑️  删除OSS文件: {oss_key}")
            self.bucket.delete_object(oss_key)
            print(f"✅ 文件删除成功")
            logger.info(f"File deleted successfully: {oss_key}")
            return True
        except Exception as e:
            print(f"⚠️  文件删除失败: {e}")
            logger.error(f"Failed to delete file from OSS: {e}")
            return False
    
    def file_exists(self, oss_key: str) -> bool:
        """
        检查OSS中文件是否存在
        
        Args:
            oss_key: OSS中的文件键名
            
        Returns:
            文件是否存在
        """
        try:
            self.bucket.head_object(oss_key)
            return True
        except oss2.exceptions.NoSuchKey:
            return False
        except Exception as e:
            logger.error(f"Error checking file existence: {e}")
            return False