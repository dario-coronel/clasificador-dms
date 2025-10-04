"""
Pydantic schemas for Document model validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Base Document schema
class DocumentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None  # JSON string of tags
    language: str = "en"
    is_public: bool = False

# Schema for creating a document
class DocumentCreate(DocumentBase):
    pass

# Schema for updating a document
class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    language: Optional[str] = None
    is_public: Optional[bool] = None
    is_archived: Optional[bool] = None

# Schema for document response
class Document(DocumentBase):
    id: int
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    extracted_text: Optional[str] = None
    ocr_confidence: Optional[int] = None
    is_processed: bool
    is_archived: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int

    class Config:
        from_attributes = True

# Schema for document with owner information
class DocumentWithOwner(Document):
    owner: "User"  # Forward reference

# Schema for document version
class DocumentVersionBase(BaseModel):
    change_description: Optional[str] = None

class DocumentVersionCreate(DocumentVersionBase):
    pass

class DocumentVersion(DocumentVersionBase):
    id: int
    version_number: int
    filename: str
    file_size: int
    file_hash: str
    created_at: datetime
    document_id: int
    created_by_id: int

    class Config:
        from_attributes = True

# Schema for file upload response
class FileUploadResponse(BaseModel):
    message: str
    document_id: int
    filename: str
    file_size: int

# Schema for search filters
class DocumentSearch(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    owner_id: Optional[int] = None
    is_public: Optional[bool] = None
    is_archived: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    tags: Optional[List[str]] = None