# LM Studio Integration with RAG-Anything

This guide shows you how to integrate **LM Studio** with **RAG-Anything** for completely local multimodal document processing and querying.

## 🎯 Benefits of LM Studio + RAG-Anything

- **🔒 Fully Local**: No data leaves your machine
- **💰 Cost-Free**: No API costs after initial setup  
- **🚀 High Performance**: GPU acceleration support
- **🎛️ Full Control**: Choose your models and parameters
- **📊 Multimodal**: Process text, images, tables, equations locally

## 📋 Prerequisites

### 1. LM Studio Setup
1. Download and install [LM Studio](https://lmstudio.ai/)
2. Load a model (recommended: 7B+ parameter models for better performance)
3. Start the local server:
   - Go to "Local Server" tab in LM Studio
   - Click "Start Server"
   - Default endpoint: `http://localhost:1234/v1`

### 2. Python Dependencies
```bash
# Core dependencies
pip install openai raganything

# For local embeddings (recommended)
pip install sentence-transformers

# Optional: For advanced markdown processing
pip install raganything[markdown]
```

### 3. System Requirements
- **LibreOffice**: For Office document processing
  - macOS: `brew install --cask libreoffice`
  - Ubuntu: `sudo apt-get install libreoffice`
  - Windows: Download from [LibreOffice website](https://www.libreoffice.org/)

## 🚀 Quick Start

### 1. Environment Configuration

Copy the example environment file:
```bash
cp .env.lmstudio.example .env
```

Edit `.env` with your settings:
```env
# LM Studio Configuration
LMSTUDIO_API_HOST=http://localhost:1234/v1
LMSTUDIO_API_KEY=lm-studio

# Model Configuration (get from LM Studio)
MODEL_CHOICE=microsoft/DialoGPT-medium
VISION_MODEL_CHOICE=microsoft/DialoGPT-medium

# RAG Configuration
WORKING_DIR=./lmstudio_rag_storage
PARSER=mineru
PARSE_METHOD=auto
OUTPUT_DIR=./lmstudio_output
```

### 2. Test Your Setup

Run the quick test to verify everything works:
```bash
python test_lmstudio_integration.py
```

Expected output:
```
🧪 Quick LM Studio + RAG-Anything Integration Test
=======================================================
✅ All required packages imported successfully
✅ LM Studio connected (3 models available)
✅ LLM function works: Hello, RAG-Anything!...
✅ Embedding function works (dim: 384)
✅ RAG-Anything initialized successfully
✅ Multimodal query works: Based on the provided table...

🎉 All tests passed! Your integration is working.
```

### 3. Run Full Example

```bash
python examples/lmstudio_integration_example.py
```

## 💻 Code Examples

### Basic Integration

```python
import asyncio
from openai import OpenAI
from raganything import RAGAnything, RAGAnythingConfig
from lightrag.utils import EmbeddingFunc
from sentence_transformers import SentenceTransformer

async def main():
    # LM Studio client
    client = OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio"
    )
    
    # LLM function for RAG-Anything
    def llm_func(prompt, system_prompt=None, **kwargs):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="your-model-name",
            messages=messages,
            max_tokens=kwargs.get('max_tokens', 1000)
        )
        return response.choices[0].message.content
    
    # Local embedding function
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    embed_func = EmbeddingFunc(
        embedding_dim=384,
        max_token_size=512,
        func=lambda texts: embedding_model.encode(texts).tolist()
    )
    
    # Initialize RAG-Anything
    rag = RAGAnything(
        config=RAGAnythingConfig(working_dir="./rag_storage"),
        llm_model_func=llm_func,
        embedding_func=embed_func
    )
    
    # Process documents
    await rag.process_document_complete("document.pdf", "./output")
    
    # Query
    result = await rag.aquery("What are the main findings?", mode="hybrid")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Multimodal Query Example

```python
# Query with table data
result = await rag.aquery_with_multimodal(
    "Compare this data with the document content",
    multimodal_content=[{
        "type": "table",
        "table_data": """Method,Accuracy,Speed
LM Studio,95%,Fast
Cloud API,92%,Medium
Local CPU,88%,Slow""",
        "table_caption": "Performance Comparison"
    }],
    mode="hybrid"
)
```

### Vision Model Integration (if supported)

```python
def vision_func(prompt, image_data=None, **kwargs):
    if image_data:
        # For vision-capable models in LM Studio
        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data}"
                }}
            ]
        }]
    else:
        messages = [{"role": "user", "content": prompt}]
    
    response = client.chat.completions.create(
        model="vision-model-name",
        messages=messages
    )
    return response.choices[0].message.content

