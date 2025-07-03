"""
Specialized processors for different modalities

Includes:
- ImageModalProcessor: Specialized processor for image content
- TableModalProcessor: Specialized processor for table content
- EquationModalProcessor: Specialized processor for equation content
- GenericModalProcessor: Processor for other modal content
"""

import re
import json
import time
import asyncio
import base64
from typing import Dict, Any, Tuple, cast, List
from pathlib import Path

from lightrag.base import StorageNameSpace
from lightrag.utils import (
    logger,
    compute_mdhash_id,
)
from lightrag.lightrag import LightRAG
from dataclasses import asdict
from lightrag.kg.shared_storage import get_namespace_data, get_pipeline_status_lock

# Import prompt templates
from raganything.prompt import PROMPTS


class BaseModalProcessor:
    """Base class for modal processors"""

    def __init__(self, lightrag: LightRAG, modal_caption_func):
        """Initialize base processor

        Args:
            lightrag: LightRAG instance
            modal_caption_func: Function for generating descriptions
        """
        self.lightrag = lightrag
        self.modal_caption_func = modal_caption_func

        # Use LightRAG's storage instances
        self.text_chunks_db = lightrag.text_chunks
        self.chunks_vdb = lightrag.chunks_vdb
        self.entities_vdb = lightrag.entities_vdb
        self.relationships_vdb = lightrag.relationships_vdb
        self.knowledge_graph_inst = lightrag.chunk_entity_relation_graph

        # Use LightRAG's configuration and functions
        self.embedding_func = lightrag.embedding_func
        self.llm_model_func = lightrag.llm_model_func
        self.global_config = asdict(lightrag)
        self.hashing_kv = lightrag.llm_response_cache
        self.tokenizer = lightrag.tokenizer

    async def process_multimodal_content(
        self,
        modal_content,
        content_type: str,
        file_path: str = "manual_creation",
        entity_name: str = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """Process multimodal content"""
        # Subclasses need to implement specific processing logic
        raise NotImplementedError("Subclasses must implement this method")

    async def process_multimodal_content_batch(
        self,
        modal_content,
        content_type: str,
        file_path: str = "manual_creation",
        entity_name: str = None,
    ) -> Tuple[str, Dict[str, Any], List[Tuple]]:
        """Process multimodal content in batch mode (returns chunk results for later merging)"""
        # Subclasses need to implement specific processing logic
        raise NotImplementedError("Subclasses must implement this method")

    async def _create_entity_and_chunk(
        self, modal_chunk: str, entity_info: Dict[str, Any], file_path: str
    ) -> Tuple[str, Dict[str, Any]]:
        """Create entity and text chunk"""
        # Create chunk
        chunk_id = compute_mdhash_id(str(modal_chunk), prefix="chunk-")
        tokens = len(self.tokenizer.encode(modal_chunk))

        chunk_data = {
            "tokens": tokens,
            "content": modal_chunk,
            "chunk_order_index": 0,
            "full_doc_id": chunk_id,
            "file_path": file_path,
        }

        # Store chunk
        await self.text_chunks_db.upsert({chunk_id: chunk_data})

        # Create entity node
        node_data = {
            "entity_id": entity_info["entity_name"],
            "entity_type": entity_info["entity_type"],
            "description": entity_info["summary"],
            "source_id": chunk_id,
            "file_path": file_path,
            "created_at": int(time.time()),
        }

        await self.knowledge_graph_inst.upsert_node(
            entity_info["entity_name"], node_data
        )

        # Insert entity into vector database
        entity_vdb_data = {
            compute_mdhash_id(entity_info["entity_name"], prefix="ent-"): {
                "entity_name": entity_info["entity_name"],
                "entity_type": entity_info["entity_type"],
                "content": f"{entity_info['entity_name']}\n{entity_info['summary']}",
                "source_id": chunk_id,
                "file_path": file_path,
            }
        }
        await self.entities_vdb.upsert(entity_vdb_data)

        # Process entity and relationship extraction
        await self._process_chunk_for_extraction(chunk_id, entity_info["entity_name"])

        # Ensure all storage updates are complete
        await self._insert_done()

        return entity_info["summary"], {
            "entity_name": entity_info["entity_name"],
            "entity_type": entity_info["entity_type"],
            "description": entity_info["summary"],
            "chunk_id": chunk_id,
        }

    async def _create_entity_and_chunk_batch(
        self, modal_chunk: str, entity_info: Dict[str, Any], file_path: str
    ) -> Tuple[str, Dict[str, Any], List[Tuple]]:
        """Create entity and text chunk for batch processing (returns chunk results instead of merging immediately)"""
        # Create chunk
        chunk_id = compute_mdhash_id(str(modal_chunk), prefix="chunk-")
        tokens = len(self.tokenizer.encode(modal_chunk))

        chunk_data = {
            "tokens": tokens,
            "content": modal_chunk,
            "chunk_order_index": 0,
            "full_doc_id": chunk_id,
            "file_path": file_path,  # Ensure file_path is set correctly
        }

        # Store chunk
        await self.text_chunks_db.upsert({chunk_id: chunk_data})

        # Create entity node
        node_data = {
            "entity_id": entity_info["entity_name"],
            "entity_type": entity_info["entity_type"],
            "description": entity_info["summary"],
            "source_id": chunk_id,
            "file_path": file_path,  # Ensure file_path is set correctly
            "created_at": int(time.time()),
        }

        await self.knowledge_graph_inst.upsert_node(
            entity_info["entity_name"], node_data
        )

        # Insert entity into vector database
        entity_vdb_data = {
            compute_mdhash_id(entity_info["entity_name"], prefix="ent-"): {
                "entity_name": entity_info["entity_name"],
                "entity_type": entity_info["entity_type"],
                "content": f"{entity_info['entity_name']}\n{entity_info['summary']}",
                "source_id": chunk_id,
                "file_path": file_path,  # Ensure file_path is set correctly
            }
        }
        await self.entities_vdb.upsert(entity_vdb_data)

        # Create text chunk for vector database
        chunk_vdb_data = {
            chunk_id: {
                "content": chunk_data["content"],
                "full_doc_id": chunk_id,
                "tokens": chunk_data["tokens"],
                "chunk_order_index": chunk_data["chunk_order_index"],
                "file_path": file_path,  # Ensure file_path is set correctly
            }
        }

        await self.chunks_vdb.upsert(chunk_vdb_data)

        # Get chunk results for batch processing instead of immediate extraction
        chunk_results = await self._get_chunk_results_for_batch(
            chunk_id, entity_info["entity_name"], file_path
        )

        return (
            entity_info["summary"],
            {
                "entity_name": entity_info["entity_name"],
                "entity_type": entity_info["entity_type"],
                "description": entity_info["summary"],
                "chunk_id": chunk_id,
            },
            chunk_results,
        )

    async def _process_chunk_for_extraction(
        self, chunk_id: str, modal_entity_name: str
    ):
        """Process chunk for entity and relationship extraction"""
        chunk_data = await self.text_chunks_db.get_by_id(chunk_id)
        if not chunk_data:
            logger.error(f"Chunk {chunk_id} not found")
            return

        # Create text chunk for vector database
        chunk_vdb_data = {
            chunk_id: {
                "content": chunk_data["content"],
                "full_doc_id": chunk_id,
                "tokens": chunk_data["tokens"],
                "chunk_order_index": chunk_data["chunk_order_index"],
                "file_path": chunk_data["file_path"],
            }
        }

        await self.chunks_vdb.upsert(chunk_vdb_data)

        # Trigger extraction process
        from lightrag.operate import extract_entities, merge_nodes_and_edges

        pipeline_status = await get_namespace_data("pipeline_status")
        pipeline_status_lock = get_pipeline_status_lock()

        # Prepare chunk for extraction
        chunks = {chunk_id: chunk_data}

        # Extract entities and relationships
        chunk_results = await extract_entities(
            chunks=chunks,
            global_config=self.global_config,
            pipeline_status=pipeline_status,
            pipeline_status_lock=pipeline_status_lock,
            llm_response_cache=self.hashing_kv,
        )

        # Add "belongs_to" relationships for all extracted entities
        for maybe_nodes, maybe_edges in chunk_results:
            for entity_name in maybe_nodes.keys():
                if entity_name != modal_entity_name:  # Skip self-relationship
                    # Create belongs_to relationship
                    relation_data = {
                        "description": f"Entity {entity_name} belongs to {modal_entity_name}",
                        "keywords": "belongs_to,part_of,contained_in",
                        "source_id": chunk_id,
                        "weight": 10.0,
                        "file_path": chunk_data.get("file_path", "manual_creation"),
                    }
                    await self.knowledge_graph_inst.upsert_edge(
                        entity_name, modal_entity_name, relation_data
                    )

                    relation_id = compute_mdhash_id(
                        entity_name + modal_entity_name, prefix="rel-"
                    )
                    relation_vdb_data = {
                        relation_id: {
                            "src_id": entity_name,
                            "tgt_id": modal_entity_name,
                            "keywords": relation_data["keywords"],
                            "content": f"{relation_data['keywords']}\t{entity_name}\n{modal_entity_name}\n{relation_data['description']}",
                            "source_id": chunk_id,
                            "file_path": chunk_data.get("file_path", "manual_creation"),
                        }
                    }
                    await self.relationships_vdb.upsert(relation_vdb_data)

        # Merge with correct file_path parameter
        file_path = chunk_data.get("file_path", "manual_creation")
        await merge_nodes_and_edges(
            chunk_results=chunk_results,
            knowledge_graph_inst=self.knowledge_graph_inst,
            entity_vdb=self.entities_vdb,
            relationships_vdb=self.relationships_vdb,
            global_config=self.global_config,
            pipeline_status=pipeline_status,
            pipeline_status_lock=pipeline_status_lock,
            llm_response_cache=self.hashing_kv,
            current_file_number=1,
            total_files=1,
            file_path=file_path,  # Pass the correct file_path
        )

    async def _insert_done(self) -> None:
        await asyncio.gather(
            *[
                cast(StorageNameSpace, storage_inst).index_done_callback()
                for storage_inst in [
                    self.text_chunks_db,
                    self.chunks_vdb,
                    self.entities_vdb,
                    self.relationships_vdb,
                    self.knowledge_graph_inst,
                ]
            ]
        )

    async def _get_chunk_results_for_batch(
        self, chunk_id: str, modal_entity_name: str, file_path: str
    ) -> List[Tuple]:
        """Get chunk results for batch processing instead of immediate extraction"""
        chunk_data = await self.text_chunks_db.get_by_id(chunk_id)
        if not chunk_data:
            logger.error(f"Chunk {chunk_id} not found")
            return []

        # Trigger extraction process
        from lightrag.operate import extract_entities

        pipeline_status = await get_namespace_data("pipeline_status")
        pipeline_status_lock = get_pipeline_status_lock()

        # Prepare chunk for extraction
        chunks = {chunk_id: chunk_data}

        # Extract entities and relationships
        chunk_results = await extract_entities(
            chunks=chunks,
            global_config=self.global_config,
            pipeline_status=pipeline_status,
            pipeline_status_lock=pipeline_status_lock,
            llm_response_cache=self.hashing_kv,
        )

        # Add "belongs_to" relationships for all extracted entities
        processed_chunk_results = []
        for maybe_nodes, maybe_edges in chunk_results:
            # Add belongs_to relationships
            for entity_name in maybe_nodes.keys():
                if entity_name != modal_entity_name:  # Skip self-relationship
                    # Create belongs_to relationship data
                    relation_data = {
                        "src_id": entity_name,
                        "tgt_id": modal_entity_name,
                        "description": f"Entity {entity_name} belongs to {modal_entity_name}",
                        "keywords": "belongs_to,part_of,contained_in",
                        "source_id": chunk_id,
                        "weight": 10.0,
                        "file_path": file_path,
                    }

                    # Add to maybe_edges
                    maybe_edges[(entity_name, modal_entity_name)] = [relation_data]

            processed_chunk_results.append((maybe_nodes, maybe_edges))

        return processed_chunk_results


class ImageModalProcessor(BaseModalProcessor):
    """Processor specialized for image content"""

    def __init__(self, lightrag: LightRAG, modal_caption_func):
        """Initialize image processor

        Args:
            lightrag: LightRAG instance
            modal_caption_func: Function for generating descriptions (supporting image understanding)
        """
        super().__init__(lightrag, modal_caption_func)

    def _encode_image_to_base64(self, image_path: str) -> str:
        """Encode image to base64"""
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_string
        except Exception as e:
            logger.error(f"Failed to encode image {image_path}: {e}")
            return ""

    async def process_multimodal_content(
        self,
        modal_content,
        content_type: str,
        file_path: str = "manual_creation",
        entity_name: str = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """Process image content"""
        try:
            # Parse image content
            if isinstance(modal_content, str):
                try:
                    content_data = json.loads(modal_content)
                except json.JSONDecodeError:
                    content_data = {"description": modal_content}
            else:
                content_data = modal_content

            image_path = content_data.get("img_path")
            captions = content_data.get("img_caption", [])
            footnotes = content_data.get("img_footnote", [])

            # Build detailed visual analysis prompt
            vision_prompt = PROMPTS["vision_prompt"].format(
                entity_name=entity_name
                if entity_name
                else "unique descriptive name for this image",
                image_path=image_path,
                captions=captions if captions else "None",
                footnotes=footnotes if footnotes else "None",
            )

            # If image path exists, try to encode image
            image_base64 = ""
            if image_path and Path(image_path).exists():
                image_base64 = self._encode_image_to_base64(image_path)

            # Call vision model
            if image_base64:
                # Use real image for analysis
                response = await self.modal_caption_func(
                    vision_prompt,
                    image_data=image_base64,
                    system_prompt=PROMPTS["IMAGE_ANALYSIS_SYSTEM"],
                )
            else:
                # Analyze based on existing text information
                text_prompt = PROMPTS["text_prompt"].format(
                    image_path=image_path,
                    captions=captions,
                    footnotes=footnotes,
                    vision_prompt=vision_prompt,
                )

                response = await self.modal_caption_func(
                    text_prompt,
                    system_prompt=PROMPTS["IMAGE_ANALYSIS_FALLBACK_SYSTEM"],
                )

            # Parse response
            enhanced_caption, entity_info = self._parse_response(response, entity_name)

            # Build complete image content
            modal_chunk = PROMPTS["image_chunk"].format(
                image_path=image_path,
                captions=", ".join(captions) if captions else "None",
                footnotes=", ".join(footnotes) if footnotes else "None",
                enhanced_caption=enhanced_caption,
            )

            return await self._create_entity_and_chunk(
                modal_chunk, entity_info, file_path
            )

        except Exception as e:
            logger.error(f"Error processing image content: {e}")
            # Fallback processing
            fallback_entity = {
                "entity_name": entity_name
                if entity_name
                else f"image_{compute_mdhash_id(str(modal_content))}",
                "entity_type": "image",
                "summary": f"Image content: {str(modal_content)[:100]}",
            }
            return str(modal_content), fallback_entity

    def _parse_response(
        self, response: str, entity_name: str = None
    ) -> Tuple[str, Dict[str, Any]]:
        """Parse model response"""
        try:
            response_data = json.loads(
                re.search(r"\{.*\}", response, re.DOTALL).group(0)
            )

            description = response_data.get("detailed_description", "")
            entity_data = response_data.get("entity_info", {})

            if not description or not entity_data:
                raise ValueError("Missing required fields in response")

            if not all(
                key in entity_data for key in ["entity_name", "entity_type", "summary"]
            ):
                raise ValueError("Missing required fields in entity_info")

            entity_data["entity_name"] = (
                entity_data["entity_name"] + f" ({entity_data['entity_type']})"
            )
            if entity_name:
                entity_data["entity_name"] = entity_name

            return description, entity_data

        except (json.JSONDecodeError, AttributeError, ValueError) as e:
            logger.error(f"Error parsing image analysis response: {e}")
            fallback_entity = {
                "entity_name": entity_name
                if entity_name
                else f"image_{compute_mdhash_id(response)}",
                "entity_type": "image",
                "summary": response[:100] + "..." if len(response) > 100 else response,
            }
            return response, fallback_entity

    async def process_multimodal_content_batch(
        self,
        modal_content,
        content_type: str,
        file_path: str = "manual_creation",
        entity_name: str = None,
    ) -> Tuple[str, Dict[str, Any], List[Tuple]]:
        """Process image content in batch mode"""
        try:
            # Parse image content
            if isinstance(modal_content, str):
                try:
                    content_data = json.loads(modal_content)
                except json.JSONDecodeError:
                    content_data = {"description": modal_content}
            else:
                content_data = modal_content

            image_path = content_data.get("img_path")
            captions = content_data.get("img_caption", [])
            footnotes = content_data.get("img_footnote", [])

            # Build detailed visual analysis prompt
            vision_prompt = PROMPTS["vision_prompt"].format(
                entity_name=entity_name
                if entity_name
                else "unique descriptive name for this image",
                image_path=image_path,
                captions=captions if captions else "None",
                footnotes=footnotes if footnotes else "None",
            )

            # If image path exists, try to encode image
            image_base64 = ""
            if image_path and Path(image_path).exists():
                image_base64 = self._encode_image_to_base64(image_path)

            # Call vision model
            if image_base64:
                # Use real image for analysis
                response = await self.modal_caption_func(
                    vision_prompt,
                    image_data=image_base64,
                    system_prompt=PROMPTS["IMAGE_ANALYSIS_SYSTEM"],
                )
            else:
                # Analyze based on existing text information
                text_prompt = PROMPTS["text_prompt"].format(
                    image_path=image_path,
                    captions=captions,
                    footnotes=footnotes,
                    vision_prompt=vision_prompt,
                )

                response = await self.modal_caption_func(
                    text_prompt,
                    system_prompt=PROMPTS["IMAGE_ANALYSIS_FALLBACK_SYSTEM"],
                )

            # Parse response
            enhanced_caption, entity_info = self._parse_response(response, entity_name)

            # Build complete image content
            modal_chunk = PROMPTS["image_chunk"].format(
                image_path=image_path,
                captions=", ".join(captions) if captions else "None",
                footnotes=", ".join(footnotes) if footnotes else "None",
                enhanced_caption=enhanced_caption,
            )

            return await self._create_entity_and_chunk_batch(
                modal_chunk, entity_info, file_path
            )

        except Exception as e:
            logger.error(f"Error processing image content: {e}")
            # Fallback processing
            fallback_entity = {
                "entity_name": entity_name
                if entity_name
                else f"image_{compute_mdhash_id(str(modal_content))}",
                "entity_type": "image",
                "summary": f"Image content: {str(modal_content)[:100]}",
            }
            return str(modal_content), fallback_entity, []


class TableModalProcessor(BaseModalProcessor):
    """Processor specialized for table content"""

    async def process_multimodal_content(
        self,
        modal_content,
        content_type: str,
        file_path: str = "manual_creation",
        entity_name: str = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """Process table content"""
        # Parse table content
        if isinstance(modal_content, str):
            try:
                content_data = json.loads(modal_content)
            except json.JSONDecodeError:
                content_data = {"table_body": modal_content}
        else:
            content_data = modal_content

        table_img_path = content_data.get("img_path")
        table_caption = content_data.get("table_caption", [])
        table_body = content_data.get("table_body", "")
        table_footnote = content_data.get("table_footnote", [])

        # Build table analysis prompt
        table_prompt = PROMPTS["table_prompt"].format(
            entity_name=entity_name
            if entity_name
            else "descriptive name for this table",
            table_img_path=table_img_path,
            table_caption=table_caption if table_caption else "None",
            table_body=table_body,
            table_footnote=table_footnote if table_footnote else "None",
        )

        response = await self.modal_caption_func(
            table_prompt,
            system_prompt=PROMPTS["TABLE_ANALYSIS_SYSTEM"],
        )

        # Parse response
        enhanced_caption, entity_info = self._parse_table_response(
            response, entity_name
        )

        # TODO: Add Retry Mechanism

        # Build complete table content
        modal_chunk = PROMPTS["table_chunk"].format(
            table_img_path=table_img_path,
            table_caption=", ".join(table_caption) if table_caption else "None",
            table_body=table_body,
            table_footnote=", ".join(table_footnote) if table_footnote else "None",
            enhanced_caption=enhanced_caption,
        )

        return await self._create_entity_and_chunk(modal_chunk, entity_info, file_path)

    def _parse_table_response(
        self, response: str, entity_name: str = None
    ) -> Tuple[str, Dict[str, Any]]:
        """Parse table analysis response"""
        try:
            response_data = json.loads(
                re.search(r"\{.*\}", response, re.DOTALL).group(0)
            )

            description = response_data.get("detailed_description", "")
            entity_data = response_data.get("entity_info", {})

            if not description or not entity_data:
                raise ValueError("Missing required fields in response")

            if not all(
                key in entity_data for key in ["entity_name", "entity_type", "summary"]
            ):
                raise ValueError("Missing required fields in entity_info")

            entity_data["entity_name"] = (
                entity_data["entity_name"] + f" ({entity_data['entity_type']})"
            )
            if entity_name:
                entity_data["entity_name"] = entity_name

            return description, entity_data

        except (json.JSONDecodeError, AttributeError, ValueError) as e:
            logger.error(f"Error parsing table analysis response: {e}")
            fallback_entity = {
                "entity_name": entity_name
                if entity_name
                else f"table_{compute_mdhash_id(response)}",
                "entity_type": "table",
                "summary": response[:100] + "..." if len(response) > 100 else response,
            }
            return response, fallback_entity

    async def process_multimodal_content_batch(
        self,
        modal_content,
        content_type: str,
        file_path: str = "manual_creation",
        entity_name: str = None,
    ) -> Tuple[str, Dict[str, Any], List[Tuple]]:
        """Process table content in batch mode"""
        # Parse table content
        if isinstance(modal_content, str):
            try:
                content_data = json.loads(modal_content)
            except json.JSONDecodeError:
                content_data = {"table_body": modal_content}
        else:
            content_data = modal_content

        table_img_path = content_data.get("img_path")
        table_caption = content_data.get("table_caption", [])
        table_body = content_data.get("table_body", "")
        table_footnote = content_data.get("table_footnote", [])

        # Build table analysis prompt
        table_prompt = PROMPTS["table_prompt"].format(
            entity_name=entity_name
            if entity_name
            else "descriptive name for this table",
            table_img_path=table_img_path,
            table_caption=table_caption if table_caption else "None",
            table_body=table_body,
            table_footnote=table_footnote if table_footnote else "None",
        )

        response = await self.modal_caption_func(
            table_prompt,
            system_prompt=PROMPTS["TABLE_ANALYSIS_SYSTEM"],
        )

        # Parse response
        enhanced_caption, entity_info = self._parse_table_response(
            response, entity_name
        )

        # TODO: Add Retry Mechanism

        # Build complete table content
        modal_chunk = PROMPTS["table_chunk"].format(
            table_img_path=table_img_path,
            table_caption=", ".join(table_caption) if table_caption else "None",
            table_body=table_body,
            table_footnote=", ".join(table_footnote) if table_footnote else "None",
            enhanced_caption=enhanced_caption,
        )

        return await self._create_entity_and_chunk_batch(
            modal_chunk, entity_info, file_path
        )


class EquationModalProcessor(BaseModalProcessor):
    """Processor specialized for equation content"""

    async def process_multimodal_content(
        self,
        modal_content,
        content_type: str,
        file_path: str = "manual_creation",
        entity_name: str = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """Process equation content"""
        # Parse equation content
        if isinstance(modal_content, str):
            try:
                content_data = json.loads(modal_content)
            except json.JSONDecodeError:
                content_data = {"equation": modal_content}
        else:
            content_data = modal_content

        equation_text = content_data.get("text")
        equation_format = content_data.get("text_format", "")

        # Build equation analysis prompt
        equation_prompt = PROMPTS["equation_prompt"].format(
            equation_text=equation_text,
            equation_format=equation_format,
            entity_name=entity_name
            if entity_name
            else "descriptive name for this equation",
        )

        response = await self.modal_caption_func(
            equation_prompt,
            system_prompt=PROMPTS["EQUATION_ANALYSIS_SYSTEM"],
        )

        # Parse response
        enhanced_caption, entity_info = self._parse_equation_response(
            response, entity_name
        )

        # Build complete equation content
        modal_chunk = PROMPTS["equation_chunk"].format(
            equation_text=equation_text,
            equation_format=equation_format,
            enhanced_caption=enhanced_caption,
        )

        return await self._create_entity_and_chunk(modal_chunk, entity_info, file_path)

    async def process_multimodal_content_batch(
        self,
        modal_content,
        content_type: str,
        file_path: str = "manual_creation",
        entity_name: str = None,
    ) -> Tuple[str, Dict[str, Any], List[Tuple]]:
        """Process equation content in batch mode"""
        # Parse equation content
        if isinstance(modal_content, str):
            try:
                content_data = json.loads(modal_content)
            except json.JSONDecodeError:
                content_data = {"equation": modal_content}
        else:
            content_data = modal_content

        equation_text = content_data.get("text")
        equation_format = content_data.get("text_format", "")

        # Build equation analysis prompt
        equation_prompt = PROMPTS["equation_prompt"].format(
            equation_text=equation_text,
            equation_format=equation_format,
            entity_name=entity_name
            if entity_name
            else "descriptive name for this equation",
        )

        response = await self.modal_caption_func(
            equation_prompt,
            system_prompt=PROMPTS["EQUATION_ANALYSIS_SYSTEM"],
        )

        # Parse response
        enhanced_caption, entity_info = self._parse_equation_response(
            response, entity_name
        )

        # Build complete equation content
        modal_chunk = PROMPTS["equation_chunk"].format(
            equation_text=equation_text,
            equation_format=equation_format,
            enhanced_caption=enhanced_caption,
        )

        return await self._create_entity_and_chunk_batch(
            modal_chunk, entity_info, file_path
        )

    def _parse_equation_response(
        self, response: str, entity_name: str = None
    ) -> Tuple[str, Dict[str, Any]]:
        """Parse equation analysis response"""
        try:
            response_data = json.loads(
                re.search(r"\{.*\}", response, re.DOTALL).group(0)
            )

            description = response_data.get("detailed_description", "")
            entity_data = response_data.get("entity_info", {})

            if not description or not entity_data:
                raise ValueError("Missing required fields in response")

            if not all(
                key in entity_data for key in ["entity_name", "entity_type", "summary"]
            ):
                raise ValueError("Missing required fields in entity_info")

            entity_data["entity_name"] = (
                entity_data["entity_name"] + f" ({entity_data['entity_type']})"
            )
            if entity_name:
                entity_data["entity_name"] = entity_name

            return description, entity_data

        except (json.JSONDecodeError, AttributeError, ValueError) as e:
            logger.error(f"Error parsing equation analysis response: {e}")
            fallback_entity = {
                "entity_name": entity_name
                if entity_name
                else f"equation_{compute_mdhash_id(response)}",
                "entity_type": "equation",
                "summary": response[:100] + "..." if len(response) > 100 else response,
            }
            return response, fallback_entity


class GenericModalProcessor(BaseModalProcessor):
    """Generic processor for other types of modal content"""

    async def process_multimodal_content(
        self,
        modal_content,
        content_type: str,
        file_path: str = "manual_creation",
        entity_name: str = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """Process generic modal content"""
        # Build generic analysis prompt
        generic_prompt = PROMPTS["generic_prompt"].format(
            content_type=content_type,
            entity_name=entity_name
            if entity_name
            else f"descriptive name for this {content_type}",
            content=str(modal_content),
        )

        response = await self.modal_caption_func(
            generic_prompt,
            system_prompt=PROMPTS["GENERIC_ANALYSIS_SYSTEM"].format(
                content_type=content_type
            ),
        )

        # Parse response
        enhanced_caption, entity_info = self._parse_generic_response(
            response, entity_name, content_type
        )

        # Build complete content
        modal_chunk = PROMPTS["generic_chunk"].format(
            content_type=content_type.title(),
            content=str(modal_content),
            enhanced_caption=enhanced_caption,
        )

        return await self._create_entity_and_chunk(modal_chunk, entity_info, file_path)

    def _parse_generic_response(
        self, response: str, entity_name: str = None, content_type: str = "content"
    ) -> Tuple[str, Dict[str, Any]]:
        """Parse generic analysis response"""
        try:
            response_data = json.loads(
                re.search(r"\{.*\}", response, re.DOTALL).group(0)
            )

            description = response_data.get("detailed_description", "")
            entity_data = response_data.get("entity_info", {})

            if not description or not entity_data:
                raise ValueError("Missing required fields in response")

            if not all(
                key in entity_data for key in ["entity_name", "entity_type", "summary"]
            ):
                raise ValueError("Missing required fields in entity_info")

            entity_data["entity_name"] = (
                entity_data["entity_name"] + f" ({entity_data['entity_type']})"
            )
            if entity_name:
                entity_data["entity_name"] = entity_name

            return description, entity_data

        except (json.JSONDecodeError, AttributeError, ValueError) as e:
            logger.error(f"Error parsing generic analysis response: {e}")
            fallback_entity = {
                "entity_name": entity_name
                if entity_name
                else f"{content_type}_{compute_mdhash_id(response)}",
                "entity_type": content_type,
                "summary": response[:100] + "..." if len(response) > 100 else response,
            }
            return response, fallback_entity

    async def process_multimodal_content_batch(
        self,
        modal_content,
        content_type: str,
        file_path: str = "manual_creation",
        entity_name: str = None,
    ) -> Tuple[str, Dict[str, Any], List[Tuple]]:
        """Process generic modal content in batch mode"""
        # Build generic analysis prompt
        generic_prompt = PROMPTS["generic_prompt"].format(
            content_type=content_type,
            entity_name=entity_name
            if entity_name
            else f"descriptive name for this {content_type}",
            content=str(modal_content),
        )

        response = await self.modal_caption_func(
            generic_prompt,
            system_prompt=PROMPTS["GENERIC_ANALYSIS_SYSTEM"].format(
                content_type=content_type
            ),
        )

        # Parse response
        enhanced_caption, entity_info = self._parse_generic_response(
            response, entity_name, content_type
        )

        # Build complete content
        modal_chunk = PROMPTS["generic_chunk"].format(
            content_type=content_type.title(),
            content=str(modal_content),
            enhanced_caption=enhanced_caption,
        )

        return await self._create_entity_and_chunk_batch(
            modal_chunk, entity_info, file_path
        )
