from pathlib import Path
import shutil
import config
from util import pdfs_to_markdowns, word_to_markdown

class DocumentManager:

    def __init__(self, rag_system):
        self.rag_system = rag_system
        self.markdown_dir = Path(config.MARKDOWN_DIR)
        self.markdown_dir.mkdir(parents=True, exist_ok=True)
        
    def add_documents(self, document_paths, progress_callback=None):
        if not document_paths:
            return 0, 0
            
        document_paths = [document_paths] if isinstance(document_paths, str) else document_paths
        document_paths = [p for p in document_paths if p and Path(p).suffix.lower() in [".pdf", ".md", ".docx", ".doc"]]
        
        if not document_paths:
            return 0, 0
            
        added = 0
        skipped = 0
            
        for i, doc_path in enumerate(document_paths):
            if progress_callback:
                progress_callback((i + 1) / len(document_paths), f"Processing {Path(doc_path).name}")
                
            doc_name = Path(doc_path).stem
            md_path = self.markdown_dir / f"{doc_name}.md"
            
            if md_path.exists():
                skipped += 1
                continue
                
            try:            
                if Path(doc_path).suffix.lower() == ".md":
                    shutil.copy(doc_path, md_path)
                elif Path(doc_path).suffix.lower() == ".pdf":
                    # 明确使用MineRU处理PDF
                    pdfs_to_markdowns(str(doc_path), overwrite=False, use_mineru=True)
                elif Path(doc_path).suffix.lower() in [".docx", ".doc"]:
                    # 处理Word文档
                    word_to_markdown(str(doc_path), str(self.markdown_dir), method="auto")
                else:
                    print(f"不支持的文件格式: {Path(doc_path).suffix}")
                    skipped += 1
                    continue
                    
                parent_chunks, child_chunks = self.rag_system.chunker.create_chunks_single(md_path)
                
                if not child_chunks:
                    skipped += 1
                    continue
                
                collection = self.rag_system.vector_db.get_collection(self.rag_system.collection_name)
                if collection is None:
                    print(f"Error: Could not get collection for {doc_path}")
                    skipped += 1
                    continue
                    
                collection.add_documents(child_chunks)
                self.rag_system.parent_store.save_many(parent_chunks)
                
                added += 1
                
            except Exception as e:
                print(f"Error processing {doc_path}: {e}")
                skipped += 1
            
        return added, skipped
    
    def get_markdown_files(self):
        if not self.markdown_dir.exists():
            return []
        files = []
        for p in self.markdown_dir.glob("*.md"):
            # 显示原始文件名，支持多种格式
            original_name = p.name.replace(".md", "")
            # 尝试推断原始文件类型
            if (self.markdown_dir.parent / f"{original_name}.pdf").exists():
                files.append(f"{original_name}.pdf")
            elif (self.markdown_dir.parent / f"{original_name}.docx").exists():
                files.append(f"{original_name}.docx")
            elif (self.markdown_dir.parent / f"{original_name}.doc").exists():
                files.append(f"{original_name}.doc")
            else:
                files.append(f"{original_name}.md")
        return sorted(files)
    
    def clear_all(self):
        if self.markdown_dir.exists():
            shutil.rmtree(self.markdown_dir)
            self.markdown_dir.mkdir(parents=True, exist_ok=True)
        
        self.rag_system.parent_store.clear_store()
        self.rag_system.vector_db.delete_collection(self.rag_system.collection_name)
        self.rag_system.vector_db.create_collection(self.rag_system.collection_name)