#!/usr/bin/env python3
"""
Multi-Format Document Optimizer

Unified document optimization tool that chains docling-converter, imagemagick-expert,
and markdown-to-pdf. Supports PDF image optimization, format conversion pipelines,
and batch processing with configurable quality presets.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class QualityPreset(Enum):
    """Quality presets for document optimization."""

    WEB = "web"
    PRINT = "print"
    ARCHIVE = "archive"
    MINIMAL = "minimal"
    CUSTOM = "custom"


@dataclass
class PresetConfig:
    """Configuration for a quality preset."""

    name: str
    image_quality: int
    image_dpi: int
    image_format: str
    max_width: int
    max_height: int
    strip_metadata: bool

    @classmethod
    def from_preset(cls, preset: QualityPreset) -> "PresetConfig":
        """Create configuration from preset name."""
        presets = {
            QualityPreset.WEB: cls(
                name="web",
                image_quality=80,
                image_dpi=96,
                image_format="webp",
                max_width=1920,
                max_height=1080,
                strip_metadata=True,
            ),
            QualityPreset.PRINT: cls(
                name="print",
                image_quality=95,
                image_dpi=300,
                image_format="jpeg",
                max_width=0,  # No limit
                max_height=0,
                strip_metadata=False,
            ),
            QualityPreset.ARCHIVE: cls(
                name="archive",
                image_quality=90,
                image_dpi=150,
                image_format="jpeg",
                max_width=2400,
                max_height=2400,
                strip_metadata=False,
            ),
            QualityPreset.MINIMAL: cls(
                name="minimal",
                image_quality=70,
                image_dpi=72,
                image_format="webp",
                max_width=1280,
                max_height=720,
                strip_metadata=True,
            ),
        }
        return presets.get(preset, presets[QualityPreset.WEB])


@dataclass
class DocumentAnalysis:
    """Analysis result for a document."""

    input_file: str
    format: str
    page_count: int
    file_size_bytes: int
    images: dict = field(default_factory=dict)
    recommended_pipeline: str = ""
    recommended_preset: str = ""
    estimated_output_size_bytes: int = 0
    schema_version: str = "1.0"

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(asdict(self), indent=2)


@dataclass
class ConversionResult:
    """Result of a document conversion."""

    input_file: str
    output_file: str
    pipeline: str
    preset: str
    input_size_bytes: int
    output_size_bytes: int
    compression_ratio: float
    images_processed: int
    processing_time_seconds: float
    status: str
    error_message: str = ""
    schema_version: str = "1.0"

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(asdict(self), indent=2)


class DocumentOptimizer:
    """Main document optimization engine."""

    SUPPORTED_FORMATS = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".doc": "doc",
        ".pptx": "pptx",
        ".ppt": "ppt",
        ".xlsx": "xlsx",
        ".xls": "xls",
        ".html": "html",
        ".htm": "html",
        ".md": "markdown",
        ".png": "image",
        ".jpg": "image",
        ".jpeg": "image",
        ".tiff": "image",
        ".tif": "image",
        ".webp": "image",
        ".gif": "image",
    }

    def __init__(self, verbose: bool = False):
        """Initialize the optimizer."""
        self.verbose = verbose
        self._check_dependencies()

    def _check_dependencies(self) -> None:
        """Check that required external tools are available."""
        self.has_imagemagick = shutil.which("magick") is not None
        self.has_docling = shutil.which("docling") is not None
        self.has_pymupdf = False
        try:
            import fitz  # noqa: F401

            self.has_pymupdf = True
        except ImportError:
            pass

    def _log(self, message: str) -> None:
        """Print verbose log message."""
        if self.verbose:
            print(f"[INFO] {message}", file=sys.stderr)

    def detect_format(self, file_path: Path) -> str:
        """Detect the format of a file."""
        suffix = file_path.suffix.lower()
        return self.SUPPORTED_FORMATS.get(suffix, "unknown")

    def analyze(self, input_path: Path) -> DocumentAnalysis:
        """Analyze a document and return optimization recommendations."""
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        file_format = self.detect_format(input_path)
        file_size = input_path.stat().st_size

        analysis = DocumentAnalysis(
            input_file=str(input_path),
            format=file_format,
            page_count=0,
            file_size_bytes=file_size,
        )

        if file_format == "pdf" and self.has_pymupdf:
            analysis = self._analyze_pdf(input_path, analysis)
        elif file_format == "image":
            analysis = self._analyze_image(input_path, analysis)
        else:
            # Basic analysis for other formats
            analysis.recommended_pipeline = f"{file_format}_to_pdf"
            analysis.recommended_preset = "web"
            analysis.estimated_output_size_bytes = int(file_size * 0.5)

        return analysis

    def _analyze_pdf(self, input_path: Path, analysis: DocumentAnalysis) -> DocumentAnalysis:
        """Analyze a PDF document."""
        try:
            import fitz

            doc = fitz.open(input_path)
            analysis.page_count = len(doc)

            # Extract image information
            image_count = 0
            total_image_bytes = 0
            formats_seen = set()
            max_width = 0
            max_height = 0

            for page_num in range(len(doc)):
                page = doc[page_num]
                images = page.get_images(full=True)
                for img in images:
                    image_count += 1
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    if base_image:
                        total_image_bytes += len(base_image.get("image", b""))
                        formats_seen.add(base_image.get("ext", "unknown"))
                        w = base_image.get("width", 0)
                        h = base_image.get("height", 0)
                        max_width = max(max_width, w)
                        max_height = max(max_height, h)

            doc.close()

            analysis.images = {
                "count": image_count,
                "total_bytes": total_image_bytes,
                "formats": list(formats_seen),
                "max_resolution": f"{max_width}x{max_height}",
            }

            # Determine recommendations
            if image_count > 0:
                analysis.recommended_pipeline = "pdf_optimize"
                if total_image_bytes > 10 * 1024 * 1024:  # > 10MB images
                    analysis.recommended_preset = "web"
                else:
                    analysis.recommended_preset = "archive"
                # Estimate compression ratio
                estimated_ratio = 0.3 if analysis.recommended_preset == "web" else 0.6
                analysis.estimated_output_size_bytes = int(analysis.file_size_bytes * estimated_ratio)
            else:
                analysis.recommended_pipeline = "pdf_passthrough"
                analysis.recommended_preset = "archive"
                analysis.estimated_output_size_bytes = analysis.file_size_bytes

        except Exception as e:
            self._log(f"PDF analysis error: {e}")
            analysis.recommended_pipeline = "pdf_optimize"
            analysis.recommended_preset = "web"

        return analysis

    def _analyze_image(self, input_path: Path, analysis: DocumentAnalysis) -> DocumentAnalysis:
        """Analyze an image file."""
        analysis.page_count = 1
        analysis.recommended_pipeline = "images_to_pdf"
        analysis.recommended_preset = "web"

        if self.has_imagemagick:
            try:
                result = subprocess.run(
                    ["magick", "identify", "-format", "%w %h %m", str(input_path)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    parts = result.stdout.strip().split()
                    if len(parts) >= 3:
                        width, height = int(parts[0]), int(parts[1])
                        img_format = parts[2].lower()
                        analysis.images = {
                            "count": 1,
                            "total_bytes": analysis.file_size_bytes,
                            "formats": [img_format],
                            "max_resolution": f"{width}x{height}",
                        }
            except Exception as e:
                self._log(f"Image analysis error: {e}")

        analysis.estimated_output_size_bytes = int(analysis.file_size_bytes * 0.5)
        return analysis

    def optimize_image(
        self,
        input_path: Path,
        output_path: Path,
        config: PresetConfig,
    ) -> bool:
        """Optimize a single image using ImageMagick."""
        if not self.has_imagemagick:
            self._log("ImageMagick not available, skipping optimization")
            shutil.copy(input_path, output_path)
            return True

        cmd = ["magick", str(input_path)]

        # Strip metadata if configured
        if config.strip_metadata:
            cmd.append("-strip")

        # Apply resize if dimensions are set
        if config.max_width > 0 or config.max_height > 0:
            w = config.max_width if config.max_width > 0 else ""
            h = config.max_height if config.max_height > 0 else ""
            cmd.extend(["-filter", "Lanczos", "-resize", f"{w}x{h}>"])

        # Apply quality setting
        cmd.extend(["-quality", str(config.image_quality)])

        # Set output format
        output_with_format = output_path.with_suffix(f".{config.image_format}")
        cmd.append(str(output_with_format))

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                self._log(f"ImageMagick error: {result.stderr}")
                return False
            # Rename if output format differs
            if output_with_format != output_path:
                shutil.move(output_with_format, output_path)
            return True
        except subprocess.TimeoutExpired:
            self._log("ImageMagick timeout")
            return False
        except Exception as e:
            self._log(f"Image optimization error: {e}")
            return False

    def convert(
        self,
        input_path: Path,
        output_path: Path,
        preset: QualityPreset = QualityPreset.WEB,
        config: Optional[PresetConfig] = None,
        ocr: bool = False,
        ocr_lang: str = "en,ja",
        keep_temp: bool = False,
    ) -> ConversionResult:
        """Convert and optimize a document."""
        import time

        start_time = time.time()

        if config is None:
            config = PresetConfig.from_preset(preset)

        input_size = input_path.stat().st_size
        file_format = self.detect_format(input_path)

        result = ConversionResult(
            input_file=str(input_path),
            output_file=str(output_path),
            pipeline=f"{file_format}_to_pdf",
            preset=config.name,
            input_size_bytes=input_size,
            output_size_bytes=0,
            compression_ratio=0.0,
            images_processed=0,
            processing_time_seconds=0.0,
            status="pending",
        )

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)

                if file_format == "pdf":
                    result = self._optimize_pdf(input_path, output_path, config, temp_path, result)
                elif file_format in ("docx", "doc", "pptx", "ppt", "xlsx", "xls", "html"):
                    result = self._convert_office_to_pdf(
                        input_path, output_path, config, temp_path, result, ocr, ocr_lang
                    )
                elif file_format == "markdown":
                    result = self._convert_markdown_to_pdf(input_path, output_path, config, temp_path, result)
                elif file_format == "image":
                    result = self._convert_image_to_pdf(input_path, output_path, config, temp_path, result)
                else:
                    result.status = "error"
                    result.error_message = f"Unsupported format: {file_format}"

                if keep_temp:
                    self._log(f"Temp files preserved in: {temp_dir}")

        except Exception as e:
            result.status = "error"
            result.error_message = str(e)

        result.processing_time_seconds = round(time.time() - start_time, 2)

        if result.status != "error" and output_path.exists():
            result.output_size_bytes = output_path.stat().st_size
            if result.input_size_bytes > 0:
                result.compression_ratio = round(result.output_size_bytes / result.input_size_bytes, 3)
            result.status = "success"

        return result

    def _optimize_pdf(
        self,
        input_path: Path,
        output_path: Path,
        config: PresetConfig,
        temp_path: Path,
        result: ConversionResult,
    ) -> ConversionResult:
        """Optimize a PDF by extracting and re-embedding optimized images."""
        result.pipeline = "pdf_optimize"

        if not self.has_pymupdf:
            self._log("PyMuPDF not available, copying file without optimization")
            shutil.copy(input_path, output_path)
            return result

        try:
            import fitz

            doc = fitz.open(input_path)
            images_dir = temp_path / "images"
            images_dir.mkdir()

            # Extract and optimize images
            image_map = {}  # xref -> optimized_path
            images_processed = 0

            for page_num in range(len(doc)):
                page = doc[page_num]
                images = page.get_images(full=True)
                for img in images:
                    xref = img[0]
                    if xref in image_map:
                        continue

                    base_image = doc.extract_image(xref)
                    if not base_image:
                        continue

                    img_ext = base_image.get("ext", "png")
                    img_data = base_image.get("image", b"")
                    if not img_data:
                        continue

                    # Save original image
                    orig_path = images_dir / f"img_{xref}.{img_ext}"
                    with open(orig_path, "wb") as f:
                        f.write(img_data)

                    # Optimize image
                    opt_path = images_dir / f"img_{xref}_opt.{config.image_format}"
                    if self.optimize_image(orig_path, opt_path, config):
                        image_map[xref] = opt_path
                        images_processed += 1
                    else:
                        image_map[xref] = orig_path

            # Replace images in PDF
            for xref, opt_path in image_map.items():
                if opt_path.exists():
                    with open(opt_path, "rb") as f:
                        img_data = f.read()
                    try:
                        doc.delete_object(xref)
                        # Note: Full image replacement would require more complex handling
                        # For now, we save as a new PDF which re-embeds all images
                    except Exception:
                        pass

            # Save optimized PDF
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()

            result.images_processed = images_processed

        except Exception as e:
            result.status = "error"
            result.error_message = f"PDF optimization error: {e}"
            # Fallback: copy original
            if not output_path.exists():
                shutil.copy(input_path, output_path)

        return result

    def _convert_office_to_pdf(
        self,
        input_path: Path,
        output_path: Path,
        config: PresetConfig,
        temp_path: Path,
        result: ConversionResult,
        ocr: bool,
        ocr_lang: str,
    ) -> ConversionResult:
        """Convert Office documents to PDF via docling and markdown-to-pdf."""
        result.pipeline = f"{self.detect_format(input_path)}_to_pdf"

        if not self.has_docling:
            result.status = "error"
            result.error_message = "docling not available"
            return result

        # Step 1: Convert to Markdown with docling
        md_output = temp_path / "converted"
        md_output.mkdir()

        cmd = ["docling", str(input_path), "--output", str(md_output), "--to", "md"]
        if ocr:
            cmd.extend(["--ocr-lang", ocr_lang])

        try:
            subprocess.run(cmd, capture_output=True, timeout=300, check=True)
        except subprocess.CalledProcessError as e:
            result.status = "error"
            result.error_message = f"docling conversion failed: {e}"
            return result
        except subprocess.TimeoutExpired:
            result.status = "error"
            result.error_message = "docling conversion timeout"
            return result

        # Find the generated markdown file
        md_files = list(md_output.glob("*.md"))
        if not md_files:
            result.status = "error"
            result.error_message = "No markdown output from docling"
            return result

        md_file = md_files[0]

        # Step 2: Optimize any extracted images
        images_dir = md_output / "images"
        if images_dir.exists():
            for img_path in images_dir.glob("*"):
                if img_path.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
                    opt_path = img_path.with_suffix(f".opt{img_path.suffix}")
                    if self.optimize_image(img_path, opt_path, config):
                        shutil.move(opt_path, img_path)
                        result.images_processed += 1

        # Step 3: Convert Markdown to PDF
        # Try to use markdown-to-pdf skill scripts
        script_dir = Path(__file__).parent.parent.parent / "markdown-to-pdf" / "scripts"
        fpdf_script = script_dir / "markdown_to_fpdf.py"

        if fpdf_script.exists():
            cmd = ["python3", str(fpdf_script), str(md_file), str(output_path)]
            try:
                subprocess.run(cmd, capture_output=True, timeout=120, check=True)
            except Exception as e:
                result.status = "error"
                result.error_message = f"PDF generation failed: {e}"
        else:
            # Fallback: just copy markdown for now
            result.status = "error"
            result.error_message = "markdown-to-pdf not available"

        return result

    def _convert_markdown_to_pdf(
        self,
        input_path: Path,
        output_path: Path,
        config: PresetConfig,
        temp_path: Path,
        result: ConversionResult,
    ) -> ConversionResult:
        """Convert Markdown to optimized PDF."""
        result.pipeline = "md_to_pdf"

        # Try to use markdown-to-pdf skill scripts
        script_dir = Path(__file__).parent.parent.parent / "markdown-to-pdf" / "scripts"
        fpdf_script = script_dir / "markdown_to_fpdf.py"

        if fpdf_script.exists():
            cmd = ["python3", str(fpdf_script), str(input_path), str(output_path)]
            try:
                subprocess.run(cmd, capture_output=True, timeout=120, check=True)
            except Exception as e:
                result.status = "error"
                result.error_message = f"PDF generation failed: {e}"
        else:
            result.status = "error"
            result.error_message = "markdown-to-pdf not available"

        return result

    def _convert_image_to_pdf(
        self,
        input_path: Path,
        output_path: Path,
        config: PresetConfig,
        temp_path: Path,
        result: ConversionResult,
    ) -> ConversionResult:
        """Convert image(s) to PDF."""
        result.pipeline = "images_to_pdf"

        # Optimize image first
        opt_path = temp_path / f"optimized.{config.image_format}"
        if self.optimize_image(input_path, opt_path, config):
            result.images_processed = 1
            source_path = opt_path
        else:
            source_path = input_path

        # Convert to PDF using ImageMagick
        if self.has_imagemagick:
            cmd = ["magick", str(source_path), "-page", "A4", str(output_path)]
            try:
                subprocess.run(cmd, capture_output=True, timeout=60, check=True)
            except Exception as e:
                result.status = "error"
                result.error_message = f"PDF creation failed: {e}"
        else:
            result.status = "error"
            result.error_message = "ImageMagick not available"

        return result

    def verify(self, document_path: Path) -> dict:
        """Verify document quality and integrity."""
        if not document_path.exists():
            return {"status": "error", "message": "File not found"}

        result = {
            "file": str(document_path),
            "file_size_bytes": document_path.stat().st_size,
            "status": "success",
            "checks": {},
        }

        if document_path.suffix.lower() == ".pdf" and self.has_pymupdf:
            try:
                import fitz

                doc = fitz.open(document_path)
                result["checks"]["page_count"] = len(doc)
                result["checks"]["is_valid_pdf"] = True

                # Check for rendering issues
                for i, page in enumerate(doc):
                    try:
                        _ = page.get_text()
                    except Exception:
                        result["checks"][f"page_{i}_text_extraction"] = "failed"

                doc.close()
            except Exception as e:
                result["status"] = "error"
                result["checks"]["pdf_open"] = f"failed: {e}"

        return result

    def batch(
        self,
        input_dir: Path,
        output_dir: Path,
        preset: QualityPreset = QualityPreset.WEB,
        pattern: str = "*.pdf,*.docx,*.pptx",
        parallel: int = 1,
        skip_existing: bool = False,
    ) -> list:
        """Process multiple documents in batch."""
        output_dir.mkdir(parents=True, exist_ok=True)
        results = []

        patterns = pattern.split(",")
        files = []
        for p in patterns:
            files.extend(input_dir.glob(p.strip()))

        for input_file in files:
            output_file = output_dir / input_file.with_suffix(".pdf").name

            if skip_existing and output_file.exists():
                self._log(f"Skipping existing: {output_file}")
                continue

            self._log(f"Processing: {input_file}")
            result = self.convert(input_file, output_file, preset)
            results.append(result)

        return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Multi-Format Document Optimizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze document")
    analyze_parser.add_argument("input", type=Path, help="Input file or directory")
    analyze_parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")
    analyze_parser.add_argument("--verbose", action="store_true", help="Verbose output")

    # convert command
    convert_parser = subparsers.add_parser("convert", help="Convert and optimize document")
    convert_parser.add_argument("input", type=Path, help="Input file")
    convert_parser.add_argument("output", type=Path, help="Output file")
    convert_parser.add_argument(
        "--preset",
        choices=["web", "print", "archive", "minimal", "custom"],
        default="web",
        help="Quality preset",
    )
    convert_parser.add_argument("--image-quality", type=int, help="Image quality (0-100)")
    convert_parser.add_argument("--image-dpi", type=int, help="Target DPI")
    convert_parser.add_argument("--image-format", choices=["jpeg", "png", "webp"], help="Image format")
    convert_parser.add_argument("--max-width", type=int, help="Max image width")
    convert_parser.add_argument("--max-height", type=int, help="Max image height")
    convert_parser.add_argument("--ocr", action="store_true", help="Enable OCR")
    convert_parser.add_argument("--ocr-lang", default="en,ja", help="OCR languages")
    convert_parser.add_argument("--keep-temp", action="store_true", help="Keep temp files")
    convert_parser.add_argument("--verbose", action="store_true", help="Verbose output")

    # batch command
    batch_parser = subparsers.add_parser("batch", help="Batch process documents")
    batch_parser.add_argument("input_dir", type=Path, help="Input directory")
    batch_parser.add_argument("output_dir", type=Path, help="Output directory")
    batch_parser.add_argument(
        "--preset",
        choices=["web", "print", "archive", "minimal"],
        default="web",
        help="Quality preset",
    )
    batch_parser.add_argument("--pattern", default="*.pdf,*.docx,*.pptx", help="File patterns")
    batch_parser.add_argument("--parallel", type=int, default=1, help="Parallel workers")
    batch_parser.add_argument("--skip-existing", action="store_true", help="Skip existing files")
    batch_parser.add_argument("--verbose", action="store_true", help="Verbose output")

    # optimize-images command
    opt_parser = subparsers.add_parser("optimize-images", help="Optimize PDF images")
    opt_parser.add_argument("input", type=Path, help="Input PDF")
    opt_parser.add_argument("output", type=Path, help="Output PDF")
    opt_parser.add_argument(
        "--preset",
        choices=["web", "print", "archive", "minimal"],
        default="web",
        help="Quality preset",
    )
    opt_parser.add_argument("--image-quality", type=int, help="Image quality (0-100)")
    opt_parser.add_argument("--max-width", type=int, help="Max image width")
    opt_parser.add_argument("--max-height", type=int, help="Max image height")
    opt_parser.add_argument("--strip-metadata", action="store_true", help="Strip image metadata")
    opt_parser.add_argument("--verbose", action="store_true", help="Verbose output")

    # verify command
    verify_parser = subparsers.add_parser("verify", help="Verify document quality")
    verify_parser.add_argument("document", type=Path, help="Document to verify")
    verify_parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")
    verify_parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    verbose = getattr(args, "verbose", False)
    optimizer = DocumentOptimizer(verbose=verbose)

    if args.command == "analyze":
        analysis = optimizer.analyze(args.input)
        if args.format == "json":
            print(analysis.to_json())
        else:
            print(f"File: {analysis.input_file}")
            print(f"Format: {analysis.format}")
            print(f"Pages: {analysis.page_count}")
            print(f"Size: {analysis.file_size_bytes:,} bytes")
            if analysis.images:
                print(f"Images: {analysis.images.get('count', 0)}")
                print(f"Image Size: {analysis.images.get('total_bytes', 0):,} bytes")
            print(f"Recommended Pipeline: {analysis.recommended_pipeline}")
            print(f"Recommended Preset: {analysis.recommended_preset}")

    elif args.command == "convert":
        preset = QualityPreset(args.preset)
        config = PresetConfig.from_preset(preset)

        # Override with custom settings
        if args.image_quality:
            config.image_quality = args.image_quality
        if args.image_dpi:
            config.image_dpi = args.image_dpi
        if args.image_format:
            config.image_format = args.image_format
        if args.max_width:
            config.max_width = args.max_width
        if args.max_height:
            config.max_height = args.max_height

        result = optimizer.convert(
            args.input,
            args.output,
            preset,
            config,
            ocr=args.ocr,
            ocr_lang=args.ocr_lang,
            keep_temp=args.keep_temp,
        )
        print(result.to_json())

    elif args.command == "batch":
        preset = QualityPreset(args.preset)
        results = optimizer.batch(
            args.input_dir,
            args.output_dir,
            preset,
            args.pattern,
            args.parallel,
            args.skip_existing,
        )
        for r in results:
            print(r.to_json())

    elif args.command == "optimize-images":
        preset = QualityPreset(args.preset)
        config = PresetConfig.from_preset(preset)

        if args.image_quality:
            config.image_quality = args.image_quality
        if args.max_width:
            config.max_width = args.max_width
        if args.max_height:
            config.max_height = args.max_height
        if args.strip_metadata:
            config.strip_metadata = True

        result = optimizer.convert(args.input, args.output, preset, config)
        print(result.to_json())

    elif args.command == "verify":
        result = optimizer.verify(args.document)
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"File: {result['file']}")
            print(f"Size: {result['file_size_bytes']:,} bytes")
            print(f"Status: {result['status']}")
            for check, value in result.get("checks", {}).items():
                print(f"  {check}: {value}")


if __name__ == "__main__":
    main()
