from config.gemini_config import load_gemini_llm
from chains.gap_analysis import skill_gap_analysis

llm = load_gemini_llm()

skills = "Python, SQL, Git, FastAPI"
role = "Data Scientist"

result = skill_gap_analysis(llm, skills, role)
print(result)
