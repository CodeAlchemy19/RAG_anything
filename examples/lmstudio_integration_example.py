"""
LMStudio Integration Example with RAG-Anything

This example demonstrates how to integrate LMStudio with RAG-Anything for local
multimodal document processing and querying.

Requirements:
- LMStudio running locally with server enabled
- OpenAI Python package: pip install openai
- RAG-Anything installed: pip install raganything

Environment Setup:
Create a .env file with:
LMSTUDIO_API_HOST=http://localhost:1234/v1
LMSTUDIO_API_KEY=lm-studio
MODEL_CHOICE=your-model-name
VISION_MODEL_CHOICE=your-vision-model-name  # Optional for vision tasks
EMBEDDING_MODEL_CHOICE=text-embedding-nomic-embed-text-v1.5  # Default LMStudio embedding model
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables
load_dotenv()

# RAG-Anything imports
from raganything import RAGAnything, RAGAnythingConfig
from lightrag.utils import EmbeddingFunc
from lightrag.llm.openai import openai_complete_if_cache

class LMStudioRAGIntegration:
    """Integration class for LMStudio with RAG-Anything."""
    
    def __init__(self):
        # LMStudio configuration
        self.base_url = os.getenv('LMSTUDIO_API_HOST', 'http://localhost:1234/v1')
        self.api_key = os.getenv('LMSTUDIO_API_KEY', 'lm-studio')
        self.model_name = os.getenv('MODEL_CHOICE', 'openai/gpt-oss-20b')
        self.vision_model = os.getenv('VISION_MODEL_CHOICE', self.model_name)
        self.embedding_model = os.getenv('EMBEDDING_MODEL_CHOICE', 'text-embedding-nomic-embed-text-v1.5')
        
        # Initialize AsyncOpenAI client for LightRAG compatibility
        self.client = AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        
        # RAG-Anything configuration
        self.config = RAGAnythingConfig(
            working_dir="./lmstudio_rag_storage",
            parser="mineru",
            parse_method="auto",
            enable_image_processing=True,
            enable_table_processing=True,
            enable_equation_processing=True,
        )
        
        self.rag = None
    
    async def test_connection(self) -> bool:
        """Test LMStudio connection."""
        try:
            print(f"🔌 Testing LMStudio connection at: {self.base_url}")
            models = await self.client.models.list()
            print(f"✅ Connected successfully! Found {len(models.data)} models")
            
            # Show available models
            print("📊 Available models:")
            for i, model in enumerate(models.data[:5]):
                marker = "🎯" if model.id == self.model_name else "  "
                print(f"{marker} {i+1}. {model.id}")
            
            if len(models.data) > 5:
                print(f"  ... and {len(models.data) - 5} more models")
            
            return True
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            print("\n💡 Troubleshooting tips:")
            print("1. Ensure LMStudio is running")
            print("2. Start the local server in LMStudio")
            print("3. Load a model or enable just-in-time loading")
            print(f"4. Verify server address: {self.base_url}")
            return False
    
    async def test_chat_completion(self) -> bool:
        """Test basic chat functionality."""
        try:
            print(f"💬 Testing chat with model: {self.model_name}")
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": "Hello! Please confirm you're working and tell me your capabilities."}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            result = response.choices[0].message.content.strip()
            print(f"✅ Chat test successful!")
            print(f"Response: {result}")
            return True
        except Exception as e:
            print(f"❌ Chat test failed: {str(e)}")
            return False
    
    async def llm_model_func(self, prompt: str, system_prompt: Optional[str] = None, 
                            history_messages: List[Dict] = None, **kwargs) -> str:
        """LLM function compatible with LightRAG via openai_complete_if_cache."""
        try:
            # Use LightRAG's built-in function for better compatibility
            return await openai_complete_if_cache(
                model=self.model_name,
                prompt=prompt,
                system_prompt=system_prompt,
                history_messages=history_messages or [],
                base_url=self.base_url,
                api_key=self.api_key,
                **kwargs
            )
        except Exception as e:
            print(f"❌ LLM function error: {str(e)}")
            raise
    
    async def vision_model_func(self, prompt: str, system_prompt: Optional[str] = None, 
                               history_messages: List[Dict] = None, image_data: Optional[str] = None,
                               messages: Optional[List[Dict]] = None, **kwargs) -> str:
        """Vision model function for multimodal content."""
        try:
            # If messages format is provided (for VLM enhanced query), use LightRAG's function
            if messages:
                return await openai_complete_if_cache(
                    model=self.vision_model,
                    prompt="",  # Empty prompt when using messages format
                    system_prompt=None,
                    history_messages=[],
                    messages=messages,
                    base_url=self.base_url,
                    api_key=self.api_key,
                    **kwargs
                )
            
            # Traditional single image format
            elif image_data:
                # Construct messages for image input
                vision_messages = []
                if system_prompt:
                    vision_messages.append({"role": "system", "content": system_prompt})
                if history_messages:
                    vision_messages.extend(history_messages)
                
                vision_messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                        }
                    ]
                })
                
                return await openai_complete_if_cache(
                    model=self.vision_model,
                    prompt="",
                    system_prompt=None,
                    history_messages=[],
                    messages=vision_messages,
                    base_url=self.base_url,
                    api_key=self.api_key,
                    **kwargs
                )
            
            # Pure text format - fallback to regular LLM
            else:
                return await self.llm_model_func(prompt, system_prompt, history_messages, **kwargs)
                
        except Exception as e:
            print(f"❌ Vision model error: {str(e)}")
            # Fallback to text-only model
            return await self.llm_model_func(prompt, system_prompt, history_messages, **kwargs)
    
    def embedding_func_factory(self):
        async def embedding_func(texts: List[str]) -> List[List[float]]:
            """
            Embedding function using LMStudio's embedding API.
            Uses nomic-embed-text-v1.5 as default model with 768 dimensions.
            """
            try:
                embeddings = []
                for text in texts:
                    response = await self.client.embeddings.create(
                        model=self.embedding_model,
                        input=text
                    )
                    embeddings.append(response.data[0].embedding)
                return embeddings
            except Exception as e:
                print(f"❌ LMStudio embeddings failed with model '{self.embedding_model}': {e}")
                raise RuntimeError(
                    f"LMStudio embeddings unavailable. Ensure embedding model '{self.embedding_model}' is loaded."
                )
        
        return EmbeddingFunc(
            embedding_dim=768,  # nomic-embed-text-v1.5 default dimension
            max_token_size=8192,  # nomic-embed-text-v1.5 context length
            func=embedding_func
        )
    
    async def initialize_rag(self):
        """Initialize RAG-Anything with LMStudio functions."""
        print("Initializing RAG-Anything with LMStudio...")
        
        try:
            self.rag = RAGAnything(
                config=self.config,
                llm_model_func=self.llm_model_func,
                vision_model_func=self.vision_model_func,
                embedding_func=self.embedding_func_factory(),
            )
            print("✅ RAG-Anything initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ RAG initialization failed: {str(e)}")
            return False
    
    async def process_document_example(self, file_path: str):
        """Example: Process a document with LMStudio backend."""
        if not self.rag:
            print("❌ RAG not initialized. Call initialize_rag() first.")
            return
        
        try:
            print(f"📄 Processing document: {file_path}")
            await self.rag.process_document_complete(
                file_path=file_path,
                output_dir="./lmstudio_output",
                parse_method="auto",
                display_stats=True
            )
            print("✅ Document processing completed!")
        except Exception as e:
            print(f"❌ Document processing failed: {str(e)}")
    
    async def query_examples(self):
        """Example queries with different modes."""
        if not self.rag:
            print("❌ RAG not initialized. Call initialize_rag() first.")
            return
        
        # Example queries
        queries = [
            ("What are the main topics in the processed documents?", "hybrid"),
            ("Summarize any tables or data found in the documents", "local"),
            ("What images or figures are mentioned?", "global"),
        ]
        
        print("\n🔍 Running example queries...")
        for query, mode in queries:
            try:
                print(f"\nQuery ({mode}): {query}")
                result = await self.rag.aquery(query, mode=mode)
                print(f"Answer: {result[:200]}...")
            except Exception as e:
                print(f"❌ Query failed: {str(e)}")
    
    async def multimodal_query_example(self):
        """Example multimodal query."""
        if not self.rag:
            print("❌ RAG not initialized")
            return
        
        try:
            print("\nTesting multimodal query...")
            
            # Example with table data
            result = await self.rag.aquery_with_multimodal(
                "Analyze this performance data and compare it with document content",
                multimodal_content=[{
                    "type": "table",
                    "table_data": """Method,Accuracy,Speed
