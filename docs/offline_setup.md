# Running RAG-Anything in an Offline Environment

This document explains a critical consideration for running the RAG-Anything project in an environment with no internet access.

## The Network Dependency: `LightRAG` and `tiktoken`

The `RAGAnything` core engine relies on the `LightRAG` library for its primary functionality. `LightRAG`, in turn, uses OpenAI's `tiktoken` library for text tokenization.

By default, the `tiktoken` library has a network dependency. On its first use, it attempts to download tokenizer models from OpenAI's public servers (`openaipublic.blob.core.windows.net`). If the application is running in an offline or network-restricted environment, this download will fail, causing the `LightRAG` instance to fail to initialize.

This results in an error similar to the following:

```
Failed to initialize LightRAG instance: HTTPSConnectionPool(host='openaipublic.blob.core.windows.net', port=443): Max retries exceeded with url: /encodings/o200k_ba
```

This dependency is indirect. The `RAG-Anything` codebase itself does not directly import or call `tiktoken`. The call is made from within the `lightrag` library.

## The Solution: Using a Local `tiktoken` Cache

To resolve this issue and enable fully offline operation, you must provide a local cache for the `tiktoken` models. This is achieved by setting the `TIKTOKEN_CACHE_DIR` environment variable.

When this environment variable is set, `tiktoken` will look for its model files in the specified local directory instead of attempting to download them from the internet.

### Steps to Implement the Solution:

1.  **Create a Model Cache:** In an environment *with* internet access, run a simple Python script to download and cache the necessary `tiktoken` models.

    ```python
    import tiktoken
    import os

    # Define the directory where you want to store the cache
    cache_dir = "./tiktoken_cache"
    if "TIKTOKEN_CACHE_DIR" not in os.environ:
        os.environ["TIKTOKEN_CACHE_DIR"] = cache_dir

    # Create the directory if it doesn't exist
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    print("Downloading and caching tiktoken models...")
    tiktoken.get_encoding("cl100k_base")
    # tiktoken.get_encoding("p50k_base")

    print(f"tiktoken models have been cached in '{cache_dir}'")
    ```

2.  **Deploy the Cache:** Copy the created `tiktoken_cache` directory to the machine where you will be running the `RAG-Anything` application.

By following these steps, you can eliminate the network dependency and run the `RAG-Anything` project successfully in a fully offline environment.