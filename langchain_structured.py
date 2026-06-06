# langchain_structured.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

# Define structured output schema
class BusinessInsight(BaseModel):
    company: str = Field(description="Company name")
    problem: str = Field(description="Main business problem identified")
    solution: str = Field(description="Recommended AI solution")
    estimated_roi: str = Field(description="Estimated ROI in percentage")
    priority: str = Field(description="High / Medium / Low")

# Setup Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# Parser
parser = JsonOutputParser(pydantic_object=BusinessInsight)

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI consultant for Indian manufacturing businesses. Always respond in valid JSON only."),
    ("human", "Analyze this business: {business_description}\n\n{format_instructions}")
])

# Chain
chain = prompt | llm | parser

# Run
result = chain.invoke({
    "business_description": "Agrawal Metal Works, copper and brass manufacturer in Bhiwadi, 3 factories, 3300 tons/month, uses SAP but employees find it confusing, manual meeting tracking",
    "format_instructions": parser.get_format_instructions()
})

print(result)