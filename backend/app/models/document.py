"""
Document model for file management
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, BigInteger, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # File information
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger, nullable=False)  # Size in bytes
    mime_type = Column(String(100), nullable=False)
    file_hash = Column(String(64), nullable=False, index=True)  # SHA-256 hash
    
    # Content and OCR
    extracted_text = Column(Text, nullable=True)  # OCR extracted text
    ocr_confidence = Column(Integer, nullable=True)  # OCR confidence score (0-100)
    
    # Metadata
    tags = Column(Text, nullable=True)  # JSON string of tags
    category = Column(String(100), nullable=True)
    language = Column(String(10), default="en")
    
    # Status and flags
    is_processed = Column(Boolean, default=False)  # OCR processing status
    is_public = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document")
    
    def __repr__(self):
        return f"<Document(id={self.id}, title='{self.title}')>"

class DocumentVersion(Base):
    __tablename__ = "document_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    version_number = Column(Integer, nullable=False)
    
    # File information for this version
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    file_hash = Column(String(64), nullable=False)
    
    # Version metadata
    change_description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign keys
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    document = relationship("Document", back_populates="versions")
    created_by = relationship("User")
    
    def __repr__(self):
        return f"<DocumentVersion(id={self.id}, version={self.version_number})>"