# Add to RAG initialization
rag = RAGAnything(
    config=config,
    llm_model_func=llm_func,
    vision_model_func=vision_func,  # For image analysis
    embedding_func=embed_func
)
```

## 🛠️ Troubleshooting

### Common Issues

**1. Connection Failed**
```
❌ LM Studio connection failed: Connection refused
```
**Solution**: 
- Ensure LM Studio is running
- Start the local server in LM Studio
- Check the server address (default: localhost:1234)

**2. Model Not Found**
```
❌ Chat test failed: Model 'model-name' not found
```
**Solution**: 
- Load a model in LM Studio first
- Update `MODEL_CHOICE` in `.env` with the correct model name
- Enable "just-in-time loading" in LM Studio

**3. Embedding Issues**
```
❌ Embedding function failed: sentence-transformers not available
```
**Solution**:
```bash
pip install sentence-transformers
```

**4. LibreOffice Issues**
```
❌ LibreOffice conversion failed
```
**Solution**:
- Install LibreOffice for your OS
- Verify installation: `libreoffice --version`
- Check file permissions

### Performance Optimization

**1. Model Selection**
- **7B models**: Good balance of speed/quality (Llama 2 7B, Mistral 7B)
- **13B+ models**: Better quality, slower (Llama 2 13B, CodeLlama 13B)
- **Quantized models**: Faster inference, good quality (Q4, Q5 versions)

**2. Hardware Optimization**
- **GPU**: Enable GPU acceleration in LM Studio for faster inference
- **RAM**: Ensure sufficient RAM for your model size
- **Storage**: Use SSD for faster model loading

**3. RAG Configuration**
```python
config = RAGAnythingConfig(
    max_concurrent_files=2,  # Adjust based on your CPU
    context_window=1,        # Reduce for faster processing
    max_context_tokens=1000, # Reduce for speed
)
```

## 🔧 Advanced Configuration

### Custom Context Processing

```python
config = RAGAnythingConfig(
    # Context extraction settings
    context_window=2,              # Pages before/after for context
    context_mode="page",           # or "chunk"
    max_context_tokens=2000,       # Max tokens in context
    include_headers=True,          # Include document headers
    include_captions=True,         # Include image/table captions
)
```

### Batch Processing

```python
# Process multiple documents
await rag.process_folder_complete(
    folder_path="./documents",
    output_dir="./output", 
    file_extensions=[".pdf", ".docx", ".txt"],
    recursive=True,
    max_workers=2  # Adjust based on system
)
```

### Different Query Modes

```python
# Different query strategies
local_result = await rag.aquery("question", mode="local")     # Fast, local context
global_result = await rag.aquery("question", mode="global")   # Comprehensive, slower
hybrid_result = await rag.aquery("question", mode="hybrid")   # Balanced (recommended)
naive_result = await rag.aquery("question", mode="naive")     # Simple vector search
```

## 📊 Comparison: Local vs Cloud

| Aspect | LM Studio (Local) | Cloud APIs |
|--------|------------------|------------|
| **Privacy** | 🔒 Fully local | ⚠️ Data sent to servers |
| **Cost** | 💚 Free after setup | 💰 Per-token pricing |
| **Speed** | ⚡ Fast (GPU) / 🐌 Slow (CPU) | ⚡ Generally fast |
| **Models** | 🎛️ Your choice | 🔒 Provider limited |
| **Reliability** | 🏠 Depends on your hardware | 🌐 Depends on internet |
| **Scaling** | 📊 Limited by hardware | 📈 Highly scalable |

## 🤝 Contributing

Found an issue or want to improve the integration? 

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📚 Additional Resources

- [LM Studio Documentation](https://lmstudio.ai/docs)
- [RAG-Anything GitHub](https://github.com/HKUDS/RAG-Anything)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Sentence Transformers](https://www.sbert.net/)

## 📄 License

This integration example follows the same MIT license as RAG-Anything.
