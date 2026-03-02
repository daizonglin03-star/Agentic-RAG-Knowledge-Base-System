import os
import config
from pathlib import Path
import glob
import logging
from oss_utils import OSSManager
from mineru_utils import MineRUProcessor
from word_utils import WordProcessor

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def pdf_to_markdown_mineru(pdf_path, output_dir):
    """
    使用MineRU API将PDF转换为Markdown
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    
    print(f"\n🚀 开始使用 MineRU 处理PDF")
    print("=" * 80)
    print(f"📄 文件名: {pdf_path.name}")
    print(f"📏 文件大小: {pdf_path.stat().st_size / 1024:.1f} KB")
    print(f"📂 输出目录: {output_dir}")
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
    
    # 初始化OSS管理器和MineRU处理器
    print(f"\n🔧 初始化服务...")
    oss_manager = OSSManager()
    mineru_processor = MineRUProcessor()
    
    oss_key = f"pdfs/{pdf_path.name}"
    
    try:
        # 1. 上传PDF到OSS
        print(f"\n📤 步骤1: 上传PDF到OSS")
        print("-" * 40)
        pdf_url = oss_manager.upload_file(str(pdf_path), oss_key)
        
        # 2. 使用MineRU处理PDF
        print(f"\n🤖 步骤2: MineRU处理PDF")
        print("-" * 40)
        processing_options = {
            "output_format": "markdown",
            "extract_images": False,
            "preserve_layout": True,
            "ocr_enabled": True,
            "table_recognition": True
        }
        
        markdown_content = mineru_processor.process_pdf_sync(pdf_url, processing_options)
        
        # 3. 保存Markdown文件
        print(f"\n💾 步骤3: 保存Markdown文件")
        print("-" * 40)
        output_path = output_dir / pdf_path.with_suffix(".md").name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ 文件保存成功")
        print(f"   输出路径: {output_path}")
        print(f"   内容长度: {len(markdown_content)} 字符")
        print(f"   估算行数: {len(markdown_content.split())} 行")
        
        # 4. 清理OSS文件
        print(f"\n🧹 步骤4: 清理临时文件")
        print("-" * 40)
        if oss_manager.delete_file(oss_key):
            print(f"✅ OSS临时文件已清理")
        else:
            print(f"⚠️  OSS文件清理失败，但不影响结果")
        
        print("=" * 80)
        print(f"🎉 MineRU处理完成!")
        print(f"   输出文件: {output_path}")
        print(f"   处理方式: MineRU (高级)")
        
        return str(output_path)
        
    except Exception as e:
        print(f"\n❌ MineRU处理失败: {e}")
        logger.error(f"MineRU处理失败 {pdf_path.name}: {e}")
        
        # 尝试清理OSS文件
        print(f"🧹 清理OSS临时文件...")
        try:
            oss_manager.delete_file(oss_key)
            print(f"✅ OSS文件已清理")
        except:
            print(f"⚠️  OSS文件清理失败")
        
        raise

def pdf_to_markdown_legacy(pdf_path, output_dir):
    """
    使用pymupdf4llm的传统方法（作为备用）
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
    """
    print(f"\n📚 使用传统方法 (pymupdf4llm) 处理PDF")
    print("=" * 80)
    print(f"� 文件名: {Path(pdf_path).name}")
    
    try:
        import pymupdf
        import pymupdf4llm
        
        print(f"📖 正在解析PDF文件...")
        doc = pymupdf.open(pdf_path)
        
        print(f"�🔄 转换为Markdown格式...")
        md = pymupdf4llm.to_markdown(doc, header=False, footer=False, page_separators=True, ignore_images=True, write_images=False, image_path=None)
        md_cleaned = md.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='ignore')
        
        print(f"💾 保存Markdown文件...")
        output_path = Path(output_dir) / Path(doc.name).stem
        final_path = output_path.with_suffix(".md")
        final_path.write_bytes(md_cleaned.encode('utf-8'))
        
        print("=" * 80)
        print(f"🎉 传统方法处理完成!")
        print(f"   输出文件: {final_path}")
        print(f"   内容长度: {len(md_cleaned)} 字符")
        print(f"   处理方式: 传统方法 (pymupdf4llm)")
        
        return str(final_path)
        
    except ImportError:
        print("❌ pymupdf4llm 不可用，无法使用传统方法")
        logger.error("pymupdf4llm not available for legacy processing")
        raise

def pdf_to_markdown(pdf_path, output_dir, use_mineru=True):
    """
    将PDF转换为Markdown，优先使用MineRU，失败时回退到传统方法
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
        use_mineru: 是否使用MineRU（默认True）
    """
    print(f"\n� PDF处理任务开始")
    print(f"   文件: {Path(pdf_path).name}")
    print(f"   首选方法: {'MineRU (高级)' if use_mineru else '传统方法 (pymupdf4llm)'}")
    
    if use_mineru:
        try:
            result_path = pdf_to_markdown_mineru(pdf_path, output_dir)
            print(f"\n✨ 最终结果: 使用 MineRU 成功处理!")
            return result_path
        except Exception as e:
            print(f"\n⚠️  MineRU处理失败，错误: {e}")
            print(f"🔄 自动切换到传统方法...")
            logger.warning(f"MineRU processing failed, falling back to legacy method: {e}")
    
    # 回退到传统方法
    result_path = pdf_to_markdown_legacy(pdf_path, output_dir)
    print(f"\n✨ 最终结果: 使用传统方法 (pymupdf4llm) 处理!")
    return result_path

def pdfs_to_markdowns(path_pattern, overwrite: bool = False, use_mineru: bool = True):
    """
    批量将PDF转换为Markdown
    
    Args:
        path_pattern: PDF文件路径模式
        overwrite: 是否覆盖已存在的文件
        use_mineru: 是否使用MineRU
    """
    output_dir = Path(config.MARKDOWN_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(map(Path, glob.glob(path_pattern)))
    
    print(f"\n📋 批量PDF处理任务")
    print("=" * 80)
    print(f"   模式: {path_pattern}")
    print(f"   找到文件: {len(pdf_files)} 个")
    print(f"   处理方法: {'MineRU (高级)' if use_mineru else '传统方法 (pymupdf4llm)'}")
    print(f"   覆盖模式: {'是' if overwrite else '否'}")
    
    if not pdf_files:
        print(f"❌ 未找到匹配的PDF文件")
        return
    
    processed_count = 0
    skipped_count = 0
    failed_count = 0
    
    for i, pdf_path in enumerate(pdf_files, 1):
        md_path = (output_dir / pdf_path.stem).with_suffix(".md")
        
        print(f"\n📄 处理文件 {i}/{len(pdf_files)}: {pdf_path.name}")
        
        if not overwrite and md_path.exists():
            print(f"⏭️  跳过 (文件已存在): {md_path}")
            skipped_count += 1
            continue
            
        try:
            logger.info(f"Processing PDF: {pdf_path}")
            pdf_to_markdown(pdf_path, output_dir, use_mineru=use_mineru)
            processed_count += 1
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            logger.error(f"Failed to process {pdf_path}: {e}")
            failed_count += 1
    
    print(f"\n📊 批量处理完成")
    print("=" * 80)
    print(f"   成功处理: {processed_count} 个文件")
    print(f"   跳过文件: {skipped_count} 个文件")
    print(f"   失败文件: {failed_count} 个文件")
    print(f"   总计文件: {len(pdf_files)} 个文件")
    
    if failed_count > 0:
        print(f"\n⚠️  有 {failed_count} 个文件处理失败，请检查日志")

# 强制使用MineRU的便捷函数
def force_mineru_processing(pdf_path, output_dir="markdown_docs"):
    """
    强制使用MineRU处理PDF（不回退到传统方法）
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
        
    Returns:
        输出文件路径
    """
    print(f"\n🎯 强制使用MineRU处理模式")
    return pdf_to_markdown_mineru(pdf_path, output_dir)

def word_to_markdown(word_path, output_dir, method="auto"):
    """
    将Word文档转换为Markdown
    
    Args:
        word_path: Word文档路径
        output_dir: 输出目录
        method: 转换方法 ("auto", "native", "python-docx", "antiword")
        
    Returns:
        输出文件路径
    """
    print(f"\n📄 Word文档处理任务开始")
    print(f"   文件: {Path(word_path).name}")
    print(f"   方法: {method}")
    
    word_processor = WordProcessor()
    return word_processor.word_to_markdown(word_path, output_dir, method)

def words_to_markdowns(path_pattern, overwrite: bool = False, method: str = "auto"):
    """
    批量将Word文档转换为Markdown
    
    Args:
        path_pattern: Word文档路径模式
        overwrite: 是否覆盖已存在的文件
        method: 转换方法 ("auto", "native", "python-docx", "antiword")
    """
    output_dir = Path(config.MARKDOWN_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 支持多种Word文档格式
    word_files = []
    for pattern in [path_pattern.replace('*', '*.docx'), path_pattern.replace('*', '*.doc')]:
        word_files.extend(list(map(Path, glob.glob(pattern))))
    
    # 去重并排序
    word_files = sorted(list(set(word_files)))
    
    print(f"\n📋 批量Word文档处理任务")
    print("=" * 80)
    print(f"   模式: {path_pattern}")
    print(f"   找到文件: {len(word_files)} 个")
    print(f"   处理方法: {method}")
    print(f"   覆盖模式: {'是' if overwrite else '否'}")
    
    if not word_files:
        print(f"❌ 未找到匹配的Word文档")
        return
    
    processed_count = 0
    skipped_count = 0
    failed_count = 0
    
    for i, word_path in enumerate(word_files, 1):
        md_path = (output_dir / word_path.stem).with_suffix(".md")
        
        print(f"\n📄 处理文件 {i}/{len(word_files)}: {word_path.name}")
        
        if not overwrite and md_path.exists():
            print(f"⏭️  跳过 (文件已存在): {md_path}")
            skipped_count += 1
            continue
            
        try:
            logger.info(f"Processing Word document: {word_path}")
            word_to_markdown(word_path, output_dir, method=method)
            processed_count += 1
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            logger.error(f"Failed to process {word_path}: {e}")
            failed_count += 1
    
    print(f"\n📊 批量处理完成")
    print("=" * 80)
    print(f"   成功处理: {processed_count} 个文件")
    print(f"   跳过文件: {skipped_count} 个文件")
    print(f"   失败文件: {failed_count} 个文件")
    print(f"   总计文件: {len(word_files)} 个文件")
    
    if failed_count > 0:
        print(f"\n⚠️  有 {failed_count} 个文件处理失败，请检查日志")

def documents_to_markdowns(path_pattern, overwrite: bool = False, use_mineru: bool = True, word_method: str = "auto"):
    """
    批量将文档（PDF和Word）转换为Markdown
    
    Args:
        path_pattern: 文档路径模式
        overwrite: 是否覆盖已存在的文件
        use_mineru: PDF是否使用MineRU
        word_method: Word文档转换方法
    """
    output_dir = Path(config.MARKDOWN_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 查找所有支持的文档格式
    all_files = []
    for ext in ['*.pdf', '*.docx', '*.doc']:
        pattern = path_pattern.replace('*', ext)
        all_files.extend(list(map(Path, glob.glob(pattern))))
    
    # 去重并排序
    all_files = sorted(list(set(all_files)))
    
    print(f"\n📋 批量文档处理任务")
    print("=" * 80)
    print(f"   模式: {path_pattern}")
    print(f"   找到文件: {len(all_files)} 个")
    print(f"   PDF方法: {'MineRU (高级)' if use_mineru else '传统方法 (pymupdf4llm)'}")
    print(f"   Word方法: {word_method}")
    print(f"   覆盖模式: {'是' if overwrite else '否'}")
    
    if not all_files:
        print(f"❌ 未找到匹配的文档文件")
        return
    
    # 按文件类型分组
    pdf_files = [f for f in all_files if f.suffix.lower() == '.pdf']
    word_files = [f for f in all_files if f.suffix.lower() in ['.docx', '.doc']]
    
    print(f"   PDF文件: {len(pdf_files)} 个")
    print(f"   Word文件: {len(word_files)} 个")
    
    total_processed = 0
    total_skipped = 0
    total_failed = 0
    
    # 处理PDF文件
    if pdf_files:
        print(f"\n🔴 处理PDF文件...")
        for pdf_file in pdf_files:
            try:
                pdfs_to_markdowns(str(pdf_file), overwrite=overwrite, use_mineru=use_mineru)
                total_processed += 1
            except Exception as e:
                print(f"❌ PDF处理失败 {pdf_file.name}: {e}")
                total_failed += 1
    
    # 处理Word文件
    if word_files:
        print(f"\n🔵 处理Word文件...")
        for word_file in word_files:
            md_path = (output_dir / word_file.stem).with_suffix(".md")
            
            if not overwrite and md_path.exists():
                print(f"⏭️  跳过 (文件已存在): {word_file.name}")
                total_skipped += 1
                continue
            
            try:
                word_to_markdown(word_file, output_dir, method=word_method)
                total_processed += 1
            except Exception as e:
                print(f"❌ Word处理失败 {word_file.name}: {e}")
                total_failed += 1
    
    print(f"\n📊 批量文档处理完成")
    print("=" * 80)
    print(f"   成功处理: {total_processed} 个文件")
    print(f"   跳过文件: {total_skipped} 个文件")
    print(f"   失败文件: {total_failed} 个文件")
    print(f"   总计文件: {len(all_files)} 个文件")
    
    if total_failed > 0:
        print(f"\n⚠️  有 {total_failed} 个文件处理失败，请检查日志")