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
        self, 
        file_paths: List[str], 
        recursive: Optional[bool] = None
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
        total_content_blocks = 0

        if parse_result.successful_files:
            self.logger.info(f"Processing {len(parse_result.successful_files)} files with RAG")

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
                    rag_results[file_path] = {
                        "status": "success",
                        "processed": True
                    }
                    
                except Exception as e:
                    self.logger.error(f"Failed to process {file_path} with RAG: {str(e)}")
                    rag_results[file_path] = {
                        "status": "failed",
                        "error": str(e),
                        "processed": False
                    }

        processing_time = time.time() - start_time

        return {
            "parse_result": parse_result,
            "rag_results": rag_results,
            "total_processing_time": processing_time,
            "successful_rag_files": len([r for r in rag_results.values() if r["processed"]]),
            "failed_rag_files": len([r for r in rag_results.values() if not r["processed"]]),
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
