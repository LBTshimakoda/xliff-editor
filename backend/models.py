from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class XliffTag(BaseModel):
    """Represents an inline tag (like <g>, <x/>, <bpt>, <ept>, <ph>, etc.)"""
    tag_type: str  # 'g', 'x', 'bpt', 'ept', 'ph', 'it', 'mrk', etc.
    id: Optional[str] = None
    content: Optional[str] = None  # Inner content for tags like <bpt>&lt;b&gt;</bpt>
    attributes: Dict[str, str] = {}
    position: int  # Position in the segment
    ctype: Optional[str] = None  # Content type: bold, italic, image, etc.
    paired_with: Optional[str] = None  # For bpt/ept pairs

class SegmentContent(BaseModel):
    """Represents a segment's content with text and tags"""
    text: str  # The full text
    tags: List[XliffTag] = []  # Inline tags

class TransUnit(BaseModel):
    """Represents a single trans-unit"""
    id: str
    source: SegmentContent
    target: Optional[SegmentContent] = None
    state: Optional[str] = None  # translated, needs-review, etc.
    notes: List[str] = []
    attributes: Dict[str, Any] = {}

class XliffFile(BaseModel):
    """Represents a file element in XLIFF"""
    original: str
    source_language: str
    target_language: Optional[str] = None
    datatype: Optional[str] = None
    trans_units: List[TransUnit] = []

class XliffDocument(BaseModel):
    """Represents the entire XLIFF document"""
    version: str
    files: List[XliffFile] = []
    
class TransUnitUpdate(BaseModel):
    """For updating a trans-unit's target"""
    file_index: int
    trans_unit_id: str
    target_text: str
    target_tags: List[XliffTag] = []