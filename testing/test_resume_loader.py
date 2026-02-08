from ingestion.resume_loader import load_resume_text

with open("sample_resume.pdf", "rb") as f:
    text = load_resume_text(f)

print(text[:500])
