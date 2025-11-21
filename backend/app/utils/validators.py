from fastapi import HTTPException, UploadFile
import re

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = ["application/pdf"]
MAX_SEARCH_QUERY_LENGTH = 200
MAX_PDF_PAGES = 50

def validate_pdf_file(file: UploadFile) -> None:
    """Validate uploaded PDF file"""
    # Check content type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only PDF files are allowed. Received: {file.content_type}"
        )
    
    # Check filename
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="File must have .pdf extension"
        )
    
    # Sanitize filename to prevent path traversal
    if '..' in file.filename or '/' in file.filename or '\\' in file.filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )

def validate_search_query(query: str) -> str:
    """Validate and sanitize search query"""
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    query = query.strip()
    
    if len(query) > MAX_SEARCH_QUERY_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Search query too long. Maximum {MAX_SEARCH_QUERY_LENGTH} characters"
        )
    
    # Remove potentially dangerous characters
    query = re.sub(r'[<>]', '', query)
    
    return query

def validate_job_id(job_id: str) -> str:
    """Validate job ID format"""
    if not job_id or not job_id.strip():
        raise HTTPException(status_code=400, detail="Job ID cannot be empty")
    
    job_id = job_id.strip()
    
    # Job IDs should be alphanumeric with possible hyphens/underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', job_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID format"
        )
    
    if len(job_id) > 100:
        raise HTTPException(status_code=400, detail="Job ID too long")
    
    return job_id

def validate_pagination(offset: int, limit: int) -> tuple[int, int]:
    """Validate pagination parameters"""
    if offset < 0:
        raise HTTPException(status_code=400, detail="Offset must be non-negative")
    
    if limit < 1 or limit > 50:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 50"
        )
    
    return offset, limit
