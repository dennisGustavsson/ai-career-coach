from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title="AI Career Coach API")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.routes import router

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Career Coach API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