LMStudio + RAG,95.2%,Fast
Traditional RAG,87.3%,Medium
Baseline,75.1%,Slow""",
                    "table_caption": "Performance Comparison"
                }],
                mode="hybrid"
            )
            print(f"✅ Multimodal query result: {result[:200]}...")
            
        except Exception as e:
            print(f"❌ Multimodal query failed: {str(e)}")

async def main():
    """Main example function."""
    print("=" * 70)
    print("LMStudio + RAG-Anything Integration Example")
    print("=" * 70)
    
    # Initialize integration
    integration = LMStudioRAGIntegration()
    
    # Test connection
    if not await integration.test_connection():
        return False
    
    print()
    if not await integration.test_chat_completion():
        return False
    
    # Initialize RAG
    print("\n" + "─" * 50)
    if not await integration.initialize_rag():
        return False
    
    # Example document processing (uncomment and provide a real file path)
    # await integration.process_document_example("path/to/your/document.pdf")
    
    # Example queries (uncomment after processing documents)
    # await integration.query_examples()
    
    # Example multimodal query
    await integration.multimodal_query_example()
    
    print("\n" + "=" * 70)
    print("Integration example completed successfully!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    print("🚀 Starting LMStudio integration example...")
    success = asyncio.run(main())
    
    exit(0 if success else 1)
