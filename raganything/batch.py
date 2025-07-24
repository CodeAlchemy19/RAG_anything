"""
Batch processing functionality for RAGAnything

Contains methods for processing multiple documents in batch mode
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, TYPE_CHECKING
import time

from .batch_parser import BatchParser, BatchProcessingResult

if TYPE_CHECKING:
    from .config import RAGAnythingConfig


class BatchMixin:
    """BatchMixin class containing batch processing functionality for RAGAnything"""

    # Type hints for mixin attributes (will be available when mixed into RAGAnything)
    config: "RAGAnythingConfig"
    logger: logging.Logger

    # Type hints for methods that will be available from other mixins
    async def _ensure_lightrag_initialized(self) -> None: ...
    async def process_document_complete(self, file_path: str, **kwargs) -> None: ...

    # ==========================================
    # ORIGINAL BATCH PROCESSING METHOD (RESTORED)
    # ==========================================

    async def process_folder_complete(
        self,
        folder_path: str,
        output_dir: str = None,
        parse_method: str = None,
        display_stats: bool = None,
        split_by_character: str | None = None,
        split_by_character_only: bool = False,
        file_extensions: Optional[List[str]] = None,
        recursive: bool = None,
        max_workers: int = None,
    ):
        """
        Process all files in a folder in batch

        Args:
            folder_path: Path to the folder to process
            output_dir: Parser output directory (defaults to config.parser_output_dir)
            parse_method: Parse method (defaults to config.parse_method)
            display_stats: Whether to display content statistics for each file (defaults to False for batch processing)
            split_by_character: Optional character to split text by
            split_by_character_only: If True, split only by the specified character
            file_extensions: List of file extensions to process (defaults to config.supported_file_extensions)
            recursive: Whether to recursively process subfolders (defaults to config.recursive_folder_processing)
            max_workers: Maximum number of concurrent workers (defaults to config.max_concurrent_files)
        """
        # Ensure LightRAG is initialized
        await self._ensure_lightrag_initialized()

        # Use config defaults if not provided
        if output_dir is None:
            output_dir = self.config.parser_output_dir
        if parse_method is None:
            parse_method = self.config.parse_method
        if display_stats is None:
            display_stats = False  # Default to False for batch processing
        if recursive is None:
            recursive = self.config.recursive_folder_processing
        if max_workers is None:
            max_workers = self.config.max_concurrent_files
        if file_extensions is None:
            file_extensions = self.config.supported_file_extensions

        folder_path = Path(folder_path)
        if not folder_path.exists() or not folder_path.is_dir():
            raise ValueError(
                f"Folder does not exist or is not a valid directory: {folder_path}"
            )

        # Convert file extensions to set for faster lookup
        target_extensions = set(ext.lower().strip() for ext in file_extensions)

        # Log the extensions being used
        self.logger.info(
            f"Processing files with extensions: {sorted(target_extensions)}"
        )

        # Collect all files to process
        files_to_process = []

        if recursive:
            # Recursively traverse all subfolders
            for file_path in folder_path.rglob("*"):
                if (
                    file_path.is_file()
                    and file_path.suffix.lower() in target_extensions
                ):
                    files_to_process.append(file_path)
        else:
            # Process only current folder
            for file_path in folder_path.glob("*"):
                if (
                    file_path.is_file()
                    and file_path.suffix.lower() in target_extensions
                ):
                    files_to_process.append(file_path)

        if not files_to_process:
            self.logger.info(f"No files to process found in {folder_path}")
            return

        self.logger.info(f"Found {len(files_to_process)} files to process")
        self.logger.info("File type distribution:")

        # Count file types
        file_type_count = {}
        for file_path in files_to_process:
            ext = file_path.suffix.lower()
            file_type_count[ext] = file_type_count.get(ext, 0) + 1

        for ext, count in sorted(file_type_count.items()):
            self.logger.info(f"  {ext}: {count} files")

        # Create progress tracking
        processed_count = 0
        failed_files = []

        # Use semaphore to control concurrency
        semaphore = asyncio.Semaphore(max_workers)

        async def process_single_file(file_path: Path, index: int) -> None:
            """Process a single file"""
            async with semaphore:
                nonlocal processed_count
                try:
                    self.logger.info(
                        f"[{index}/{len(files_to_process)}] Processing: {file_path}"
                    )

                    # Create separate output directory for each file
                    file_output_dir = Path(output_dir) / file_path.stem
                    file_output_dir.mkdir(parents=True, exist_ok=True)

                    # Process file
                    await self.process_document_complete(
                        file_path=str(file_path),
                        output_dir=str(file_output_dir),
                        parse_method=parse_method,
                        display_stats=display_stats,
                        split_by_character=split_by_character,
                        split_by_character_only=split_by_character_only,
                    )

                    processed_count += 1
                    self.logger.info(
                        f"[{index}/{len(files_to_process)}] Successfully processed: {file_path}"
                    )

                except Exception as e:
                    self.logger.error(
                        f"[{index}/{len(files_to_process)}] Failed to process: {file_path}"
                    )
                    self.logger.error(f"Error: {str(e)}")
                    failed_files.append((file_path, str(e)))

        # Create all processing tasks
        tasks = []
        for index, file_path in enumerate(files_to_process, 1):
            task = process_single_file(file_path, index)
            tasks.append(task)

        # Wait for all tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)

        # Output processing statistics
        self.logger.info("\n===== Batch Processing Complete =====")
        self.logger.info(f"Total files: {len(files_to_process)}")
        self.logger.info(f"Successfully processed: {processed_count}")
        self.logger.info(f"Failed: {len(failed_files)}")

        if failed_files:
            self.logger.info("\nFailed files:")
            for file_path, error in failed_files:
                self.logger.info(f"  - {file_path}: {error}")

        return {
            "total": len(files_to_process),
            "success": processed_count,
            "failed": len(failed_files),
            "failed_files": failed_files,
        }

    # ==========================================
    # NEW ENHANCED BATCH PROCESSING METHODS
    # ==========================================

    def process_documents_batch(
        self,
        file_paths: List[str],
        output_dir: Optional[str] = None,
        parse_method: Optional[str] = None,
        max_workers: Optional[int] = None,
        recursive: Optional[bool] = None,
        show_progress: bool = True,
        **kwargs,
    ) -> BatchProcessingResult:
        """
        Process multiple documents in batch mode

        Args:
            file_paths: List of file paths or directories to process
            output_dir: Output directory (defaults to config.output_dir)
            parse_method: Parse method (defaults to config.mineru_parse_method)
            max_workers: Maximum number of parallel workers (defaults to config.max_concurrent_files)
            recursive: Whether to search directories recursively (defaults to config.recursive_folder_processing)
            show_progress: Whether to show progress bars
            **kwargs: Additional parameters for parser

        Returns:
            BatchProcessingResult with processing statistics
        """
        # Use config defaults if not provided
        if output_dir is None:
            output_dir = self.config.parser_output_dir
        if parse_method is None:
            parse_method = self.config.mineru_parse_method
        if max_workers is None:
            max_workers = self.config.max_concurrent_files
        if recursive is None:
            recursive = self.config.recursive_folder_processing

        self.logger.info(f"Starting batch processing of {len(file_paths)} paths")

        # Create batch parser
        batch_parser = BatchParser(
            parser_type=self.config.parser,
            max_workers=max_workers,
            show_progress=show_progress,
            timeout_per_file=300,  # 5 minutes per file
        )

        # Process files
        result = batch_parser.process_batch(
            file_paths=file_paths,
            output_dir=output_dir,
            parse_method=parse_method,
            recursive=recursive,
            **kwargs,
        )

        self.logger.info(f"Batch processing completed: {result.summary()}")
        return result

    async def process_documents_batch_async(
        self,
        file_paths: List[str],
        output_dir: Optional[str] = None,
        parse_method: Optional[str] = None,
        max_workers: Optional[int] = None,
        recursive: Optional[bool] = None,
        show_progress: bool = True,
        **kwargs,
    ) -> BatchProcessingResult:
        """
        Async version of batch document processing

        Args:
            file_paths: List of file paths or directories to process
            output_dir: Output directory (defaults to config.output_dir)
            parse_method: Parse method (defaults to config.mineru_parse_method)
            max_workers: Maximum number of parallel workers (defaults to config.max_concurrent_files)
            recursive: Whether to search directories recursively (defaults to config.recursive_folder_processing)
            show_progress: Whether to show progress bars
            **kwargs: Additional parameters for parser

        Returns:
            BatchProcessingResult with processing statistics
        """
        # Use config defaults if not provided
        if output_dir is None:
            output_dir = self.config.parser_output_dir
        if parse_method is None:
            parse_method = self.config.mineru_parse_method
        if max_workers is None:
            max_workers = self.config.max_concurrent_files
        if recursive is None:
            recursive = self.config.recursive_folder_processing

        self.logger.info(f"Starting async batch processing of {len(file_paths)} paths")

        # Create batch parser
        batch_parser = BatchParser(
            parser_type=self.config.parser,
            max_workers=max_workers,
            show_progress=show_progress,
            timeout_per_file=300,  # 5 minutes per file
        )

        # Process files asynchronously
        result = await batch_parser.process_batch_async(
            file_paths=file_paths,
            output_dir=output_dir,
            parse_method=parse_method,
            recursive=recursive,
            **kwargs,
        )

        self.logger.info(f"Async batch processing completed: {result.summary()}")
        return result

    def get_supported_file_extensions(self) -> List[str]:
        """Get list of supported file extensions for batch processing"""
        batch_parser = BatchParser(parser_type=self.config.parser)
        return batch_parser.get_supported_extensions()

    def filter_supported_files(
        self, file_paths: List[str], recursive: Optional[bool] = None
    ) -> List[str]:
        """
        Filter file paths to only include supported file types

        Args:
            file_paths: List of file paths or directories
            recursive: Whether to search directories recursively (defaults to config.recursive_folder_processing)

        Returns:
            List of supported file paths
        """
        if recursive is None:
            recursive = self.config.recursive_folder_processing

        batch_parser = BatchParser(parser_type=self.config.parser)
        return batch_parser.filter_supported_files(file_paths, recursive)

    async def process_documents_with_rag_batch(
        self,
        file_paths: List[str],
        output_dir: Optional[str] = None,
        parse_method: Optional[str] = None,
        max_workers: Optional[int] = None,
        recursive: Optional[bool] = None,
        show_progress: bool = True,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Process multiple documents and insert them into RAG system

        Args:
            file_paths: List of file paths or directories to process
            output_dir: Output directory (defaults to config.output_dir)
            parse_method: Parse method (defaults to config.mineru_parse_method)
            max_workers: Maximum number of parallel workers (defaults to config.max_concurrent_files)
            recursive: Whether to search directories recursively (defaults to config.recursive_folder_processing)
            show_progress: Whether to show progress bars
            **kwargs: Additional parameters for parser

        Returns:
            Dictionary with processing results and RAG statistics
        """
        # Ensure LightRAG is initialized
        await self._ensure_lightrag_initialized()

        start_time = time.time()

        # First, parse all documents
        parse_result = self.process_documents_batch(
            file_paths=file_paths,
            output_dir=output_dir,
            parse_method=parse_method,
            max_workers=max_workers,
            recursive=recursive,
            show_progress=show_progress,
            **kwargs,
        )

        # Then, process each successful file with RAG
        rag_results = {}

        if parse_result.successful_files:
            self.logger.info(
                f"Processing {len(parse_result.successful_files)} files with RAG"
            )

            # Process files with RAG (this could be parallelized in the future)
            for file_path in parse_result.successful_files:
                try:
                    # Process the document with RAG
                    await self.process_document_complete(
                        file_path=file_path,
                        output_dir=output_dir,
                        parse_method=parse_method,
                        **kwargs,
                    )

                    # Get some statistics about the processed content
                    # This would require additional tracking in the RAG system
                    rag_results[file_path] = {"status": "success", "processed": True}

                except Exception as e:
                    self.logger.error(
                        f"Failed to process {file_path} with RAG: {str(e)}"
                    )
                    rag_results[file_path] = {
                        "status": "failed",
                        "error": str(e),
                        "processed": False,
                    }

        processing_time = time.time() - start_time

        return {
            "parse_result": parse_result,
            "rag_results": rag_results,
            "total_processing_time": processing_time,
            "successful_rag_files": len(
                [r for r in rag_results.values() if r["processed"]]
            ),
            "failed_rag_files": len(
                [r for r in rag_results.values() if not r["processed"]]
            ),
        }
