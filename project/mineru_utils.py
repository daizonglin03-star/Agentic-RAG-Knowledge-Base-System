"""
MineRU API utilities for advanced PDF processing
"""
import requests
import time
import json
from typing import Dict, Any, Optional
import config
import logging

logger = logging.getLogger(__name__)

class MineRUProcessor:
    """MineRU API处理器，用于高质量PDF转换"""
    
    def __init__(self):
        self.api_url = config.MINERU_CONFIG["api_url"]
        self.api_key = config.MINERU_CONFIG["api_key"]
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        print(f"🔧 MineRU处理器初始化完成")
        print(f"   API地址: {self.api_url}")
        print(f"   API密钥: {self.api_key[:20]}...{self.api_key[-10:]}")
    
    def submit_pdf_processing(self, pdf_url: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        提交PDF处理任务
        
        Args:
            pdf_url: PDF文件的公网访问URL
            options: 处理选项配置
            
        Returns:
            任务ID
        """
        if options is None:
            options = {
                "output_format": "markdown",
                "extract_images": False,
                "preserve_layout": True,
                "ocr_enabled": True,
                "table_recognition": True
            }
        
        payload = {
            "url": pdf_url,
            "options": options
        }
        
        print(f"📤 提交PDF处理任务到MineRU...")
        print(f"   PDF URL: {pdf_url}")
        print(f"   处理选项: {options}")
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            print(f"   HTTP状态码: {response.status_code}")
            print(f"   响应内容: {response.text[:200]}...")
            
            response.raise_for_status()
            
            result = response.json()
            
            # 修复：正确解析task_id的位置
            if result.get("code") == 0 and "data" in result and "task_id" in result["data"]:
                task_id = result["data"]["task_id"]
                print(f"✅ 任务提交成功，任务ID: {task_id}")
                logger.info(f"PDF processing task submitted: {task_id}")
                return task_id
            else:
                # 如果响应格式不符合预期，尝试直接获取task_id
                task_id = result.get("task_id")
                if task_id:
                    print(f"✅ 任务提交成功，任务ID: {task_id}")
                    logger.info(f"PDF processing task submitted: {task_id}")
                    return task_id
                else:
                    raise ValueError(f"MineRU API响应格式异常: {result}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 提交任务失败 - 网络错误: {e}")
            logger.error(f"Failed to submit PDF processing task: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ 提交任务失败 - JSON解析错误: {e}")
            print(f"   原始响应: {response.text}")
            logger.error(f"Invalid JSON response from MineRU API: {e}")
            raise
        except Exception as e:
            print(f"❌ 提交任务失败 - 未知错误: {e}")
            raise
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态信息
        """
        # 使用正确的状态查询URL
        status_url = f"https://mineru.net/api/v4/extract/task/{task_id}"
        
        try:
            response = requests.get(
                status_url,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # 处理MineRU API的响应格式
                if result.get("code") == 0 and "data" in result:
                    return result["data"]
                else:
                    return result
            else:
                raise requests.exceptions.RequestException(f"HTTP {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️  获取任务状态失败: {e}")
            logger.error(f"Failed to get task status: {e}")
            raise
    
    def get_task_result(self, task_id: str) -> str:
        """
        获取任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            处理后的markdown内容
        """
        # 尝试不同的结果获取URL格式
        possible_urls = [
            f"https://mineru.net/api/v4/extract/task/{task_id}/result",
            f"https://mineru.net/api/v4/extract/{task_id}/result",
            f"https://mineru.net/api/v4/task/{task_id}/result",
            f"https://mineru.net/api/v4/result/{task_id}",
            f"{self.api_url}/{task_id}/result",
        ]
        
        for result_url in possible_urls:
            try:
                print(f"   尝试结果URL: {result_url}")
                response = requests.get(
                    result_url,
                    headers=self.headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ 结果获取成功")
                    
                    # 处理MineRU API的响应格式
                    if result.get("code") == 0 and "data" in result:
                        data = result["data"]
                        markdown_content = data.get("content") or data.get("markdown") or data.get("result") or data.get("text")
                    else:
                        markdown_content = result.get("content") or result.get("markdown") or result.get("result") or result.get("text")
                    
                    if markdown_content:
                        print(f"✅ 获取处理结果成功，内容长度: {len(markdown_content)} 字符")
                        return markdown_content
                    else:
                        print(f"   响应中没有找到内容: {result}")
                        continue
                        
                elif response.status_code == 404:
                    print(f"   404 - URL不存在，尝试下一个")
                    continue
                else:
                    print(f"   状态码: {response.status_code}")
                    continue
                    
            except requests.exceptions.RequestException as e:
                print(f"   请求失败: {e}")
                continue
        
        # 如果所有URL都失败，抛出异常
        raise ValueError(f"所有结果获取URL都失败，task_id: {task_id}")
    
    def wait_for_completion(self, task_id: str, max_wait_time: int = 300, poll_interval: int = 10) -> str:
        """
        等待任务完成并获取结果
        
        Args:
            task_id: 任务ID
            max_wait_time: 最大等待时间（秒）
            poll_interval: 轮询间隔（秒）
            
        Returns:
            处理后的markdown内容
        """
        start_time = time.time()
        print(f"⏳ 等待MineRU处理完成...")
        print(f"   任务ID: {task_id}")
        print(f"   最大等待时间: {max_wait_time}秒")
        print(f"   轮询间隔: {poll_interval}秒")
        
        while time.time() - start_time < max_wait_time:
            try:
                status_info = self.get_task_status(task_id)
                
                # MineRU API使用 'state' 字段而不是 'status'
                state = status_info.get("state", "unknown")
                elapsed = int(time.time() - start_time)
                
                print(f"   [{elapsed:3d}s] 状态: {state}")
                logger.info(f"Task {task_id} state: {state}")
                
                if state == "done" or state == "completed" or state == "success" or state == "finished":
                    print(f"🎉 任务完成! 总耗时: {elapsed}秒")
                    
                    # 检查是否有zip文件URL
                    zip_url = status_info.get("full_zip_url")
                    if zip_url:
                        print(f"📦 发现ZIP文件: {zip_url}")
                        return self.download_and_extract_result(zip_url)
                    else:
                        # 尝试传统的结果获取方式
                        return self.get_task_result(task_id)
                        
                elif state == "failed" or state == "error":
                    error_msg = status_info.get("err_msg", "Unknown error")
                    print(f"❌ 任务失败: {error_msg}")
                    raise RuntimeError(f"MineRU任务失败: {error_msg}")
                elif state in ["pending", "processing", "running", "queued"]:
                    print(f"   继续等待...")
                    time.sleep(poll_interval)
                else:
                    print(f"⚠️  未知状态: {state}，继续等待...")
                    logger.warning(f"Unknown task state: {state}")
                    time.sleep(poll_interval)
                    
            except Exception as e:
                print(f"⚠️  检查状态时出错: {e}")
                logger.error(f"Error while waiting for task completion: {e}")
                time.sleep(poll_interval)
        
        print(f"⏰ 任务超时 (超过 {max_wait_time} 秒)")
        raise TimeoutError(f"MineRU任务超时: {task_id}")
    
    def download_and_extract_result(self, zip_url: str) -> str:
        """
        下载并提取ZIP文件中的markdown内容
        
        Args:
            zip_url: ZIP文件的URL
            
        Returns:
            提取的markdown内容
        """
        import zipfile
        import io
        
        print(f"📥 下载处理结果: {zip_url}")
        
        try:
            # 下载ZIP文件
            response = requests.get(zip_url, timeout=60)
            response.raise_for_status()
            
            print(f"✅ ZIP文件下载成功，大小: {len(response.content)} 字节")
            
            # 解压ZIP文件
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                file_list = zip_file.namelist()
                print(f"📁 ZIP文件包含: {file_list}")
                
                # 查找markdown文件
                markdown_files = [f for f in file_list if f.endswith('.md')]
                
                if markdown_files:
                    # 使用第一个markdown文件
                    md_file = markdown_files[0]
                    print(f"📄 提取markdown文件: {md_file}")
                    
                    with zip_file.open(md_file) as f:
                        content = f.read().decode('utf-8')
                        print(f"✅ 成功提取内容，长度: {len(content)} 字符")
                        return content
                else:
                    # 如果没有markdown文件，查找其他文本文件
                    text_files = [f for f in file_list if f.endswith(('.txt', '.json'))]
                    if text_files:
                        text_file = text_files[0]
                        print(f"📄 提取文本文件: {text_file}")
                        
                        with zip_file.open(text_file) as f:
                            content = f.read().decode('utf-8')
                            print(f"✅ 成功提取内容，长度: {len(content)} 字符")
                            return content
                    else:
                        raise ValueError(f"ZIP文件中未找到可用的文本内容: {file_list}")
            
        except Exception as e:
            print(f"❌ 下载或解压ZIP文件失败: {e}")
            raise
    
    def process_pdf_sync(self, pdf_url: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        同步处理PDF（提交任务并等待完成）
        
        Args:
            pdf_url: PDF文件的公网访问URL
            options: 处理选项配置
            
        Returns:
            处理后的markdown内容
        """
        print(f"🚀 开始MineRU同步处理...")
        task_id = self.submit_pdf_processing(pdf_url, options)
        return self.wait_for_completion(task_id)