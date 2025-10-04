"""
Document management endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import os
import hashlib
import shutil
from pathlib import Path

from ....core.database import get_db
from ....core.security import get_current_user
from ....models.user import User
from ....models.document import Document
from ....schemas.document import (
    Document as DocumentSchema,
    DocumentCreate,
    DocumentUpdate,
    FileUploadResponse,
    DocumentSearch
)
from ....core.config import settings

router = APIRouter()

def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    is_public: bool = Form(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a new document
    """
    # Create uploads directory if it doesn't exist
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{current_user.id}_{title}_{hashlib.md5(file.filename.encode()).hexdigest()}{file_extension}"
    file_path = upload_dir / unique_filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Calculate file hash and size
    file_hash = calculate_file_hash(str(file_path))
    file_size = file_path.stat().st_size
    
    # Create database record
    db_document = Document(
        title=title,
        description=description,
        filename=unique_filename,
        original_filename=file.filename,
        file_path=str(file_path),
        file_size=file_size,
        mime_type=file.content_type or "application/octet-stream",
        file_hash=file_hash,
        category=category,
        tags=tags,
        is_public=is_public,
        owner_id=current_user.id
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return FileUploadResponse(
        message="File uploaded successfully",
        document_id=db_document.id,
        filename=unique_filename,
        file_size=file_size
    )

@router.get("/", response_model=List[DocumentSchema])
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get documents accessible to current user
    """
    query = db.query(Document)
    
    # Non-admin users can only see their own documents and public documents
    if not current_user.is_superuser:
        query = query.filter(
            (Document.owner_id == current_user.id) | (Document.is_public == True)
        )
    
    documents = query.offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=DocumentSchema)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get document by ID
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check permissions
    if (document.owner_id != current_user.id and 
        not document.is_public and 
        not current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return document

@router.put("/{document_id}", response_model=DocumentSchema)
async def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update document metadata
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check permissions (only owner or admin can update)
    if document.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update fields
    update_data = document_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(document, field, value)
    
    db.commit()
    db.refresh(document)
    
    return document

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete document
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check permissions (only owner or admin can delete)
    if document.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Delete file from filesystem
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}