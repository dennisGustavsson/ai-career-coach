from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List
from app.core.config import settings

class MatchAnalysis(BaseModel):
    match_score: int = Field(description="Score from 0 to 100 indicating how well the candidate fits the job")
    reasoning: str = Field(description="Explanation of the score, highlighting strengths and gaps. In Swedish.")
    missing_skills: List[str] = Field(description="Critical skills the candidate is missing")
    advice: str = Field(description="Actionable advice to improve chances for this specific job. In Swedish.")

class CareerCoach:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=settings.GOOGLE_API_KEY, 
            model="gemini-2.5-flash-lite",
            temperature=0.3,
            max_retries=2
        )
        self.parser = JsonOutputParser(pydantic_object=MatchAnalysis)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful Career Coach. Compare the Candidate Profile with the Job Requirements. Provide a match score and advice in Swedish."),
            ("user", "Candidate Profile:\n{cv_profile}\n\nJob Requirements:\n{job_requirements}\n\n{format_instructions}")
        ])
        self.chain = self.prompt | self.llm | self.parser

    async def analyze_match(self, cv_profile: dict, job_requirements: dict) -> dict:
        return await self.chain.ainvoke({
            "cv_profile": str(cv_profile),
            "job_requirements": str(job_requirements),
            "format_instructions": self.parser.get_format_instructions()
        })

career_coach = CareerCoach()
