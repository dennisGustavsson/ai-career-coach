from pypdf import PdfReader
from fastapi import UploadFile, HTTPException

MAX_PDF_PAGES = 50
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def extract_text_from_pdf(file: UploadFile) -> str:
    try:
        print("Starting PDF extraction...")
        
        # Check file size
        contents = await file.read()
        file_size = len(contents)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024):.0f}MB"
            )
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Reset file pointer for reading
        await file.seek(0)
        
        reader = PdfReader(file.file)
        num_pages = len(reader.pages)
        print(f"PDF loaded. Pages: {num_pages}")
        
        if num_pages > MAX_PDF_PAGES:
            raise HTTPException(
                status_code=400,
                detail=f"PDF has too many pages. Maximum {MAX_PDF_PAGES} pages allowed"
            )
        
        if num_pages == 0:
            raise HTTPException(status_code=400, detail="PDF has no pages")
        
        text = ""
        for i, page in enumerate(reader.pages):
            print(f"Extracting page {i+1}")
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        text = text.strip()
        
        if len(text) < 50:
            raise HTTPException(
                status_code=400,
                detail="PDF appears to be empty or contains insufficient text"
            )
        
        print("PDF extraction complete.")
        return text
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse PDF: {str(e)}")
