from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from app.services.pdf_service import extract_text_from_pdf
from app.services.af_api_service import af_service
from app.agents.cv_analyst import cv_analyst
from app.agents.job_analyst import job_analyst
from app.agents.career_coach import career_coach
from app.middleware.rate_limit import rate_limiter
from app.utils.validators import (
    validate_pdf_file, 
    validate_search_query, 
    validate_job_id, 
    validate_pagination
)
from pydantic import BaseModel, validator
from typing import Dict, Any

router = APIRouter()

class MatchRequest(BaseModel):
    cv_profile: Dict[str, Any]
    job_id: str
    
    @validator('job_id')
    def validate_job_id_field(cls, v):
        return validate_job_id(v)
    
    @validator('cv_profile')
    def validate_cv_profile(cls, v):
        if not v or not isinstance(v, dict):
            raise ValueError("CV profile must be a non-empty dictionary")
        return v

@router.post("/analyze-cv")
async def analyze_cv(file: UploadFile = File(...)):
    # Validate file
    validate_pdf_file(file)
    
    print(f"Received file: {file.filename}")
    text = await extract_text_from_pdf(file)
    print("Text extracted. Calling CV Analyst...")
    try:
        analysis = await cv_analyst.analyze(text)
        print("CV Analysis complete.")
        return {"text": text, "analysis": analysis}
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            raise HTTPException(
                status_code=429, 
                detail="API quota exceeded. Please try again later or check your Google API key quota."
            )
        raise HTTPException(status_code=500, detail=f"Analysis failed: {error_msg}")

@router.get("/search-jobs")
def search_jobs(q: str, offset: int = 0, limit: int = 10):
    # Validate inputs
    query = validate_search_query(q)
    offset, limit = validate_pagination(offset, limit)
    
    return af_service.search_jobs(query, offset, limit)

@router.post("/match")
async def match_job(request: MatchRequest, req: Request):
    # Check rate limit
    if not rate_limiter.check_rate_limit(req):
        remaining = rate_limiter.get_remaining(req)
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. You have analyzed the maximum number of jobs (10) in this session. Please try again later."
        )
    
    # 1. Get Job Details
    job_details = af_service.get_job_details(request.job_id)
    if not job_details:
        raise HTTPException(status_code=404, detail="Job not found")

    # 2. Extract Description
    description = job_details.get("description", {}).get("text", "")
    if not description:
         raise HTTPException(status_code=400, detail="Job description not found")

    # 3. Analyze Job
    try:
        job_reqs = await job_analyst.analyze(description)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            raise HTTPException(
                status_code=429, 
                detail="API quota exceeded. Please try again later."
            )
        raise HTTPException(status_code=500, detail=f"Job analysis failed: {error_msg}")

    # 4. Match
    try:
        match_result = await career_coach.analyze_match(request.cv_profile, job_reqs)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            raise HTTPException(
                status_code=429, 
                detail="API quota exceeded. Please try again later."
            )
        raise HTTPException(status_code=500, detail=f"Match analysis failed: {error_msg}")
    
    # Increment rate limit counter after successful match
    rate_limiter.increment_count(req)
    
    # Add remaining count to response
    remaining = rate_limiter.get_remaining(req)
    match_result["remaining_matches"] = remaining
    
    return match_result

@router.get("/rate-limit-status")
async def get_rate_limit_status(req: Request):
    """Get current rate limit status for the user"""
    remaining = rate_limiter.get_remaining(req)
    return {
        "remaining_matches": remaining,
        "max_matches": 10
    }
