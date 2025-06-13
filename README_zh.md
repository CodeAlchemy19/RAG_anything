<center><h1>🚀 RAGAnything: All-in-One RAG System</h1></center>

<div align="center">
<table border="0" width="100%">
<tr>
<td width="100" align="center">
<img src="./assets/logo.png" width="80" height="80" alt="raganything">
</td>
<td>

<div>
    <p>
        <a href='https://github.com/HKUDS/RAGAnything'><img src='https://img.shields.io/badge/项目-主页-Green'></a>
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

**RAGAnything** 是一个基于 [LightRAG](https://github.com/HKUDS/LightRAG) 构建的综合性多模态文档处理RAG（检索增强生成）系统。它能够无缝处理和查询包含文本、图像、表格、公式和其他多模态内容的复杂文档。

### 核心特性

- **🔄 端到端多模态处理**：从文档解析到多模态查询回答的完整流水线
- **📄 全面的文档支持**：PDF、Office文档（DOC/DOCX/PPT/PPTX）、图像等多种格式
- **🧠 高级内容分析**：针对图像、表格、公式和通用内容的专业处理器
- **🔗 知识图谱集成**：跨模态的自动实体提取和关系构建
- **⚡ 灵活的处理选项**：基于MinerU的解析或直接多模态内容插入
- **🎯 智能检索**：跨文本和多模态内容的混合搜索

## 🏗️ 算法原理与架构

### 核心算法

RAGAnything 实现了一个**多阶段多模态处理流水线**，将传统RAG系统扩展为能够处理多样化内容类型：

#### 1. 文档解析阶段
- **MinerU集成**：利用 [MinerU](https://github.com/opendatalab/MinerU) 进行高质量文档结构提取
- **内容分解**：自动将文档分离为文本块、图像、表格、公式和其他元素
- **格式支持**：通过专业解析器处理PDF、Office文档、图像等多种格式

#### 2. 内容分离与处理
- **模态分类**：自动识别和分类不同的内容类型
- **并行处理**：通过独立流水线处理文本和多模态内容
- **质量保持**：维护内容元素之间的原始结构和关系

#### 3. 多模态分析引擎
系统为不同模态采用专业处理器：

- **ImageModalProcessor（图像模态处理器）**：
  - 视觉模型集成，进行详细图像分析
  - 上下文感知的标题生成
  - 视觉元素关系提取

- **TableModalProcessor（表格模态处理器）**：
  - 结构化数据解释
  - 统计模式识别
  - 跨表格关系识别

- **EquationModalProcessor（公式模态处理器）**：
  - 数学公式解析
  - LaTeX格式支持
  - 公式-概念关系映射

- **GenericModalProcessor（通用模态处理器）**：
  - 自定义内容类型的灵活处理
  - 新模态的可扩展框架

#### 4. 知识图谱构建
- **多模态实体创建**：每个重要的多模态元素都成为知识图谱中的实体
- **跨模态关系**：在文本实体和多模态元素之间建立连接
- **层次结构**：通过"belongs_to"关系维护文档结构
- **加权连接**：为不同关系类型分配相关性分数

#### 5. 混合检索系统
- **向量-图谱融合**：结合向量相似性搜索与图遍历
- **模态感知排序**：根据内容类型相关性调整检索分数
- **上下文保持**：维护检索元素之间的关系


## 🚀 快速开始

### 安装

#### 选项1：从PyPI安装（推荐）
```bash
pip install raganything
```

#### 选项2：从源码安装
```bash
git clone https://github.com/HKUDS/RAGAnything.git
cd RAGAnything
pip install -e .
```

#### MinerU依赖（可选）
用于文档解析功能：
```bash
pip install "magic-pdf[full]>=1.2.2" huggingface_hub
```

下载MinerU模型：
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
from lightrag.modalprocessors import ImageModalProcessor, TableModalProcessor

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

系统自动使用用户目录下的MinerU配置文件 `magic-pdf.json`。你可以自定义：
- 模型目录路径
- OCR引擎设置
- GPU加速选项
- 缓存设置

## 🧪 支持的内容类型

### 文档格式
- **PDF**：研究论文、报告、演示文稿
- **Office文档**：DOC、DOCX、PPT、PPTX
- **图像**：JPG、PNG、BMP、TIFF
- **文本文件**：TXT、MD

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

<!-- <a href="https://github.com/HKUDS/RAGAnything/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/RAGAnything" />
</a> -->

---

<div align="center">
    <p>
        <a href="https://github.com/HKUDS/RAGAnything">⭐ 在GitHub上为我们点星</a> |
        <a href="https://github.com/HKUDS/RAGAnything/issues">🐛 报告问题</a> |
        <a href="https://github.com/HKUDS/RAGAnything/discussions">💬 讨论交流</a>
    </p>
</div>
