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
        <a href='https://github.com/HKUDS/RAG-Anything'><img src='https://img.shields.io/badge/项目-主页-Green'></a>
        <a href='https://arxiv.org/abs/2410.05779'><img src='https://img.shields.io/badge/arXiv-2410.05779-b31b1b'></a>
        <a href='https://github.com/HKUDS/LightRAG'><img src='https://img.shields.io/badge/基于-LightRAG-blue'></a>
    </p>
    <p>
        <img src='https://img.shields.io/github/stars/HKUDS/RAGAnything?color=green&style=social' />
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

<!-- 在此处添加架构图 -->
<!-- <img src="./assets/raganything_architecture.png" width="800" alt="RAGAnything架构图"> -->

</div>

## 🌟 项目概述

**RAG-Anything**是一个综合性多模态文档处理RAG系统。该系统能够无缝处理和查询包含文本、图像、表格、公式等多模态内容的复杂文档，提供完整的检索增强(RAG)生成解决方案。

### 核心特性

- **🔄 端到端多模态处理流水线**：提供从文档解析到多模态查询响应的完整处理链路，确保系统的一体化运行。
- **📄 多格式文档支持**：支持PDF、Office文档（DOC/DOCX/PPT/PPTX）、图像等主流文档格式的统一处理和解析。
- **🧠 多模态内容分析引擎**：针对图像、表格、公式和通用文本内容部署专门的处理器，确保各类内容的精准解析。
- **🔗 基于知识图谱索引**：实现自动化实体提取和关系构建，建立跨模态的语义连接网络。
- **⚡ 灵活的处理架构**：支持基于MinerU的智能解析模式和直接多模态内容插入模式，满足不同应用场景需求。
- **🎯 跨模态检索机制**：实现跨文本和多模态内容的智能检索，提供精准的信息定位和匹配能力。

## 🏗️ 算法原理与架构

### 核心算法

**RAGAnything** 采用灵活的分层架构设计，实现多阶段多模态处理流水线，将传统RAG系统扩展为支持异构内容类型的综合处理平台。

#### 1. 文档解析阶段
该系统构建了高精度文档解析平台，通过结构化提取引擎实现多模态元素的完整识别与提取。系统采用自适应内容分解机制，智能分离文档中的文本、图像、表格、公式等异构内容，并保持其语义关联性。同时支持PDF、Office文档、图像等主流格式的统一处理，提供标准化的多模态内容输出。

