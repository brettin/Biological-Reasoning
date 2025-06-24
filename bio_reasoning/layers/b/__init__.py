"""
Layer B consists of bespoke foundation models specialized for non-textual or multimodal data (e.g. genomic sequences, protein structures, images) that interface with the LLM.
"""

from .visual_describer import visual_describer_factory
from .utils import load_image_data

__all__ = [
    "visual_describer_factory",
    # utils
    "load_image_data",
]
