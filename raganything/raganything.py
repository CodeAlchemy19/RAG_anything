"""
Complete MinerU parsing + multimodal content insertion Pipeline

This script integrates:
1. MinerU document parsing
2. Pure text content LightRAG insertion
3. Specialized processing for multimodal content (using different processors)
"""

import os
from typing import Dict, Any, Optional, Callable
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Add project root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lightrag import LightRAG
from lightrag.utils import logger
from dotenv import load_dotenv

# Load environment variables from .env file
# The OS environment variables take precedence over the .env file
load_dotenv(dotenv_path=".env", override=False)

# Import configuration and modules
from raganything.config import RAGAnythingConfig
from raganything.query import QueryMixin
from raganything.processor import ProcessorMixin
from raganything.batch import BatchMixin
from raganything.utils import get_processor_supports
from raganything.mineru_parser import MineruParser

# Import specialized processors
from raganything.modalprocessors import (
    ImageModalProcessor,
    TableModalProcessor,
    EquationModalProcessor,
    GenericModalProcessor,
)


@dataclass
class RAGAnything(QueryMixin, ProcessorMixin, BatchMixin):
    """Multimodal Document Processing Pipeline - Complete document parsing and insertion pipeline"""

    # Core Components
    # ---
    lightrag: Optional[LightRAG] = field(default=None)
    """Optional pre-initialized LightRAG instance."""

    llm_model_func: Optional[Callable] = field(default=None)
    """LLM model function for text analysis."""

    vision_model_func: Optional[Callable] = field(default=None)
    """Vision model function for image analysis."""

    embedding_func: Optional[Callable] = field(default=None)
    """Embedding function for text vectorization."""

    config: Optional[RAGAnythingConfig] = field(default=None)
    """Configuration object, if None will create with environment variables."""

    # Internal State
    # ---
    modal_processors: Dict[str, Any] = field(default_factory=dict, init=False)
    """Dictionary of multimodal processors."""

    def __post_init__(self):
        """Post-initialization setup following LightRAG pattern"""
        # Initialize configuration if not provided
        if self.config is None:
            self.config = RAGAnythingConfig()

        # Set working directory
        self.working_dir = self.config.working_dir

        # Set up logger (use existing logger, don't configure it)
        self.logger = logger

        # Create working directory if needed
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)
            self.logger.info(f"Created working directory: {self.working_dir}")

        # If LightRAG is provided, initialize processors immediately
        if self.lightrag is not None:
            self._initialize_processors()

        # Log configuration info
        self.logger.info("RAGAnything initialized with config:")
        self.logger.info(f"  Working directory: {self.config.working_dir}")
        self.logger.info(f"  MinerU parse method: {self.config.mineru_parse_method}")
        self.logger.info(
            f"  Multimodal processing - Image: {self.config.enable_image_processing}, "
            f"Table: {self.config.enable_table_processing}, "
            f"Equation: {self.config.enable_equation_processing}"
        )
        self.logger.info(f"  Max concurrent files: {self.config.max_concurrent_files}")

    def _initialize_processors(self):
        """Initialize multimodal processors with appropriate model functions"""
        if self.lightrag is None:
            raise ValueError(
                "LightRAG instance must be initialized before creating processors"
            )

        # Create different multimodal processors based on configuration
        self.modal_processors = {}

        if self.config.enable_image_processing:
            self.modal_processors["image"] = ImageModalProcessor(
                lightrag=self.lightrag,
                modal_caption_func=self.vision_model_func or self.llm_model_func,
            )

        if self.config.enable_table_processing:
            self.modal_processors["table"] = TableModalProcessor(
                lightrag=self.lightrag, modal_caption_func=self.llm_model_func
            )

        if self.config.enable_equation_processing:
            self.modal_processors["equation"] = EquationModalProcessor(
                lightrag=self.lightrag, modal_caption_func=self.llm_model_func
            )

        # Always include generic processor as fallback
        self.modal_processors["generic"] = GenericModalProcessor(
            lightrag=self.lightrag, modal_caption_func=self.llm_model_func
        )

        self.logger.info("Multimodal processors initialized")
        self.logger.info(f"Available processors: {list(self.modal_processors.keys())}")

    def update_config(self, **kwargs):
        """Update configuration with new values"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                self.logger.debug(f"Updated config: {key} = {value}")
            else:
                self.logger.warning(f"Unknown config parameter: {key}")

    async def _ensure_lightrag_initialized(self):
        """Ensure LightRAG instance is initialized, create if necessary"""
        if self.lightrag is not None:
            return

        # Check MinerU 2.0 installation
        if not MineruParser.check_installation():
            raise RuntimeError(
                "MinerU 2.0 is not properly installed. "
                "Please install it using: pip install -U 'mineru[core]' "
                "or uv pip install -U 'mineru[core]'"
            )

        # Validate required functions
        if self.llm_model_func is None:
            raise ValueError(
                "llm_model_func must be provided when LightRAG is not pre-initialized"
            )
        if self.embedding_func is None:
            raise ValueError(
                "embedding_func must be provided when LightRAG is not pre-initialized"
            )

        from lightrag.kg.shared_storage import initialize_pipeline_status

        # Create LightRAG instance with provided functions
        self.lightrag = LightRAG(
            working_dir=self.working_dir,
            llm_model_func=self.llm_model_func,
            embedding_func=self.embedding_func,
        )

        await self.lightrag.initialize_storages()
        await initialize_pipeline_status()

        # Initialize processors after LightRAG is ready
        self._initialize_processors()

        self.logger.info("LightRAG and multimodal processors initialized")

    def check_mineru_installation(self) -> bool:
        """
        Check if MinerU 2.0 is properly installed

        Returns:
            bool: True if MinerU 2.0 is properly installed
        """
        return MineruParser.check_installation()

    def get_config_info(self) -> Dict[str, Any]:
        """Get current configuration information"""
        return {
            "directory": {
                "working_dir": self.config.working_dir,
                "mineru_output_dir": self.config.mineru_output_dir,
            },
            "parsing": {
                "mineru_parse_method": self.config.mineru_parse_method,
                "display_content_stats": self.config.display_content_stats,
            },
            "multimodal_processing": {
                "enable_image_processing": self.config.enable_image_processing,
                "enable_table_processing": self.config.enable_table_processing,
                "enable_equation_processing": self.config.enable_equation_processing,
            },
            "batch_processing": {
                "max_concurrent_files": self.config.max_concurrent_files,
                "supported_file_extensions": self.config.supported_file_extensions,
                "recursive_folder_processing": self.config.recursive_folder_processing,
            },
            "logging": {
                "note": "Logging fields have been removed - configure logging externally",
            },
        }

    def get_processor_info(self) -> Dict[str, Any]:
        """Get processor information"""
        base_info = {
            "mineru_installed": MineruParser.check_installation(),
            "config": self.get_config_info(),
            "models": {
                "llm_model": "External function"
                if self.llm_model_func
                else "Not provided",
                "vision_model": "External function"
                if self.vision_model_func
                else "Not provided",
                "embedding_model": "External function"
                if self.embedding_func
                else "Not provided",
            },
        }

        if not self.modal_processors:
            base_info["status"] = "Not initialized"
            base_info["processors"] = {}
        else:
            base_info["status"] = "Initialized"
            base_info["processors"] = {}

            for proc_type, processor in self.modal_processors.items():
                base_info["processors"][proc_type] = {
                    "class": processor.__class__.__name__,
                    "supports": get_processor_supports(proc_type),
                    "enabled": True,
                }

        return base_info
