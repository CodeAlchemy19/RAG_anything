<div align="center">

<div style="margin: 20px 0;">
  <img src="./assets/logo.png" width="120" height="120" alt="RAG-Anything Logo" style="border-radius: 20px; box-shadow: 0 8px 32px rgba(0, 217, 255, 0.3);">
</div>

# 🚀 RAG-Anything: All-in-One RAG System

<div align="center">
  <div style="width: 100%; height: 2px; margin: 20px 0; background: linear-gradient(90deg, transparent, #00d9ff, transparent);"></div>
</div>

<div align="center">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; padding: 25px; text-align: center;">
    <p>
      <a href='https://github.com/HKUDS/RAG-Anything'><img src='https://img.shields.io/badge/🔥项目-主页-00d9ff?style=for-the-badge&logo=github&logoColor=white&labelColor=1a1a2e'></a>
      <a href='https://arxiv.org/abs/2410.05779'><img src='https://img.shields.io/badge/📄arXiv-2410.05779-ff6b6b?style=for-the-badge&logo=arxiv&logoColor=white&labelColor=1a1a2e'></a>
      <a href='https://github.com/HKUDS/LightRAG'><img src='https://img.shields.io/badge/⚡基于-LightRAG-4ecdc4?style=for-the-badge&logo=lightning&logoColor=white&labelColor=1a1a2e'></a>
    </p>
    <p>
      <a href="https://github.com/HKUDS/RAG-Anything/stargazers"><img src='https://img.shields.io/github/stars/HKUDS/RAG-Anything?color=00d9ff&style=for-the-badge&logo=star&logoColor=white&labelColor=1a1a2e' /></a>
      <img src="https://img.shields.io/badge/🐍Python-3.9+-4ecdc4?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e">
      <a href="https://pypi.org/project/raganything/"><img src="https://img.shields.io/pypi/v/raganything.svg?style=for-the-badge&logo=pypi&logoColor=white&labelColor=1a1a2e&color=ff6b6b"></a>
    </p>
    <p>
      <a href="https://discord.gg/yF2MmDJyGJ"><img src="https://img.shields.io/badge/💬Discord-社区-7289da?style=for-the-badge&logo=discord&logoColor=white&labelColor=1a1a2e"></a>
      <a href="https://github.com/HKUDS/RAG-Anything/issues/7"><img src="https://img.shields.io/badge/💬微信群-交流-07c160?style=for-the-badge&logo=wechat&logoColor=white&labelColor=1a1a2e"></a>
    </p>
    <p>
      <a href="README_zh.md"><img src="https://img.shields.io/badge/🇨🇳中文版-1a1a2e?style=for-the-badge"></a>
      <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸English-1a1a2e?style=for-the-badge"></a>
    </p>
  </div>
</div>

</div>

<div align="center" style="margin: 30px 0;">
  <img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="800">
</div>

<div align="center">
  <a href="#-快速开始" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/快速开始-立即开始使用-00d9ff?style=for-the-badge&logo=rocket&logoColor=white&labelColor=1a1a2e">
  </a>
</div>

---

## 🌟 系统概述

*下一代多模态智能*

<div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); border-radius: 15px; padding: 25px; margin: 20px 0; border: 2px solid #00d9ff; box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);">

**RAG-Anything**是一个综合性多模态文档处理RAG系统。该系统能够无缝处理和查询包含文本、图像、表格、公式等多模态内容的复杂文档，提供完整的检索增强(RAG)生成解决方案。

<img src="assets/rag_anything_framework.png" alt="RAG-Anything" />

</div>

### 🎯 核心特性

<div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; padding: 25px; margin: 20px 0;">

