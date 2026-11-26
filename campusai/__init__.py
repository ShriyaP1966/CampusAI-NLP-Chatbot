"""CampusAI: grounded question answering over campus documents."""

from campusai.documents import Chunk, load_chunks
from campusai.engine import Answer, CampusAI, Source

__version__ = "1.0.0"

__all__ = ["Answer", "CampusAI", "Chunk", "Source", "load_chunks", "__version__"]
