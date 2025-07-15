# type: ignore
"""
Generic Document Parser Utility

This module provides functionality for parsing PDF and image documents using MinerU 2.0 library,
and converts the parsing results into markdown and JSON formats

Note: MinerU 2.0 no longer includes LibreOffice document conversion module.
For Office documents (.doc, .docx, .ppt, .pptx), please convert them to PDF format first.
"""

from __future__ import annotations


import json
import argparse
import base64
import subprocess
import tempfile
from pathlib import Path
from typing import (
    Dict,
    List,
    Optional,
    Union,
    Tuple,
    Any,
    TypeVar,
)

T = TypeVar("T")


class Parser:
    """
    Base class for document parsing utilities.

    Defines common functionality and constants for parsing different document types.
    """

    # Define common file formats
    OFFICE_FORMATS = {".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"}
    IMAGE_FORMATS = {".png", ".jpeg", ".jpg", ".bmp", ".tiff", ".tif", ".gif", ".webp"}
    TEXT_FORMATS = {".txt", ".md"}

    def __init__(self) -> None:
        """Initialize the base parser."""
        pass

    @staticmethod
    def convert_office_to_pdf(
        doc_path: Union[str, Path], output_dir: Optional[str] = None
    ) -> Path:
        """
        Convert Office document (.doc, .docx, .ppt, .pptx, .xls, .xlsx) to PDF.
        Requires LibreOffice to be installed.

        Args:
            doc_path: Path to the Office document file
            output_dir: Output directory for the PDF file

        Returns:
            Path to the generated PDF file
        """
        try:
            # Convert to Path object for easier handling
            doc_path = Path(doc_path)
            if not doc_path.exists():
                raise FileNotFoundError(f"Office document does not exist: {doc_path}")

            name_without_suff = doc_path.stem

            # Prepare output directory
            if output_dir:
                base_output_dir = Path(output_dir)
            else:
                base_output_dir = doc_path.parent / "libreoffice_output"

            base_output_dir.mkdir(parents=True, exist_ok=True)

            # LibreOffice command to convert Office to PDF
            # This assumes libreoffice is in the system PATH or a specific path
            # For Windows, you might need to specify the full path to soffice.exe
            # For Linux/Mac, it's usually just 'soffice'
            libreoffice_cmd = ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(base_output_dir)]
            libreoffice_cmd.append(str(doc_path))

            try:
                result = subprocess.run(
                    libreoffice_cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    encoding="utf-8",
                    errors="ignore",
                )
                print("LibreOffice command executed successfully")
                if result.stdout:
                    print(f"Output: {result.stdout}")
            except subprocess.CalledProcessError as e:
                print(f"Error running LibreOffice command: {e}")
                if e.stderr:
                    print(f"Error details: {e.stderr}")
                raise
            except FileNotFoundError:
                raise RuntimeError(
                    "LibreOffice is not found. Please ensure it is installed and in your PATH. "
                    "On Linux/Mac, you might need to install it via 'sudo apt-get install libreoffice' or similar."
                )

            # Find the generated PDF file
            pdf_file = base_output_dir / f"{name_without_suff}.pdf"
            if not pdf_file.exists():
                raise FileNotFoundError(f"PDF file not found after LibreOffice conversion: {pdf_file}")

            return pdf_file

        except Exception as e:
            print(f"Error in convert_office_to_pdf: {str(e)}")
            raise

    @staticmethod
    def convert_text_to_pdf(
        text_path: Union[str, Path], output_dir: Optional[str] = None
    ) -> Path:
        """
        Convert text file (.txt, .md) to PDF.
        Requires a text-to-PDF conversion tool like Pandoc or a similar library.

        Args:
            text_path: Path to the text file
            output_dir: Output directory for the PDF file

        Returns:
            Path to the generated PDF file
        """
        try:
            # Convert to Path object for easier handling
            text_path = Path(text_path)
            if not text_path.exists():
                raise FileNotFoundError(f"Text file does not exist: {text_path}")

            name_without_suff = text_path.stem

            # Prepare output directory
            if output_dir:
                base_output_dir = Path(output_dir)
            else:
                base_output_dir = text_path.parent / "pandoc_output"

            base_output_dir.mkdir(parents=True, exist_ok=True)

            # Pandoc command to convert text to PDF
            pandoc_cmd = ["pandoc", "--from", "markdown", "--to", "pdf", "--output", str(base_output_dir / f"{name_without_suff}.pdf")]
            pandoc_cmd.append(str(text_path))

            try:
                result = subprocess.run(
                    pandoc_cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    encoding="utf-8",
                    errors="ignore",
                )
                print("Pandoc command executed successfully")
                if result.stdout:
                    print(f"Output: {result.stdout}")
            except subprocess.CalledProcessError as e:
                print(f"Error running Pandoc command: {e}")
                if e.stderr:
                    print(f"Error details: {e.stderr}")
                raise
            except FileNotFoundError:
                raise RuntimeError(
                    "Pandoc is not found. Please ensure it is installed and in your PATH. "
                    "You can install it via 'pip install pandoc' or 'brew install pandoc' on macOS."
                )

            # Find the generated PDF file
            pdf_file = base_output_dir / f"{name_without_suff}.pdf"
            if not pdf_file.exists():
                raise FileNotFoundError(f"PDF file not found after Pandoc conversion: {pdf_file}")

            return pdf_file

        except Exception as e:
            print(f"Error in convert_text_to_pdf: {str(e)}")
            raise

    @staticmethod
    def _process_inline_markdown(text: str) -> str:
        """
        Process inline markdown formatting (bold, italic, code, links)

        Args:
            text: Raw text with markdown formatting

        Returns:
            Text with ReportLab markup
        """
        import re

        # Escape special characters for ReportLab
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        # Bold text: **text** or __text__
        text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"__(.*?)__", r"<b>\1</b>", text)

        # Italic text: *text* or _text_ (but not in the middle of words)
        text = re.sub(r"(?<!\w)\*([^*\n]+?)\*(?!\w)", r"<i>\1</i>", text)
        text = re.sub(r"(?<!\w)_([^_\n]+?)_(?!\w)", r"<i>\1</i>", text)

        # Inline code: `code`
        text = re.sub(
            r"`([^`]+?)`",
            r'<font name="Courier" size="9" color="darkred">\1</font>',
            text,
        )

        # Links: [text](url) - convert to text with URL annotation
        def link_replacer(match):
            link_text = match.group(1)
            url = match.group(2)
            return f'<link href="{url}" color="blue"><u>{link_text}</u></link>'

        text = re.sub(r"\[([^\]]+?)\]\(([^)]+?)\)", link_replacer, text)

        # Strikethrough: ~~text~~
        text = re.sub(r"~~(.*?)~~", r"<strike>\1</strike>", text)

        return text

    def parse_document(
        self,
        file_path: Union[str, Path],
        method: str = "auto",
        output_dir: Optional[str] = None,
        lang: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Abstract method to parse a document.
        Must be implemented by subclasses.

        Args:
            file_path: Path to the file to be parsed
            method: Parsing method (auto, txt, ocr)
            output_dir: Output directory path
            lang: Document language for OCR optimization
            **kwargs: Additional parameters for parser-specific command

        Returns:
            List[Dict[str, Any]]: List of content blocks
        """
        raise NotImplementedError("parse_document must be implemented by subclasses")

    def check_installation(self) -> bool:
        """
        Abstract method to check if the parser is properly installed.
        Must be implemented by subclasses.

        Returns:
            bool: True if installation is valid, False otherwise
        """
        raise NotImplementedError("check_installation must be implemented by subclasses")


class MineruParser(Parser):
    """
    MinerU 2.0 document parsing utility class

    Supports parsing PDF and image documents, converting the content into structured data
    and generating markdown and JSON output.

    Note: Office documents are no longer directly supported. Please convert them to PDF first.
    """

    def __init__(self) -> None:
        """Initialize MineruParser"""
        super().__init__()

    @staticmethod
    def _run_mineru_command(
        input_path: Union[str, Path],
        output_dir: Union[str, Path],
        method: str = "auto",
        lang: Optional[str] = None,
        backend: str = "pipeline",
        start_page: Optional[int] = None,
        end_page: Optional[int] = None,
        formula: bool = True,
        table: bool = True,
        device: Optional[str] = None,
        source: str = "huggingface",
        vlm_url: Optional[str] = None,
    ) -> None:
        """
        Run mineru command line tool

        Args:
            input_path: Path to input file or directory
            output_dir: Output directory path
            method: Parsing method (auto, txt, ocr)
            lang: Document language for OCR optimization
            backend: Parsing backend
            start_page: Starting page number (0-based)
            end_page: Ending page number (0-based)
            formula: Enable formula parsing
            table: Enable table parsing
            device: Inference device
            source: Model source
            vlm_url: When the backend is `vlm-sglang-client`, you need to specify the server_url
        """
        cmd = [
            "mineru",
            "-p",
            str(input_path),
            "-o",
            str(output_dir),
            "-m",
            method,
            "-b",
            backend,
            "--source",
            source,
        ]

        if lang:
            cmd.extend(["-l", lang])
        if start_page is not None:
            cmd.extend(["-s", str(start_page)])
        if end_page is not None:
            cmd.extend(["-e", str(end_page)])
        if not formula:
            cmd.extend(["-f", "false"])
        if not table:
            cmd.extend(["-t", "false"])
        if device:
            cmd.extend(["-d", device])
        if vlm_url:
            cmd.extend(["-u", vlm_url])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
                errors="ignore",
            )
            print("MinerU command executed successfully")
            if result.stdout:
                print(f"Output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error running mineru command: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
            raise
        except FileNotFoundError:
            raise RuntimeError(
                "mineru command not found. Please ensure MinerU 2.0 is properly installed:\n"
                "pip install -U 'mineru[core]' or uv pip install -U 'mineru[core]'"
            )

    @staticmethod
    def _read_output_files(
        output_dir: Path, file_stem: str, method: str = "auto"
    ) -> Tuple[List[Dict[str, Any]], str]:
        """
        Read the output files generated by mineru

        Args:
            output_dir: Output directory
            file_stem: File name without extension

        Returns:
            Tuple containing (content list JSON, Markdown text)
        """
        # Look for the generated files
        md_file = output_dir / f"{file_stem}.md"
        json_file = output_dir / f"{file_stem}_content_list.json"

        # Check for files in subdirectory (MinerU 2.0 may create subdirectories)
        subdir = output_dir / file_stem
        if subdir.exists():
            md_file = subdir / method / f"{file_stem}.md"
            json_file = subdir / method / f"{file_stem}_content_list.json"

        # Read markdown content
        md_content = ""
        if md_file.exists():
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    md_content = f.read()
            except Exception as e:
                print(f"Warning: Could not read markdown file {md_file}: {e}")

        # Read JSON content list
        content_list = []
        if json_file.exists():
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    content_list = json.load(f)
            except Exception as e:
                print(f"Warning: Could not read JSON file {json_file}: {e}")

        return content_list, md_content

    def parse_pdf(
        self,
        pdf_path: Union[str, Path],
        output_dir: Optional[str] = None,
        method: str = "auto",
        lang: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Parse PDF document using MinerU 2.0

        Args:
            pdf_path: Path to the PDF file
            output_dir: Output directory path
            method: Parsing method (auto, txt, ocr)
            lang: Document language for OCR optimization
            **kwargs: Additional parameters for mineru command

        Returns:
            List[Dict[str, Any]]: List of content blocks
        """
        try:
            # Convert to Path object for easier handling
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file does not exist: {pdf_path}")

            name_without_suff = pdf_path.stem

            # Prepare output directory
            if output_dir:
                base_output_dir = Path(output_dir)
            else:
                base_output_dir = pdf_path.parent / "mineru_output"

            base_output_dir.mkdir(parents=True, exist_ok=True)

            # Run mineru command
            self._run_mineru_command(
                input_path=pdf_path,
                output_dir=base_output_dir,
                method=method,
                lang=lang,
                **kwargs,
            )

            # Read the generated output files
            content_list, _ = self._read_output_files(
                base_output_dir, name_without_suff, method=method
            )
            return content_list

        except Exception as e:
            print(f"Error in parse_pdf: {str(e)}")
            raise

    def parse_image(
        self,
        image_path: Union[str, Path],
        output_dir: Optional[str] = None,
        lang: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Parse image document using MinerU 2.0

        Note: MinerU 2.0 natively supports .png, .jpeg, .jpg formats.
        Other formats (.bmp, .tiff, .tif, etc.) will be automatically converted to .png.

        Args:
            image_path: Path to the image file
            output_dir: Output directory path
            lang: Document language for OCR optimization
            **kwargs: Additional parameters for mineru command

        Returns:
            List[Dict[str, Any]]: List of content blocks
        """
        try:
            # Convert to Path object for easier handling
            image_path = Path(image_path)
            if not image_path.exists():
                raise FileNotFoundError(f"Image file does not exist: {image_path}")

            # Supported image formats by MinerU 2.0
            mineru_supported_formats = {".png", ".jpeg", ".jpg"}

            # All supported image formats (including those we can convert)
            all_supported_formats = {
                ".png",
                ".jpeg",
                ".jpg",
                ".bmp",
                ".tiff",
                ".tif",
                ".gif",
                ".webp",
            }

            ext = image_path.suffix.lower()
            if ext not in self.IMAGE_FORMATS:
                raise ValueError(
                    f"Unsupported image format: {ext}. Supported formats: {', '.join(self.IMAGE_FORMATS)}"
                )

            # Determine the actual image file to process
            actual_image_path = image_path
            temp_converted_file = None

            # If format is not natively supported by MinerU, convert it
            if ext not in mineru_supported_formats:
                print(f"Converting {ext} image to PNG for MinerU compatibility...")

                try:
                    from PIL import Image
                except ImportError:
                    raise RuntimeError(
                        "PIL/Pillow is required for image format conversion. "
                        "Please install it using: pip install Pillow"
                    )

                # Create temporary directory for conversion
                temp_dir = Path(tempfile.mkdtemp())
                temp_converted_file = temp_dir / f"{image_path.stem}_converted.png"

                try:
                    # Open and convert image
                    with Image.open(image_path) as img:
                        # Handle different image modes
                        if img.mode in ("RGBA", "LA", "P"):
                            # For images with transparency or palette, convert to RGB first
                            if img.mode == "P":
                                img = img.convert("RGBA")

                            # Create white background for transparent images
                            background = Image.new("RGB", img.size, (255, 255, 255))
                            if img.mode == "RGBA":
                                background.paste(
                                    img, mask=img.split()[-1]
                                )  # Use alpha channel as mask
                            else:
                                background.paste(img)
                            img = background
                        elif img.mode not in ("RGB", "L"):
                            # Convert other modes to RGB
                            img = img.convert("RGB")

                        # Save as PNG
                        img.save(temp_converted_file, "PNG", optimize=True)
                        print(
                            f"Successfully converted {image_path.name} to PNG ({temp_converted_file.stat().st_size / 1024:.1f} KB)"
                        )

                        actual_image_path = temp_converted_file

                except Exception as e:
                    if temp_converted_file and temp_converted_file.exists():
                        temp_converted_file.unlink()
                    raise RuntimeError(
                        f"Failed to convert image {image_path.name}: {str(e)}"
                    )

            name_without_suff = image_path.stem

            # Prepare output directory
            if output_dir:
                base_output_dir = Path(output_dir)
            else:
                base_output_dir = image_path.parent / "mineru_output"

            base_output_dir.mkdir(parents=True, exist_ok=True)

            try:
                # Run mineru command (images are processed with OCR method)
                self._run_mineru_command(
                    input_path=actual_image_path,
                    output_dir=base_output_dir,
                    method="ocr",  # Images require OCR method
                    lang=lang,
                    **kwargs,
                )

                # Read the generated output files
                content_list, _ = self._read_output_files(
                    base_output_dir, name_without_suff, method="ocr"
                )
                return content_list

            finally:
                # Clean up temporary converted file if it was created
                if temp_converted_file and temp_converted_file.exists():
                    try:
                        temp_converted_file.unlink()
                        temp_converted_file.parent.rmdir()  # Remove temp directory if empty
                    except Exception:
                        pass  # Ignore cleanup errors

        except Exception as e:
            print(f"Error in parse_image: {str(e)}")
            raise

    def parse_office_doc(
        self,
        doc_path: Union[str, Path],
        output_dir: Optional[str] = None,
        lang: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Parse office document by first converting to PDF, then parsing with MinerU 2.0

        Note: This method requires LibreOffice to be installed separately for PDF conversion.
        MinerU 2.0 no longer includes built-in Office document conversion.

        Supported formats: .doc, .docx, .ppt, .pptx, .xls, .xlsx

        Args:
            doc_path: Path to the document file (.doc, .docx, .ppt, .pptx, .xls, .xlsx)
            output_dir: Output directory path
            lang: Document language for OCR optimization
            **kwargs: Additional parameters for mineru command

        Returns:
            List[Dict[str, Any]]: List of content blocks
        """
        try:
            # Convert Office document to PDF using base class method
            pdf_path = self.convert_office_to_pdf(doc_path, output_dir)
            
            # Parse the converted PDF
            return self.parse_pdf(
                pdf_path=pdf_path, output_dir=output_dir, lang=lang, **kwargs
            )

        except Exception as e:
            print(f"Error in parse_office_doc: {str(e)}")
            raise

    def parse_text_file(
        self,
        text_path: Union[str, Path],
        output_dir: Optional[str] = None,
        lang: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Parse text file by first converting to PDF, then parsing with MinerU 2.0

        Supported formats: .txt, .md

        Args:
            text_path: Path to the text file (.txt, .md)
            output_dir: Output directory path
            lang: Document language for OCR optimization
            **kwargs: Additional parameters for mineru command

        Returns:
            List[Dict[str, Any]]: List of content blocks
        """
        try:
            # Convert text file to PDF using base class method
            pdf_path = self.convert_text_to_pdf(text_path, output_dir)
            
            # Parse the converted PDF
            return self.parse_pdf(
                pdf_path=pdf_path, output_dir=output_dir, lang=lang, **kwargs
            )

        except Exception as e:
            print(f"Error in parse_text_file: {str(e)}")
            raise

    def parse_document(
        self,
        file_path: Union[str, Path],
        method: str = "auto",
        output_dir: Optional[str] = None,
        lang: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Parse document using MinerU 2.0 based on file extension

        Args:
            file_path: Path to the file to be parsed
            method: Parsing method (auto, txt, ocr)
            output_dir: Output directory path
            lang: Document language for OCR optimization
            **kwargs: Additional parameters for mineru command

        Returns:
            List[Dict[str, Any]]: List of content blocks
        """
        # Convert to Path object
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")

        # Get file extension
        ext = file_path.suffix.lower()

        # Choose appropriate parser based on file type
        if ext == ".pdf":
            return self.parse_pdf(file_path, output_dir, method, lang, **kwargs)
        elif ext in self.IMAGE_FORMATS:
            return self.parse_image(file_path, output_dir, lang, **kwargs)
        elif ext in self.OFFICE_FORMATS:
            print(
                f"Warning: Office document detected ({ext}). "
                f"MinerU 2.0 requires conversion to PDF first."
            )
            return self.parse_office_doc(file_path, output_dir, lang, **kwargs)
        elif ext in self.TEXT_FORMATS:
            return self.parse_text_file(file_path, output_dir, lang, **kwargs)
        else:
            # For unsupported file types, try as PDF
            print(
                f"Warning: Unsupported file extension '{ext}', "
                f"attempting to parse as PDF"
            )
            return self.parse_pdf(file_path, output_dir, method, lang, **kwargs)

    def check_installation(self) -> bool:
        """
        Check if MinerU 2.0 is properly installed

        Returns:
            bool: True if installation is valid, False otherwise
        """
        try:
            result = subprocess.run(
                ["mineru", "--version"],
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
                errors="ignore",
            )
            print(f"MinerU version: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(
                "MinerU 2.0 is not properly installed. "
                "Please install it using: pip install -U 'mineru[core]'"
            )
            return False


class DoclingParser(Parser):
    """
    Docling document parsing utility class.
    
    Specialized in parsing Office documents and HTML files, converting the content 
    into structured data and generating markdown and JSON output.
    """
    
    # Define Docling-specific formats
    HTML_FORMATS = {".html", ".htm", ".xhtml"}
    
    def __init__(self) -> None:
        """Initialize DoclingParser"""
        super().__init__()
        
    def _run_docling_command(
        self,
        input_path: Union[str, Path],
        output_dir: Union[str, Path],
        **kwargs,
    ) -> None:
        """
        Run docling command line tool

        Args:
            input_path: Path to input file or directory
            output_dir: Output directory path
            method: Parsing method
            lang: Document language for optimization
            **kwargs: Additional parameters for docling command
        """
        cmd_json = [
            "docling",  
            "--output",
            str(output_dir),
            "--to",
            "json",
            str(input_path)
        ]
        cmd_md = [
            "docling",  
            "--output",
            str(output_dir),
            "--to",
            "md",
            str(input_path)
        ]

        try:
            result_json = subprocess.run(
                cmd_json,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
                errors="ignore",
            )
            result_md = subprocess.run(
                cmd_md,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
                errors="ignore",
            )
            print("Docling command executed successfully")
            if result_json.stdout:
                print(f"JSON cmd output: {result_json.stdout}")
            if result_md.stdout:
                print(f"Markdown cmd output: {result_md.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error running docling command: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
            raise
        except FileNotFoundError:
            raise RuntimeError(
                "docling command not found. Please ensure Docling is properly installed."
            )
            
    def _read_output_files(
        self,
        output_dir: Path,
        file_stem: str,
    ) -> Tuple[List[Dict[str, Any]], str]:
        """
        Read the output files generated by docling and convert to MinerU format

        Args:
            output_dir: Output directory
            file_stem: File name without extension

        Returns:
            Tuple containing (content list JSON, Markdown text)
        """
        md_file = output_dir / f"{file_stem}.md"
        json_file = output_dir / f"{file_stem}.json"

        # 读取markdown内容
        md_content = ""
        if md_file.exists():
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    md_content = f.read()
            except Exception as e:
                print(f"Warning: Could not read markdown file {md_file}: {e}")

        # 读取JSON内容并转换格式
        content_list = []
        if json_file.exists():
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    docling_content = json.load(f)
                    # 将docling格式转换为minerU格式
                    children = docling_content["body"]["children"]
                    cnt = 0
                    for child in children:
                        cnt += 1
                        tag = child["$ref"]
                        type = tag.split("/")[1]
                        num = tag.split("/")[2]
                        block = docling_content[type][int(num)]
                        if type != "groups":
                            content_list.append(self.read_from_block(block, type, num, output_dir, cnt))
                        else:
                            members = block["children"]
                            for member in members:
                                member_tag = member["$ref"]
                                member_type = member_tag.split("/")[1]
                                member_num = member_tag.split("/")[2]
                                member_block = docling_content[member_type][int(member_num)]
                                content_list.append(self.read_from_block(member_block, member_type, member_num, output_dir, cnt))
            except Exception as e:
                print(f"Warning: Could not read or convert JSON file {json_file}: {e}")
        return content_list, md_content
    
    def read_from_block(self, block, type: str, num: str, output_dir: Path, cnt: int) -> Dict[str, Any]:
        if type == "texts":
            if block["label"] == "formula":
                return {
                    "type": "equation",
                    "img_path": "",
                    "text": block["orig"],
                    "text_format": "unkown",
                    "page_idx": int(cnt)/10,
                }
            else:
                return {
                    "type": "text",
                    "text": block["orig"],
                    "page_idx": int(cnt)/10,
                }
        elif type == "pictures":
            try:
                base64_uri = block["image"]["uri"]
                base64_str = base64_uri.split(",")[1]
                image_dir = output_dir / "images"
                image_dir.mkdir(parents=True, exist_ok=True)  # 确保目录存在
                image_path = image_dir / f"image_{num}.png"
                with open(image_path, "wb") as f:
                    f.write(base64.b64decode(base64_str))
                return {
                    "type": "image",
                    "img_path": f"images/image_{num}.png",
                    "image_caption": block.get("caption", ""),
                    "image_footnote": block.get("footnote", ""),
                    "page_idx": int(cnt)/10,
                }
            except Exception as e:
                print(f"Warning: Failed to process image {num}: {e}")
                return {
                    "type": "text",
                    "text": f"[Image processing failed: {block.get('caption', '')}]",
                    "page_idx": int(cnt)/10,
                }
        else:
            try:
                return {
                    "type": "table",
                    "img_path": "",
                    "table_caption": block.get("caption", ""),
                    "table_footnote": block.get("footnote", ""),
                    "table_body": block.get("data", []),
                    "page_idx": int(cnt)/10,
                }
            except Exception as e:
                print(f"Warning: Failed to process table {num}: {e}")
                return {
                    "type": "text",
                    "text": f"[Table processing failed: {block.get('caption', '')}]",
                    "page_idx": int(cnt)/10,
                }

    
    def parse_office_doc(
        self,
        doc_path: Union[str, Path],
        output_dir: Optional[str] = None,
        lang: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Parse office document directly using Docling
        
        Supported formats: .doc, .docx, .ppt, .pptx, .xls, .xlsx

        Args:
            doc_path: Path to the document file
            output_dir: Output directory path
            lang: Document language for optimization
            **kwargs: Additional parameters for docling command

        Returns:
            List[Dict[str, Any]]: List of content blocks
        """
        try:
            # 转换为Path对象
            doc_path = Path(doc_path)
            if not doc_path.exists():
                raise FileNotFoundError(f"Document file does not exist: {doc_path}")

            if doc_path.suffix.lower() not in self.OFFICE_FORMATS:
                raise ValueError(f"Unsupported office format: {doc_path.suffix}")

            name_without_suff = doc_path.stem

            # 准备输出目录
            if output_dir:
                base_output_dir = Path(output_dir)
            else:
                base_output_dir = doc_path.parent / "docling_output"

            base_output_dir.mkdir(parents=True, exist_ok=True)

            # 运行docling命令
            self._run_docling_command(
                input_path=doc_path,
                output_dir=base_output_dir,
                **kwargs,
            )

            # 读取生成的输出文件
            content_list, _ = self._read_output_files(base_output_dir, name_without_suff)
            return content_list

        except Exception as e:
            print(f"Error in parse_office_doc: {str(e)}")
            raise
            
    def parse_html(
        self,
        html_path: Union[str, Path],
        output_dir: Optional[str] = None,
        lang: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Parse HTML document using Docling
        
        Supported formats: .html, .htm, .xhtml

        Args:
            html_path: Path to the HTML file
            output_dir: Output directory path
            lang: Document language for optimization
            **kwargs: Additional parameters for docling command

        Returns:
            List[Dict[str, Any]]: List of content blocks
        """
        try:
            # 转换为Path对象
            html_path = Path(html_path)
            if not html_path.exists():
                raise FileNotFoundError(f"HTML file does not exist: {html_path}")

            if html_path.suffix.lower() not in self.HTML_FORMATS:
                raise ValueError(f"Unsupported HTML format: {html_path.suffix}")

            name_without_suff = html_path.stem

            # 准备输出目录
            if output_dir:
                base_output_dir = Path(output_dir)
            else:
                base_output_dir = html_path.parent / "docling_output"

            base_output_dir.mkdir(parents=True, exist_ok=True)

            # 运行docling命令
            self._run_docling_command(
                input_path=html_path,
                output_dir=base_output_dir,
                **kwargs,
            )

            # 读取生成的输出文件
            content_list, _ = self._read_output_files(base_output_dir, name_without_suff)
            return content_list

        except Exception as e:
            print(f"Error in parse_html: {str(e)}")
            raise
            
    def parse_document(
        self,
        file_path: Union[str, Path],
        method: str = "auto",
        output_dir: Optional[str] = None,
        lang: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Parse document using Docling based on file extension

        Args:
            file_path: Path to the file to be parsed
            method: Parsing method
            output_dir: Output directory path
            lang: Document language for optimization
            **kwargs: Additional parameters for docling command

        Returns:
            List[Dict[str, Any]]: List of content blocks
        """
        # 转换为Path对象
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")

        # 获取文件扩展名
        ext = file_path.suffix.lower()

        # 根据文件类型选择合适的解析器
        if ext in self.OFFICE_FORMATS:
            return self.parse_office_doc(file_path, output_dir, lang, **kwargs)
        elif ext in self.HTML_FORMATS:
            return self.parse_html(file_path, output_dir, lang, **kwargs)
        else:
            raise ValueError(
                f"Unsupported file format: {ext}. "
                f"Docling only supports Office formats ({', '.join(self.OFFICE_FORMATS)}) "
                f"and HTML formats ({', '.join(self.HTML_FORMATS)})"
            )
            
    def check_installation(self) -> bool:
        """
        Check if Docling is properly installed

        Returns:
            bool: True if installation is valid, False otherwise
        """
        try:
            result = subprocess.run(
                ["docling", "--version"],
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
                errors="ignore",
            )
            print(f"Docling version: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(
                "Docling is not properly installed. "
                "Please ensure it is installed correctly."
            )
            return False


def main():
    """
    Main function to run the MinerU 2.0 parser from command line
    """
    parser = argparse.ArgumentParser(description="Parse documents using MinerU 2.0")
    parser.add_argument("file_path", help="Path to the document to parse")
    parser.add_argument("--output", "-o", help="Output directory path")
    parser.add_argument(
        "--method",
        "-m",
        choices=["auto", "txt", "ocr"],
        default="auto",
        help="Parsing method (auto, txt, ocr)",
    )
    parser.add_argument(
        "--lang",
        "-l",
        help="Document language for OCR optimization (e.g., ch, en, ja)",
    )
    parser.add_argument(
        "--backend",
        "-b",
        choices=[
            "pipeline",
            "vlm-transformers",
            "vlm-sglang-engine",
            "vlm-sglang-client",
        ],
        default="pipeline",
        help="Parsing backend",
    )
    parser.add_argument(
        "--device",
        "-d",
        help="Inference device (e.g., cpu, cuda, cuda:0, npu, mps)",
    )
    parser.add_argument(
        "--source",
        choices=["huggingface", "modelscope", "local"],
        default="huggingface",
        help="Model source",
    )
    parser.add_argument(
        "--no-formula",
        action="store_true",
        help="Disable formula parsing",
    )
    parser.add_argument(
        "--no-table",
        action="store_true",
        help="Disable table parsing",
    )
    parser.add_argument(
        "--stats", action="store_true", help="Display content statistics"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check MinerU installation",
    )
    parser.add_argument(
        "--parser",
        choices=["mineru", "docling"],
        default="mineru",
        help="Parser selection",
    )
    parser.add_argument(
        "--vlm_url",
        help="When the backend is `vlm-sglang-client`, you need to specify the server_url, for example:`http://127.0.0.1:30000`",
    )

    args = parser.parse_args()

    # Check installation if requested
    if args.check:
        if MineruParser.check_installation():
            print("✅ MinerU 2.0 is properly installed")
            return 0
        else:
            print("❌ MinerU 2.0 installation check failed")
            return 1

    try:
        # Parse the document
        doc_parser = DoclingParser() if args.parser == "docling" else MineruParser()
        content_list = doc_parser.parse_document(
            file_path=args.file_path,
            method=args.method,
            output_dir=args.output,
            lang=args.lang,
            backend=args.backend,
            device=args.device,
            source=args.source,
            formula=not args.no_formula,
            table=not args.no_table,
            vlm_url=args.vlm_url,
        )

        print(f"✅ Successfully parsed: {args.file_path}")
        print(f"📊 Extracted {len(content_list)} content blocks")

        # Display statistics if requested
        if args.stats:
            print("\n📈 Document Statistics:")
            print(f"Total content blocks: {len(content_list)}")

            # Count different types of content
            content_types = {}
            for item in content_list:
                if isinstance(item, dict):
                    content_type = item.get("type", "unknown")
                    content_types[content_type] = content_types.get(content_type, 0) + 1

            if content_types:
                print("\n📋 Content Type Distribution:")
                for content_type, count in sorted(content_types.items()):
                    print(f"  • {content_type}: {count}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
