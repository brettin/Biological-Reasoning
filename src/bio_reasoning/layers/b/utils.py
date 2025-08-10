import base64
import urllib.parse
from io import BytesIO
from pathlib import Path
from typing import Union

from PIL import Image


def _image_to_base64(image_bytes: bytes) -> str:
    """Convert raw image bytes to base64 encoded WebP string.

    Args:
        image_bytes: Raw image data.

    Returns:
        Base64 encoded WebP string with alpha channel applied if present.

    Raises:
        ValueError: If image format is invalid.
        IOError: If image processing fails.
    """
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            # Convert RGBA to RGB with alpha applied
            if img.mode == "RGBA":
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])  # Apply alpha channel
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Save as WebP with 85% quality
            buffered = BytesIO()
            img.save(
                buffered, format="WEBP", quality=85, method=6
            )  # Default compression method

            return base64.b64encode(buffered.getvalue()).decode("utf-8")

    except Image.UnidentifiedImageError as e:
        raise ValueError(f"Invalid image format: {e}")
    except Exception as e:
        raise IOError(f"Failed to process image: {e}")


def _load_file_from_uri(uri: str) -> Union[bytes, str]:
    """Load raw image data from either local path or remote URL.

    Args:
        uri: The image location (file path or URL).

    Returns:
        Raw image bytes for local files, or the original URL string for remote resources.

    Raises:
        ValueError: If URI scheme is not supported.
        IOError: If file cannot be loaded.
    """
    parsed = urllib.parse.urlparse(uri)

    if not parsed.scheme:  # Assume local file if no scheme
        uri = f"file://{Path(uri).absolute()}"
        parsed = urllib.parse.urlparse(uri)

    if parsed.scheme not in ("http", "https", "file"):
        raise ValueError(f"Unsupported URI scheme: {parsed.scheme}")

    if parsed.scheme == "file":
        try:
            with open(parsed.path, "rb") as f:
                raw_image = f.read()
                return _image_to_base64(raw_image)
        except Exception as e:
            raise IOError(f"Failed to load local file: {e}")
    else:  # Remote URL
        return uri  # Return original URL for remote resources


def load_image_data(uri: str) -> str:
    """Load image data and return either as base64 encoded string (for local files)
    or direct URL (for remote resources).

    Args:
        uri: Image URI (file path or URL)

    Returns:
        Either a base64 encoded string (local files) or direct URL (remote resources)
    """
    result = _load_file_from_uri(uri)
    if isinstance(result, bytes):  # Local file
        return f"data:image/jpeg;base64,{_image_to_base64(result)}"
    return result  # Remote URL
