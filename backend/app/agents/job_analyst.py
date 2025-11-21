from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List
from app.core.config import settings

class JobRequirements(BaseModel):
    required_skills: List[str] = Field(description="Must-have skills")
    preferred_skills: List[str] = Field(description="Nice-to-have skills")
    experience_level: str = Field(description="Junior, Mid, Senior, etc.")
    description_summary: str = Field(description="Brief summary of the role")

class JobAnalyst:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=settings.GOOGLE_API_KEY, 
            model="gemini-2.5-flash-lite",
            temperature=0.3,
            max_retries=2
        )
        self.parser = JsonOutputParser(pydantic_object=JobRequirements)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert Job Analyst. Extract requirements from the job description. Return ONLY JSON."),
            ("user", "Job Description:\n{job_text}\n\n{format_instructions}")
        ])
        self.chain = self.prompt | self.llm | self.parser

    async def analyze(self, job_text: str) -> dict:
        return await self.chain.ainvoke({
            "job_text": job_text,
            "format_instructions": self.parser.get_format_instructions()
        })

job_analyst = JobAnalyst()
