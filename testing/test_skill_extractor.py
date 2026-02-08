from config.gemini_config import load_gemini_llm
from chains.skill_extractor import extract_skills

llm = load_gemini_llm()

dummy_resume = """
Python developer with experience in FastAPI, SQL, Git, and ML.
Worked on data pipelines and REST APIs.
"""

output = extract_skills(llm, dummy_resume)
print(output)
