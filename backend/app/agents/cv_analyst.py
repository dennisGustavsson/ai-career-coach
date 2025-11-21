from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List
from app.core.config import settings

class Experience(BaseModel):
    role: str = Field(description="Job title")
    company: str = Field(description="Company name")
    years: str = Field(description="Duration or years of experience")
    description: str = Field(description="Brief description of responsibilities")

class CVProfile(BaseModel):
    skills: List[str] = Field(description="List of technical and soft skills")
    experience: List[Experience] = Field(description="Work experience history")
    education: List[str] = Field(description="Education history")
    summary: str = Field(description="Brief professional summary")
    languages: List[str] = Field(description="Languages spoken")

class CVAnalyst:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=settings.GOOGLE_API_KEY, 
            model="gemini-2.5-flash-lite",
            temperature=0.3,
            max_retries=2
        )
        self.parser = JsonOutputParser(pydantic_object=CVProfile)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert CV analyst. Extract structured data from the provided CV text. Return ONLY JSON."),
            ("user", "CV Text:\n{cv_text}\n\n{format_instructions}")
        ])
        self.chain = self.prompt | self.llm | self.parser

    async def analyze(self, cv_text: str) -> dict:
        return await self.chain.ainvoke({
            "cv_text": cv_text,
            "format_instructions": self.parser.get_format_instructions()
        })

cv_analyst = CVAnalyst()