- **🔄 端到端多模态处理流水线** - 提供从文档解析到多模态查询响应的完整处理链路，确保系统的一体化运行
- **📄 多格式文档支持** - 支持PDF、Office文档（DOC/DOCX/PPT/PPTX/XLS/XLSX）、图像等主流文档格式的统一处理和解析
- **🧠 多模态内容分析引擎** - 针对图像、表格、公式和通用文本内容部署专门的处理器，确保各类内容的精准解析
- **🔗 基于知识图谱索引** - 实现自动化实体提取和关系构建，建立跨模态的语义连接网络
- **⚡ 灵活的处理架构** - 支持基于MinerU的智能解析模式和直接多模态内容插入模式，满足不同应用场景需求
- **🎯 跨模态检索机制** - 实现跨文本和多模态内容的智能检索，提供精准的信息定位和匹配能力

</div>

---

## 🏗️ 算法原理与架构

<div style="background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%); border-radius: 15px; padding: 25px; margin: 20px 0; border-left: 5px solid #00d9ff;">

### 核心算法

**RAG-Anything** 采用灵活的分层架构设计，实现多阶段多模态处理流水线，将传统RAG系统扩展为支持异构内容类型的综合处理平台。

</div>

<div align="center">
  <div style="width: 100%; max-width: 600px; margin: 20px auto; padding: 20px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%); border-radius: 15px; border: 1px solid rgba(0, 217, 255, 0.2);">
    <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px;">
      <div style="text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">📄</div>
        <div style="font-size: 14px; color: #00d9ff;">文档解析</div>
      </div>
      <div style="font-size: 20px; color: #00d9ff;">→</div>
      <div style="text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">🧠</div>
        <div style="font-size: 14px; color: #00d9ff;">内容分析</div>
      </div>
      <div style="font-size: 20px; color: #00d9ff;">→</div>
      <div style="text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">🔍</div>
        <div style="font-size: 14px; color: #00d9ff;">知识图谱</div>
      </div>
      <div style="font-size: 20px; color: #00d9ff;">→</div>
      <div style="text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">🎯</div>
        <div style="font-size: 14px; color: #00d9ff;">智能检索</div>
      </div>
    </div>
  </div>
</div>

### 1. 文档解析阶段

<div style="background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%); border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #4ecdc4;">

该系统构建了高精度文档解析平台，通过结构化提取引擎实现多模态元素的完整识别与提取。系统采用自适应内容分解机制，智能分离文档中的文本、图像、表格、公式等异构内容，并保持其语义关联性。同时支持PDF、Office文档、图像等主流格式的统一处理，提供标准化的多模态内容输出。

**核心组件：**

