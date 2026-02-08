from config.gemini_config import load_gemini_llm
from chains.roadmap_generator import generate_roadmap

llm = load_gemini_llm()

gap_report = """
Strong: Python
Weak: Statistics, ML theory
Missing: NLP, Deployment
"""

print(generate_roadmap(llm, gap_report))