- **⚙️ 结构化提取引擎**：集成 [MinerU](https://github.com/opendatalab/MinerU) 文档解析框架，实现精确的文档结构识别与内容提取，确保多模态元素的完整性和准确性。

- **🧩 自适应内容分解机制**：建立智能内容分离系统，自动识别并提取文档中的文本块、图像、表格、公式等异构元素，保持元素间的语义关联关系。

- **📁 多格式兼容处理**：部署专业化解析器矩阵，支持PDF、Office文档系列（DOC/DOCX/PPT/PPTX）、图像等主流格式的统一处理与标准化输出。

#### 2. 多模态内容理解与处理
该多模态内容处理系统通过自主分类路由机制实现异构内容的智能识别与优化分发。系统采用并发多流水线架构，确保文本和多模态内容的高效并行处理，在最大化吞吐量的同时保持内容完整性，并能完整提取和保持原始文档的层次结构与元素关联关系。

- **🎯 自主内容分类与路由**：自动识别、分类并将不同内容类型路由至优化的执行通道。

- **⚡ 并发多流水线架构**：通过专用处理流水线实现文本和多模态内容的并发执行。这种方法在保持内容完整性的同时最大化吞吐效率。

- **🏗️ 文档层次结构提取**：在内容转换过程中提取并保持原始文档的层次结构和元素间关系。

#### 3. 多模态分析引擎
系统部署了面向异构数据模态的模态感知处理单元：

- **🔍 Visual Content Analyzer（视觉内容分析器）**：
  - 集成视觉模型进行图像分析和内容识别
  - 基于视觉语义生成上下文感知的描述性标题
  - 提取视觉元素间的空间关系和层次结构

- **📊 Structured Data Interpreter（结构化数据解释器）**：
  - 对表格和结构化数据格式进行系统性解释
  - 实现数据趋势分析的统计模式识别算法
  - 识别多个表格数据集间的语义关系和依赖性

- **📐 Mathematical Expression Parser（数学表达式解析器）**：
  - 高精度解析复杂数学表达式和公式
  - 提供原生LaTeX格式支持以实现与学术工作流的无缝集成
  - 建立数学方程与领域特定知识库间的概念映射

- **🔧 Extensible Modality Handler（可扩展模态处理器）**：
  - 为自定义和新兴内容类型提供可配置的处理框架
  - 通过插件架构实现新模态处理器的动态集成
  - 支持专用场景下处理流水线的运行时配置

#### 4. 多模态知识图谱索引
多模态知识图谱构建模块将文档内容转换为结构化语义表示。系统提取多模态实体，建立跨模态关系，并保持层次化组织结构。通过加权相关性评分实现优化的知识检索。

- **🔍 多模态实体提取**：将重要的多模态元素转换为结构化知识图谱实体。该过程包括语义标注和元数据保存。

- **🔗 跨模态关系映射**：在文本实体和多模态组件之间建立语义连接和依赖关系。通过自动化关系推理算法实现这一功能。

- **🏗️ 层次结构保持**：通过"归属于"关系链维护原始文档组织结构。这些关系链保持逻辑内容层次和章节依赖关系。

- **⚖️ 加权关系评分**：为关系类型分配定量相关性分数。评分基于语义邻近性和文档结构内的上下文重要性。

#### 5. 模态感知检索
混合检索系统结合向量相似性搜索与图遍历算法，实现全面的内容检索。系统实现模态感知排序机制，并维护检索元素间的关系一致性，确保上下文集成的信息传递。

- **🔀 向量-图谱融合**：集成向量相似性搜索与图遍历算法。该方法同时利用语义嵌入和结构关系实现全面的内容检索。

- **📊 模态感知排序**：实现基于内容类型相关性的自适应评分机制。系统根据查询特定的模态偏好调整排序结果。

- **🔗 关系一致性维护**：维护检索元素间的语义和结构关系。确保信息传递的连贯性和上下文完整性。


## 🚀 快速开始

### 安装

#### 选项1：从PyPI安装（推荐）
```bash
pip install raganything
```

#### 选项2：从源码安装
```bash
git clone https://github.com/HKUDS/RAG-Anything.git
cd RAGAnything
pip install -e .
```

#### MinerU依赖（可选）
用于MinerU 2.0文档解析功能：
```bash
# 安装MinerU 2.0
pip install -U 'mineru[core]'

# 或使用uv（更快）
uv pip install -U 'mineru[core]'
```

> **⚠️ MinerU 2.0重要变化：**
> - 包名从 `magic-pdf` 改为 `mineru`
> - 移除了LibreOffice集成（Office文档需要手动转换为PDF）
> - 简化的命令行界面，使用 `mineru` 命令
> - 新的后端选项和性能改进

检查MinerU安装：
```bash
# 验证安装
mineru --version

# 检查是否正确配置
python -c "from raganything import RAGAnything; rag = RAGAnything(); print('✅ MinerU安装正常' if rag.check_mineru_installation() else '❌ MinerU安装有问题')"
```

模型在首次使用时自动下载。手动下载（如果需要）：
```bash
# 选项1：Hugging Face
wget https://github.com/opendatalab/MinerU/raw/master/scripts/download_models_hf.py
python download_models_hf.py

# 选项2：ModelScope（适用于中国用户）
wget https://github.com/opendatalab/MinerU/raw/master/scripts/download_models.py
python download_models.py
```

### 使用方法

#### 端到端文档处理

```python
import asyncio
from raganything import RAGAnything
from lightrag.llm.openai import openai_complete_if_cache, openai_embed

async def main():
    # 初始化RAGAnything
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

    # 处理文档
    await rag.process_document_complete(
        file_path="path/to/your/document.pdf",
        output_dir="./output",
        parse_method="auto"
    )

    # 查询处理后的内容
    result = await rag.query_with_multimodal(
        "图表中显示的主要发现是什么？",
        mode="hybrid"
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

#### 直接多模态内容处理

```python
import asyncio
from lightrag import LightRAG
from raganything.modalprocessors import ImageModalProcessor, TableModalProcessor

async def process_multimodal_content():
    # 初始化LightRAG
    rag = LightRAG(
        working_dir="./rag_storage",
        # ... 你的LLM和嵌入配置
    )
    await rag.initialize_storages()

    # 处理图像
    image_processor = ImageModalProcessor(
        lightrag=rag,
        modal_caption_func=your_vision_model_func
    )

    image_content = {
        "img_path": "path/to/image.jpg",
        "img_caption": ["图1：实验结果"],
        "img_footnote": ["数据收集于2024年"]
    }

    description, entity_info = await image_processor.process_multimodal_content(
        modal_content=image_content,
        content_type="image",
        file_path="research_paper.pdf",
        entity_name="实验结果图表"
    )

    # 处理表格
    table_processor = TableModalProcessor(
        lightrag=rag,
        modal_caption_func=your_llm_model_func
    )

    table_content = {
        "table_body": """
        | 方法 | 准确率 | F1分数 |
        |------|--------|--------|
        | RAGAnything | 95.2% | 0.94 |
        | 基准方法 | 87.3% | 0.85 |
        """,
        "table_caption": ["性能对比"],
        "table_footnote": ["测试数据集结果"]
    }

    description, entity_info = await table_processor.process_multimodal_content(
        modal_content=table_content,
        content_type="table",
        file_path="research_paper.pdf",
        entity_name="性能结果表格"
    )

if __name__ == "__main__":
    asyncio.run(process_multimodal_content())
```

### 批量处理

```python
# 处理多个文档
await rag.process_folder_complete(
    folder_path="./documents",
    output_dir="./output",
    file_extensions=[".pdf", ".docx", ".pptx"],
    recursive=True,
    max_workers=4
)
```

### 自定义模态处理器

```python
from raganything.modalprocessors import GenericModalProcessor

class CustomModalProcessor(GenericModalProcessor):
    async def process_multimodal_content(self, modal_content, content_type, file_path, entity_name):
        # 你的自定义处理逻辑
        enhanced_description = await self.analyze_custom_content(modal_content)
        entity_info = self.create_custom_entity(enhanced_description, entity_name)
        return await self._create_entity_and_chunk(enhanced_description, entity_info, file_path)
```

### 查询选项

```python
# 不同的查询模式
result_hybrid = await rag.query_with_multimodal("你的问题", mode="hybrid")
result_local = await rag.query_with_multimodal("你的问题", mode="local")
result_global = await rag.query_with_multimodal("你的问题", mode="global")
```

## 🛠️ 示例

`examples/` 目录包含完整的使用示例：

- **`raganything_example.py`**：基于MinerU的端到端文档处理
- **`modalprocessors_example.py`**：直接多模态内容处理

运行示例：
```bash
# 端到端处理
python examples/raganything_example.py path/to/document.pdf --api-key YOUR_API_KEY

# 直接模态处理
python examples/modalprocessors_example.py --api-key YOUR_API_KEY
```

## 🔧 配置

### 环境变量

创建 `.env` 文件（参考 `.env.example`）：
```bash
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=your_base_url  # 可选
```

### MinerU配置

MinerU 2.0使用简化的配置方式：

```bash
# MinerU 2.0使用命令行参数而不是配置文件
# 查看可用选项：
mineru --help

# 常用配置：
mineru -p input.pdf -o output_dir -m auto    # 自动解析模式
mineru -p input.pdf -o output_dir -m ocr     # OCR重点解析
mineru -p input.pdf -o output_dir -b pipeline --device cuda  # GPU加速
```

你也可以通过RAGAnything参数配置MinerU：
```python
# 配置解析行为
await rag.process_document_complete(
    file_path="document.pdf",
    parse_method="auto",     # 或 "ocr", "txt"
    device="cuda",           # GPU加速
    backend="pipeline",      # 解析后端
    lang="ch"               # 语言优化
)
```

> **注意**：MinerU 2.0不再使用 `magic-pdf.json` 配置文件。所有设置现在通过命令行参数或函数参数传递。

## 🧪 支持的内容类型

### 文档格式
- **PDF**：研究论文、报告、演示文稿
- **Office文档**：DOC、DOCX、PPT、PPTX ⚠️
- **图像**：JPG、PNG、BMP、TIFF
- **文本文件**：TXT、MD

> **⚠️ MinerU 2.0中的Office文档处理：**
>
> 由于MinerU 2.0的架构变化，Office文档需要额外设置：
> - **自动转换**：需要安装LibreOffice进行PDF转换
> - **手动转换**：预先转换为PDF以获得最佳性能
> - **推荐方式**：尽可能使用PDF格式以获得最佳效果

### 多模态元素
- **图像**：照片、图表、示意图、截图
- **表格**：数据表、对比图、统计摘要
- **公式**：LaTeX格式的数学公式
- **通用内容**：通过可扩展处理器支持的自定义内容类型

## 📖 引用

如果你在研究中发现RAGAnything有用，请引用我们的论文：

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

## 🔗 相关项目

- [LightRAG](https://github.com/HKUDS/LightRAG)：基础RAG系统
- [VideoRAG](https://github.com/HKUDS/VideoRAG)：视频理解RAG系统
- [MiniRAG](https://github.com/HKUDS/MiniRAG)：基于小模型的轻量级RAG

## Star History

<!-- <a href="https://star-history.com/#HKUDS/RAGAnything&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HKUDS/RAGAnything&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HKUDS/RAGAnything&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=HKUDS/RAGAnything&type=Date" />
 </picture>
</a> -->

## 贡献者

感谢所有贡献者！

<!-- <a href="https://github.com/HKUDS/RAG-Anything/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/RAGAnything" />
</a> -->

---

<div align="center">
    <p>
        <a href="https://github.com/HKUDS/RAG-Anything">⭐ 在GitHub上为我们点星</a> |
        <a href="https://github.com/HKUDS/RAG-Anything/issues">🐛 报告问题</a> |
        <a href="https://github.com/HKUDS/RAG-Anything/discussions">💬 讨论交流</a>
    </p>
</div>
