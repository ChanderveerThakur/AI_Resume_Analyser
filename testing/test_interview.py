from config.gemini_config import load_gemini_llm
from chains.interview_agent import mock_interview

llm = load_gemini_llm()

gap_report = "Weak: ML Deployment, System Design"

print(mock_interview(llm, gap_report))
