<center><h1>🚀 RAG-Anything: All-in-One RAG System</h1></center>

<div align="center">
<table border="0" width="100%">
<tr>
<td width="100" align="center">
<img src="./assets/logo.png" width="80" height="80" alt="raganything">
</td>
<td>

<div>
    <p>
        <a href='https://github.com/HKUDS/RAG-Anything'><img src='https://img.shields.io/badge/Project-Page-Green'></a>
        <a href='https://arxiv.org/abs/2410.05779'><img src='https://img.shields.io/badge/arXiv-2410.05779-b31b1b'></a>
        <a href='https://github.com/HKUDS/LightRAG'><img src='https://img.shields.io/badge/Based%20on-LightRAG-blue'></a>
    </p>
    <p>
        <img src='https://img.shields.io/github/stars/HKUDS/RAG-Anything?color=green&style=social' />
        <img src="https://img.shields.io/badge/python-3.9+-blue">
        <a href="https://pypi.org/project/raganything/"><img src="https://img.shields.io/pypi/v/raganything.svg"></a>
    </p>
    <p>
        <a href="README_zh.md">中文版</a> | <a href="README.md">English</a>
    </p>
</div>
</td>
</tr>
</table>

<!-- Add architecture diagram here when available -->
<!-- <img src="./assets/raganything_architecture.png" width="800" alt="RAGAnything Architecture"> -->

</div>

## 🌟 Overview