- **⚙️ 结构化提取引擎**：集成 [MinerU](https://github.com/opendatalab/MinerU) 文档解析框架，实现精确的文档结构识别与内容提取，确保多模态元素的完整性和准确性。

- **🧩 自适应内容分解机制**：建立智能内容分离系统，自动识别并提取文档中的文本块、图像、表格、公式等异构元素，保持元素间的语义关联关系。

- **📁 多格式兼容处理**：部署专业化解析器矩阵，支持PDF、Office文档系列（DOC/DOCX/PPT/PPTX/XLS/XLSX）、图像等主流格式的统一处理与标准化输出。

</div>

### 2. 多模态内容理解与处理

<div style="background: linear-gradient(90deg, #16213e 0%, #0f3460 100%); border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #ff6b6b;">

该多模态内容处理系统通过自主分类路由机制实现异构内容的智能识别与优化分发。系统采用并发多流水线架构，确保文本和多模态内容的高效并行处理，在最大化吞吐量的同时保持内容完整性，并能完整提取和保持原始文档的层次结构与元素关联关系。

**核心组件：**

- **🎯 自主内容分类与路由**：自动识别、分类并将不同内容类型路由至优化的执行通道。

- **⚡ 并发多流水线架构**：通过专用处理流水线实现文本和多模态内容的并发执行。这种方法在保持内容完整性的同时最大化吞吐效率。

- **🏗️ 文档层次结构提取**：在内容转换过程中提取并保持原始文档的层次结构和元素间关系。

</div>

### 3. 多模态分析引擎

<div style="background: linear-gradient(90deg, #0f3460 0%, #1a1a2e 100%); border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #00d9ff;">

系统部署了面向异构数据模态的模态感知处理单元：

**专用分析器：**

- **🔍 视觉内容分析器**：
  - 集成视觉模型进行图像分析和内容识别
  - 基于视觉语义生成上下文感知的描述性标题
  - 提取视觉元素间的空间关系和层次结构

- **📊 结构化数据解释器**：
  - 对表格和结构化数据格式进行系统性解释
  - 实现数据趋势分析的统计模式识别算法
  - 识别多个表格数据集间的语义关系和依赖性

- **📐 数学表达式解析器**：
  - 高精度解析复杂数学表达式和公式
  - 提供原生LaTeX格式支持以实现与学术工作流的无缝集成
  - 建立数学方程与领域特定知识库间的概念映射

- **🔧 可扩展模态处理器**：
  - 为自定义和新兴内容类型提供可配置的处理框架
  - 通过插件架构实现新模态处理器的动态集成
  - 支持专用场景下处理流水线的运行时配置

</div>

### 4. 多模态知识图谱索引

<div style="background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%); border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #4ecdc4;">

多模态知识图谱构建模块将文档内容转换为结构化语义表示。系统提取多模态实体，建立跨模态关系，并保持层次化组织结构。通过加权相关性评分实现优化的知识检索。

**核心功能：**

- **🔍 多模态实体提取**：将重要的多模态元素转换为结构化知识图谱实体。该过程包括语义标注和元数据保存。

- **🔗 跨模态关系映射**：在文本实体和多模态组件之间建立语义连接和依赖关系。通过自动化关系推理算法实现这一功能。

- **🏗️ 层次结构保持**：通过"归属于"关系链维护原始文档组织结构。这些关系链保持逻辑内容层次和章节依赖关系。

- **⚖️ 加权关系评分**：为关系类型分配定量相关性分数。评分基于语义邻近性和文档结构内的上下文重要性。

</div>

### 5. 模态感知检索

<div style="background: linear-gradient(90deg, #16213e 0%, #0f3460 100%); border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #ff6b6b;">

混合检索系统结合向量相似性搜索与图遍历算法，实现全面的内容检索。系统实现模态感知排序机制，并维护检索元素间的关系一致性，确保上下文集成的信息传递。

**检索机制：**

- **🔀 向量-图谱融合**：集成向量相似性搜索与图遍历算法。该方法同时利用语义嵌入和结构关系实现全面的内容检索。

- **📊 模态感知排序**：实现基于内容类型相关性的自适应评分机制。系统根据查询特定的模态偏好调整排序结果。

- **🔗 关系一致性维护**：维护检索元素间的语义和结构关系。确保信息传递的连贯性和上下文完整性。

</div>

---

## 🚀 快速开始

*启动您的AI之旅*

<div align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="400">
</div>

### 安装

#### 选项1：从PyPI安装（推荐）

```bash
# 基础安装
pip install raganything

# 安装包含扩展格式支持的可选依赖：
pip install 'raganything[all]'              # 所有可选功能
pip install 'raganything[image]'            # 图像格式转换 (BMP, TIFF, GIF, WebP)
pip install 'raganything[text]'             # 文本文件处理 (TXT, MD)
pip install 'raganything[image,text]'       # 多个功能组合
```

#### 选项2：从源码安装

```bash
git clone https://github.com/HKUDS/RAG-Anything.git
cd RAG-Anything
pip install -e .

# 安装可选依赖
pip install -e '.[all]'
```

#### 可选依赖

- **`[image]`** - 启用BMP、TIFF、GIF、WebP图像格式处理（需要Pillow）
- **`[text]`** - 启用TXT和MD文件处理（需要ReportLab）
- **`[all]`** - 包含所有Python可选依赖

> **⚠️ Office文档处理配置要求：**
> - Office文档 (.doc, .docx, .ppt, .pptx, .xls, .xlsx) 需要安装 **LibreOffice**
> - 从[LibreOffice官网](https://www.libreoffice.org/download/download/)下载安装
> - **Windows**：从官网下载安装包
> - **macOS**：`brew install --cask libreoffice`
> - **Ubuntu/Debian**：`sudo apt-get install libreoffice`
> - **CentOS/RHEL**：`sudo yum install libreoffice`

**检查MinerU安装：**

```bash
# 验证安装
mineru --version

# 检查是否正确配置
python -c "from raganything import RAGAnything; rag = RAGAnything(); print('✅ MinerU安装正常' if rag.check_mineru_installation() else '❌ MinerU安装有问题')"
```

模型在首次使用时自动下载。手动下载参考[MinerU模型源配置](https://github.com/opendatalab/MinerU/blob/master/README_zh-CN.md#22-%E6%A8%A1%E5%9E%8B%E6%BA%90%E9%85%8D%E7%BD%AE)：

### 使用示例

#### 1. 端到端文档处理

```python
import asyncio
from raganything import RAGAnything
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.utils import EmbeddingFunc

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
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
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
        embedding_func=EmbeddingFunc(
            embedding_dim=3072,
            max_token_size=8192,
            func=lambda texts: openai_embed(
                texts,
                model="text-embedding-3-large",
                api_key=api_key,
                base_url=base_url,
            ),
        ),
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

#### 2. 直接多模态内容处理

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

#### 3. 批量处理

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

#### 4. 自定义模态处理器

```python
from raganything.modalprocessors import GenericModalProcessor

class CustomModalProcessor(GenericModalProcessor):
    async def process_multimodal_content(self, modal_content, content_type, file_path, entity_name):
        # 你的自定义处理逻辑
        enhanced_description = await self.analyze_custom_content(modal_content)
        entity_info = self.create_custom_entity(enhanced_description, entity_name)
        return await self._create_entity_and_chunk(enhanced_description, entity_info, file_path)
```

#### 5. 查询选项

```python
# 不同的查询模式
result_hybrid = await rag.query_with_multimodal("你的问题", mode="hybrid")
result_local = await rag.query_with_multimodal("你的问题", mode="local")
result_global = await rag.query_with_multimodal("你的问题", mode="global")
```

#### 6. 加载已存在的LightRAG实例

```python
import asyncio
from raganything import RAGAnything
from lightrag import LightRAG
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.utils import EmbeddingFunc
import os

async def load_existing_lightrag():
    # 首先，创建或加载已存在的LightRAG实例
    lightrag_working_dir = "./existing_lightrag_storage"

    # 检查是否存在之前的LightRAG实例
    if os.path.exists(lightrag_working_dir) and os.listdir(lightrag_working_dir):
        print("✅ 发现已存在的LightRAG实例，正在加载...")
    else:
        print("❌ 未找到已存在的LightRAG实例，将创建新实例")

    # 使用您的配置创建/加载LightRAG实例
    lightrag_instance = LightRAG(
        working_dir=lightrag_working_dir,
        llm_model_func=lambda prompt, system_prompt=None, history_messages=[], **kwargs: openai_complete_if_cache(
            "gpt-4o-mini",
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key="your-api-key",
            **kwargs,
        ),
        embedding_func=EmbeddingFunc(
            embedding_dim=3072,
            max_token_size=8192,
            func=lambda texts: openai_embed(
                texts,
                model="text-embedding-3-large",
                api_key=api_key,
                base_url=base_url,
            ),
        )
    )

    # 初始化存储（如果有现有数据，这将加载它们）
    await lightrag_instance.initialize_storages()

    # 现在使用已存在的LightRAG实例初始化RAGAnything
    rag = RAGAnything(
        lightrag=lightrag_instance,  # 传入已存在的LightRAG实例
        # 只需要为多模态处理配置vision model
        vision_model_func=lambda prompt, system_prompt=None, history_messages=[], image_data=None, **kwargs: openai_complete_if_cache(
            "gpt-4o",
            "",
            system_prompt=None,
            history_messages=[],
            messages=[
                {"role": "system", "content": system_prompt} if system_prompt else None,
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
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
        )
        # 注意：working_dir、llm_model_func、embedding_func等都从lightrag_instance继承
    )

    # 查询已存在的知识库
    result = await rag.query_with_multimodal(
        "这个LightRAG实例中处理了哪些数据？",
        mode="hybrid"
    )
    print("查询结果:", result)

    # 向已存在的LightRAG实例添加新的多模态文档
    await rag.process_document_complete(
        file_path="path/to/new/multimodal_document.pdf",
        output_dir="./output"
    )

if __name__ == "__main__":
    asyncio.run(load_existing_lightrag())
```

---

## 🛠️ 示例

*实际应用演示*

<div align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212257455-13e3e01e-d6a6-45dc-bb92-3ab87b12dfc1.gif" width="300">
</div>

`examples/` 目录包含完整的使用示例：

- **`raganything_example.py`**：基于MinerU的端到端文档处理
- **`modalprocessors_example.py`**：直接多模态内容处理
- **`office_document_test.py`**：Office文档解析测试（无需API密钥）
- **`image_format_test.py`**：图像格式解析测试（无需API密钥）
- **`text_format_test.py`**：文本格式解析测试（无需API密钥）

**运行示例：**

```bash
# 端到端处理
python examples/raganything_example.py path/to/document.pdf --api-key YOUR_API_KEY

# 直接模态处理
python examples/modalprocessors_example.py --api-key YOUR_API_KEY

# Office文档解析测试（仅MinerU功能）
python examples/office_document_test.py --file path/to/document.docx

# 图像格式解析测试（仅MinerU功能）
python examples/image_format_test.py --file path/to/image.bmp

# 文本格式解析测试（仅MinerU功能）
python examples/text_format_test.py --file path/to/document.md

# 检查LibreOffice安装
python examples/office_document_test.py --check-libreoffice --file dummy

# 检查PIL/Pillow安装
python examples/image_format_test.py --check-pillow --file dummy

# 检查ReportLab安装
python examples/text_format_test.py --check-reportlab --file dummy
```

> **注意**：API密钥仅在完整RAG处理和LLM集成时需要。解析测试文件（`office_document_test.py`、`image_format_test.py` 和 `text_format_test.py`）仅测试MinerU功能，无需API密钥。

---

## 🔧 配置

*系统优化参数*

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

### 处理要求

不同内容类型需要特定的可选依赖：

- **Office文档** (.doc, .docx, .ppt, .pptx, .xls, .xlsx): 安装并配置 [LibreOffice](https://www.libreoffice.org/download/download/)
- **扩展图像格式** (.bmp, .tiff, .gif, .webp): 使用 `pip install raganything[image]` 安装
- **文本文件** (.txt, .md): 使用 `pip install raganything[text]` 安装

> **📋 快速安装**: 使用 `pip install raganything[all]` 启用所有格式支持（仅Python依赖 - LibreOffice仍需单独安装）

---

## 🧪 支持的内容类型

### 文档格式

- **PDF** - 研究论文、报告、演示文稿
- **Office文档** - DOC、DOCX、PPT、PPTX、XLS、XLSX
- **图像** - JPG、PNG、BMP、TIFF、GIF、WebP
- **文本文件** - TXT、MD

### 多模态元素

- **图像** - 照片、图表、示意图、截图
- **表格** - 数据表、对比图、统计摘要
- **公式** - LaTeX格式的数学公式
- **通用内容** - 通过可扩展处理器支持的自定义内容类型

*格式特定依赖的安装说明请参见[配置](#-配置)部分。*

---

## 📖 引用

*学术参考*

<div align="center">
  <div style="width: 60px; height: 60px; margin: 20px auto; position: relative;">
    <div style="width: 100%; height: 100%; border: 2px solid #00d9ff; border-radius: 50%; position: relative;">
      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 24px; color: #00d9ff;">📖</div>
    </div>
    <div style="position: absolute; bottom: -5px; left: 50%; transform: translateX(-50%); width: 20px; height: 20px; background: white; border-right: 2px solid #00d9ff; border-bottom: 2px solid #00d9ff; transform: rotate(45deg);"></div>
  </div>
</div>

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

---

## 🔗 相关项目

*生态系统与扩展*

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/HKUDS/LightRAG">
          <div style="width: 100px; height: 100px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%); border-radius: 15px; border: 1px solid rgba(0, 217, 255, 0.2); display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <span style="font-size: 32px;">⚡</span>
          </div>
          <b>LightRAG</b><br>
          <sub>简单快速的RAG系统</sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/HKUDS/VideoRAG">
          <div style="width: 100px; height: 100px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%); border-radius: 15px; border: 1px solid rgba(0, 217, 255, 0.2); display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <span style="font-size: 32px;">🎥</span>
          </div>
          <b>VideoRAG</b><br>
          <sub>超长上下文视频RAG系统</sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/HKUDS/MiniRAG">
          <div style="width: 100px; height: 100px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%); border-radius: 15px; border: 1px solid rgba(0, 217, 255, 0.2); display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <span style="font-size: 32px;">✨</span>
          </div>
          <b>MiniRAG</b><br>
          <sub>极简RAG系统</sub>
        </a>
      </td>
    </tr>
  </table>
</div>

---

## ⭐ Star History

*社区增长轨迹*

<div align="center">
  <a href="https://star-history.com/#HKUDS/RAG-Anything&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HKUDS/RAG-Anything&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HKUDS/RAG-Anything&type=Date" />
      <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=HKUDS/RAG-Anything&type=Date" style="border-radius: 15px; box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);" />
    </picture>
  </a>
</div>

---

## 🤝 贡献者

*加入创新*

<div align="center">
  感谢所有贡献者！
</div>

<div align="center">
  <a href="https://github.com/HKUDS/RAG-Anything/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=HKUDS/RAG-Anything" style="border-radius: 15px; box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);" />
  </a>
</div>

---

<div align="center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; padding: 30px; margin: 30px 0;">
  <div>
    <img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="500">
  </div>
  <div style="margin-top: 20px;">
    <a href="https://github.com/HKUDS/RAG-Anything" style="text-decoration: none;">
      <img src="https://img.shields.io/badge/⭐%20在GitHub上为我们点星-1a1a2e?style=for-the-badge&logo=github&logoColor=white">
    </a>
    <a href="https://github.com/HKUDS/RAG-Anything/issues" style="text-decoration: none;">
      <img src="https://img.shields.io/badge/🐛%20报告问题-ff6b6b?style=for-the-badge&logo=github&logoColor=white">
    </a>
    <a href="https://github.com/HKUDS/RAG-Anything/discussions" style="text-decoration: none;">
      <img src="https://img.shields.io/badge/💬%20讨论交流-4ecdc4?style=for-the-badge&logo=github&logoColor=white">
    </a>
  </div>
</div>

<div align="center">
  <div style="width: 100%; max-width: 600px; margin: 20px auto; padding: 20px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%); border-radius: 15px; border: 1px solid rgba(0, 217, 255, 0.2);">
    <div style="display: flex; justify-content: center; align-items: center; gap: 15px;">
      <span style="font-size: 24px;">⭐</span>
      <span style="color: #00d9ff; font-size: 18px;">感谢您访问RAG-Anything!</span>
      <span style="font-size: 24px;">⭐</span>
    </div>
    <div style="margin-top: 10px; color: #00d9ff; font-size: 16px;">构建多模态AI的未来</div>
  </div>
</div>

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=20&duration=3000&pause=1000&color=00D9FF&center=true&vCenter=true&width=600&lines=感谢您访问RAG-Anything!;构建多模态AI的未来;如果觉得有用请点星⭐!" alt="Closing Animation" />
</div>

<style>
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@keyframes glow {
  0% { box-shadow: 0 0 5px rgba(0, 217, 255, 0.5); }
  50% { box-shadow: 0 0 20px rgba(0, 217, 255, 0.8); }
  100% { box-shadow: 0 0 5px rgba(0, 217, 255, 0.5); }
}
</style>