Modern documents increasingly contain diverse multimodal content—text, images, tables, equations, charts, and multimedia—that traditional text-focused RAG systems cannot effectively process. **RAG-Anything** addresses this challenge as a comprehensive **All-in-One Multimodal Document Processing RAG system** built on [LightRAG](https://github.com/HKUDS/LightRAG).

As a unified solution, RAG-Anything **eliminates the need for multiple specialized tools**. It provides **seamless processing and querying across all content modalities** within a single integrated framework. Unlike conventional RAG approaches that struggle with non-textual elements, our all-in-one system delivers **comprehensive multimodal retrieval capabilities**.

Users can query documents containing **interleaved text**, **visual diagrams**, **structured tables**, and **mathematical formulations** through **one cohesive interface**. This consolidated approach makes RAG-Anything particularly valuable for academic research, technical documentation, financial reports, and enterprise knowledge management where rich, mixed-content documents demand a **unified processing framework**.

### Key Features of RAG-Anything

- 🔄 **End-to-End Multimodal Pipeline**: Complete workflow from document ingestion and parsing to intelligent multimodal query answering.

- 📄 **Universal Document Support**: Seamless processing of PDFs, Office documents (DOC/DOCX/PPT/PPTX/XLS/XLSX), images, and diverse file formats.

- 🧠 **Specialized Content Analysis**: Dedicated processors for images, tables, mathematical equations, and heterogeneous content types.

- 🔗 **Multimodal Knowledge Graph**: Automatic entity extraction and cross-modal relationship discovery for enhanced understanding.

- ⚡ **Adaptive Processing Modes**: Flexible MinerU-based parsing or direct multimodal content injection workflows.

- 🎯 **Hybrid Intelligent Retrieval**: Advanced search capabilities spanning textual and multimodal content with contextual understanding.

## 🏗️ Algorithm & Architecture

### Core Algorithm

**RAG-Anything** implements an effective **multi-stage multimodal pipeline** that fundamentally extends traditional RAG architectures to seamlessly handle diverse content modalities through intelligent orchestration and cross-modal understanding.

#### 1. Document Parsing Stage
The system provides high-fidelity document extraction through adaptive content decomposition. It intelligently segments heterogeneous elements while preserving contextual relationships. Universal format compatibility is achieved via specialized optimized parsers.

- **⚙️ MinerU Integration**: Leverages [MinerU](https://github.com/opendatalab/MinerU) for high-fidelity document structure extraction and semantic preservation across complex layouts.

- **🧩 Adaptive Content Decomposition**: Automatically segments documents into coherent text blocks, visual elements, structured tables, mathematical equations, and specialized content types while preserving contextual relationships.

- **📁 Universal Format Support**: Provides comprehensive handling of PDFs, Office documents (DOC/DOCX/PPT/PPTX/XLS/XLSX), images, and emerging formats through specialized parsers with format-specific optimization.

#### 2. Multi-Modal Content Understanding & Processing
The system automatically categorizes and routes content through optimized channels. It uses concurrent pipelines for parallel text and multimodal processing. Document hierarchy and relationships are preserved during transformation.

- **🎯 Autonomous Content Categorization and Routing**: Automatically identify, categorize, and route different content types through optimized execution channels.

- **⚡ Concurrent Multi-Pipeline Architecture**: Implements concurrent execution of textual and multimodal content through dedicated processing pipelines. This approach maximizes throughput efficiency while preserving content integrity.

- **🏗️ Document Hierarchy Extraction**: Extracts and preserves original document hierarchy and inter-element relationships during content transformation.

#### 3. Multimodal Analysis Engine
The system deploys modality-aware processing units for heterogeneous data modalities:

- **🔍 Visual Content Analyzer**:
  - Integrate vision model for image analysis.
  - Generates context-aware descriptive captions based on visual semantics.
  - Extracts spatial relationships and hierarchical structures between visual elements.

- **📊 Structured Data Interpreter**:
  - Performs systematic interpretation of tabular and structured data formats.
  - Implements statistical pattern recognition algorithms for data trend analysis.
  - Identifies semantic relationships and dependencies across multiple tabular datasets.

- **📐 Mathematical Expression Parser**:
  - Parses complex mathematical expressions and formulas with high accuracy.
  - Provides native LaTeX format support for seamless integration with academic workflows.
  - Establishes conceptual mappings between mathematical equations and domain-specific knowledge bases.

- **🔧 Extensible Modality Handler**:
  - Provides configurable processing framework for custom and emerging content types.
  - Enables dynamic integration of new modality processors through plugin architecture.
  - Supports runtime configuration of processing pipelines for specialized use cases.

#### 4. Multi-Modal Knowledge Graph Index
The multi-modal knowledge graph construction module transforms document content into structured semantic representations. It extracts multimodal entities, establishes cross-modal relationships, and preserves hierarchical organization. The system applies weighted relevance scoring for optimized knowledge retrieval.

- **🔍 Multi-Modal Entity Extraction**: Transforms significant multimodal elements into structured knowledge graph entities. The process includes semantic annotations and metadata preservation.

- **🔗 Cross-Modal Relationship Mapping**: Establishes semantic connections and dependencies between textual entities and multimodal components. This is achieved through automated relationship inference algorithms.

- **🏗️ Hierarchical Structure Preservation**: Maintains original document organization through "belongs_to" relationship chains. These chains preserve logical content hierarchy and sectional dependencies.

- **⚖️ Weighted Relationship Scoring**: Assigns quantitative relevance scores to relationship types. Scoring is based on semantic proximity and contextual significance within the document structure.

#### 5. Modality-Aware Retrieval
The hybrid retrieval system combines vector similarity search with graph traversal algorithms for comprehensive content retrieval. It implements modality-aware ranking mechanisms and maintains relational coherence between retrieved elements to ensure contextually integrated information delivery.

-  **🔀 Vector-Graph Fusion**: Integrates vector similarity search with graph traversal algorithms. This approach leverages both semantic embeddings and structural relationships for comprehensive content retrieval.

- **📊 Modality-Aware Ranking**: Implements adaptive scoring mechanisms that weight retrieval results based on content type relevance. The system adjusts rankings according to query-specific modality preferences.

- **🔗 Relational Coherence Maintenance**: Maintains semantic and structural relationships between retrieved elements. This ensures coherent information delivery and contextual integrity.

## 🚀 Quick Start

### Installation

#### Option 1: Install from PyPI (Recommended)
```bash
pip install raganything
```

#### Option 2: Install from Source
```bash
git clone https://github.com/HKUDS/RAG-Anything.git
cd RAG-Anything
pip install -e .
```

#### MinerU Dependencies (Optional)
For document parsing capabilities with MinerU 2.0:
```bash
# Install MinerU 2.0
pip install -U 'mineru[core]'

# Or using uv (faster)
uv pip install -U 'mineru[core]'
```

> **⚠️ Important Changes in MinerU 2.0:**
> - Package name changed from `magic-pdf` to `mineru`
> - LibreOffice integration removed (Office documents require manual PDF conversion)
> - Simplified command-line interface with `mineru` command
> - New backend options and improved performance

Check MinerU installation:
```bash
# Verify installation
mineru --version

# Check if properly configured
python -c "from raganything import RAGAnything; rag = RAGAnything(); print('✅ MinerU installed properly' if rag.check_mineru_installation() else '❌ MinerU installation issue')"
```

Models are downloaded automatically on first use. For manual download, refer to [MinerU Model Source Configuration](https://github.com/opendatalab/MinerU/blob/master/README.md#22-model-source-configuration).

### Usage

#### End-to-End Document Processing

```python
import asyncio
from raganything import RAGAnything
from lightrag.llm.openai import openai_complete_if_cache, openai_embed

async def main():
    # Initialize RAGAnything
    rag = RAGAnything(
        working_dir="./rag_storage",
        llm_model_func=lambda prompt, system_prompt=None, history_messages=[], **kwargs: openai_complete_if_cache(
            "gpt-4o-mini",
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key="your-api-key",
            **kwargs,
        ),
        vision_model_func=lambda prompt, system_prompt=None, history_messages=[], image_data=None, **kwargs: openai_complete_if_cache(
            "gpt-4o",
            "",
            system_prompt=None,
            history_messages=[],
            messages=[
                {"role": "system", "content": system_prompt} if system_prompt else None,
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                    }
                ]} if image_data else {"role": "user", "content": prompt}
            ],
            api_key="your-api-key",
            **kwargs,
        ) if image_data else openai_complete_if_cache(
            "gpt-4o-mini",
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key="your-api-key",
            **kwargs,
        ),
        embedding_func=lambda texts: openai_embed(
            texts,
            model="text-embedding-3-large",
            api_key="your-api-key",
        ),
        embedding_dim=3072,
        max_token_size=8192
    )

    # Process a document
    await rag.process_document_complete(
        file_path="path/to/your/document.pdf",
        output_dir="./output",
        parse_method="auto"
    )

    # Query the processed content
    result = await rag.query_with_multimodal(
        "What are the main findings shown in the figures and tables?",
        mode="hybrid"
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

#### Direct Multimodal Content Processing

```python
import asyncio
from lightrag import LightRAG
from raganything.modalprocessors import ImageModalProcessor, TableModalProcessor

async def process_multimodal_content():
    # Initialize LightRAG
    rag = LightRAG(
        working_dir="./rag_storage",
        # ... your LLM and embedding configurations
    )
    await rag.initialize_storages()

    # Process an image
    image_processor = ImageModalProcessor(
        lightrag=rag,
        modal_caption_func=your_vision_model_func
    )

    image_content = {
        "img_path": "path/to/image.jpg",
        "img_caption": ["Figure 1: Experimental results"],
        "img_footnote": ["Data collected in 2024"]
    }

    description, entity_info = await image_processor.process_multimodal_content(
        modal_content=image_content,
        content_type="image",
        file_path="research_paper.pdf",
        entity_name="Experimental Results Figure"
    )

    # Process a table
    table_processor = TableModalProcessor(
        lightrag=rag,
        modal_caption_func=your_llm_model_func
    )

    table_content = {
        "table_body": """
        | Method | Accuracy | F1-Score |
        |--------|----------|----------|
        | RAGAnything | 95.2% | 0.94 |
        | Baseline | 87.3% | 0.85 |
        """,
        "table_caption": ["Performance Comparison"],
        "table_footnote": ["Results on test dataset"]
    }

    description, entity_info = await table_processor.process_multimodal_content(
        modal_content=table_content,
        content_type="table",
        file_path="research_paper.pdf",
        entity_name="Performance Results Table"
    )

if __name__ == "__main__":
    asyncio.run(process_multimodal_content())
```

### Batch Processing

```python
# Process multiple documents
await rag.process_folder_complete(
    folder_path="./documents",
    output_dir="./output",
    file_extensions=[".pdf", ".docx", ".pptx"],
    recursive=True,
    max_workers=4
)
```

### Custom Modal Processors

```python
from raganything.modalprocessors import GenericModalProcessor

class CustomModalProcessor(GenericModalProcessor):
    async def process_multimodal_content(self, modal_content, content_type, file_path, entity_name):
        # Your custom processing logic
        enhanced_description = await self.analyze_custom_content(modal_content)
        entity_info = self.create_custom_entity(enhanced_description, entity_name)
        return await self._create_entity_and_chunk(enhanced_description, entity_info, file_path)
```

### Query Options

```python
# Different query modes
result_hybrid = await rag.query_with_multimodal("Your question", mode="hybrid")
result_local = await rag.query_with_multimodal("Your question", mode="local")
result_global = await rag.query_with_multimodal("Your question", mode="global")
```

## 🛠️ Examples

The `examples/` directory contains comprehensive usage examples:

- **`raganything_example.py`**: End-to-end document processing with MinerU
- **`modalprocessors_example.py`**: Direct multimodal content processing
- **`office_document_test.py`**: Office document parsing test with MinerU (no API key required)
- **`image_format_test.py`**: Image format parsing test with MinerU (no API key required)
- **`text_format_test.py`**: Text format parsing test with MinerU (no API key required)

Run examples:
```bash
# End-to-end processing
python examples/raganything_example.py path/to/document.pdf --api-key YOUR_API_KEY

# Direct modal processing
python examples/modalprocessors_example.py --api-key YOUR_API_KEY

# Office document parsing test (MinerU only)
python examples/office_document_test.py --file path/to/document.docx

# Image format parsing test (MinerU only)
python examples/image_format_test.py --file path/to/image.bmp

# Text format parsing test (MinerU only)
python examples/text_format_test.py --file path/to/document.md

# Check LibreOffice installation
python examples/office_document_test.py --check-libreoffice --file dummy

# Check PIL/Pillow installation
python examples/image_format_test.py --check-pillow --file dummy

# Check ReportLab installation
python examples/text_format_test.py --check-reportlab --file dummy
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file (refer to `.env.example`):
```bash
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=your_base_url  # Optional
```

> **Note**: API keys are only required for full RAG processing with LLM integration. The parsing test files (`office_document_test.py` and `image_format_test.py`) only test MinerU functionality and do not require API keys.

### MinerU Configuration

MinerU 2.0 uses a simplified configuration approach:

```bash
# MinerU 2.0 uses command-line parameters instead of config files
# Check available options:
mineru --help

# Common configurations:
mineru -p input.pdf -o output_dir -m auto    # Automatic parsing mode
mineru -p input.pdf -o output_dir -m ocr     # OCR-focused parsing
mineru -p input.pdf -o output_dir -b pipeline --device cuda  # GPU acceleration
```

You can also configure MinerU through RAGAnything parameters:
```python
# Configure parsing behavior
await rag.process_document_complete(
    file_path="document.pdf",
    parse_method="auto",     # or "ocr", "txt"
    device="cuda",           # GPU acceleration
    backend="pipeline",      # parsing backend
    lang="en"               # language optimization
)
```

> **Note**: MinerU 2.0 no longer uses the `magic-pdf.json` configuration file. All settings are now passed as command-line parameters or function arguments.

## 🧪 Supported Content Types

### Document Formats
- **PDFs**: Research papers, reports, presentations
- **Office Documents**: DOC, DOCX, PPT, PPTX, XLS, XLSX ⚠️
- **Images**: JPG, PNG, BMP, TIFF, GIF, WebP 📸
- **Text Files**: TXT, MD ⚠️

> **⚠️ Office Document Processing Requirements:**
>
> RAG-Anything supports comprehensive Office document processing through automatic PDF conversion:
> - **Supported formats**: .doc, .docx, .ppt, .pptx, .xls, .xlsx
> - **LibreOffice requirement**: Automatic conversion requires LibreOffice installation
> - **Installation instructions**:
>   - **Windows**: Download from [LibreOffice official website](https://www.libreoffice.org/download/download/)
>   - **macOS**: `brew install --cask libreoffice`
>   - **Ubuntu/Debian**: `sudo apt-get install libreoffice`
>   - **CentOS/RHEL**: `sudo yum install libreoffice`
> - **Alternative approach**: Convert to PDF manually for optimal performance
> - **Processing workflow**: Office files are automatically converted to PDF, then processed by MinerU

> **📸 Image Format Support:**
>
> RAG-Anything supports comprehensive image format processing:
> - **MinerU native formats**: .jpg, .jpeg, .png (processed directly)
> - **Auto-converted formats**: .bmp, .tiff/.tif, .gif, .webp (automatically converted to PNG)
> - **Conversion requirements**: PIL/Pillow library (`pip install Pillow`)
> - **Processing workflow**: Non-native formats are converted to PNG, then processed by MinerU
> - **Quality preservation**: Conversion maintains image quality while ensuring compatibility

> **⚠️ Text File Processing Requirements:**
>
> RAG-Anything supports text file processing through automatic PDF conversion:
> - **Supported formats**: .txt, .md
> - **ReportLab requirement**: Automatic conversion requires ReportLab library
> - **Installation**: `pip install reportlab`
> - **Features**: Supports multiple text encodings (UTF-8, GBK, Latin-1, CP1252)
> - **Complete Markdown support**: Headers, paragraphs, **bold**, *italic*, ~~strikethrough~~, `inline code`, code blocks, tables, lists, quotes, links, images, and horizontal rules
> - **Advanced features**: Auto-scaling images, nested lists, multi-level quotes, syntax-highlighted code blocks
> - **Cross-platform fonts**: Automatic Chinese font detection for Windows/macOS
> - **Processing workflow**: Text files are automatically converted to PDF, then processed by MinerU


### Multimodal Elements
- **Images**: Photographs, diagrams, charts, screenshots
- **Tables**: Data tables, comparison charts, statistical summaries
- **Equations**: Mathematical formulas in LaTeX format
- **Generic Content**: Custom content types via extensible processors

## 📖 Citation

If you find RAG-Anything useful in your research, please cite our paper:

```bibtex
@article{guo2024lightrag,
  title={LightRAG: Simple and Fast Retrieval-Augmented Generation},
  author={Zirui Guo and Lianghao Xia and Yanhua Yu and Tu Ao and Chao Huang},
  year={2024},
  eprint={2410.05779},
  archivePrefix={arXiv},
  primaryClass={cs.IR}
}
```

## 🔗 Related Projects

- [LightRAG](https://github.com/HKUDS/LightRAG): **Simple and Fast RAG**
- [VideoRAG](https://github.com/HKUDS/VideoRAG): **Extreme Long-Context Video RAG**
- [MiniRAG](https://github.com/HKUDS/MiniRAG): **Extremely Simple RAG**

## Star History

<a href="https://star-history.com/#HKUDS/RAG-Anything&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HKUDS/RAG-Anything&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HKUDS/RAG-Anything&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=HKUDS/RAG-Anything&type=Date" />
 </picture>
</a>

## Contribution

We thank all our contributors for their valuable contributions.

<a href="https://github.com/HKUDS/RAG-Anything/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/RAG-Anything" />
</a>

---

<div align="center">
    <p>
        <a href="https://github.com/HKUDS/RAG-Anything">⭐ Star us on GitHub</a> |
        <a href="https://github.com/HKUDS/RAG-Anything/issues">🐛 Report Issues</a> |
        <a href="https://github.com/HKUDS/RAG-Anything/discussions">💬 Discussions</a>
    </p>
</div>
