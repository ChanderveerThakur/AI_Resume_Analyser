from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def generate_user_report(
    file_path,
    target_role,
    skills,
    roadmap,
    questions,
    user_answers,
    score,
    feedback
):
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Career Mentor – User Report", styles["Title"]))
    story.append(Spacer(1, 14))

    story.append(Paragraph(f"<b>Target Role:</b> {target_role}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Extracted Skills</b>", styles["Heading2"]))
    story.append(Paragraph(str(skills), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Learning Roadmap</b>", styles["Heading2"]))
    story.append(Paragraph(str(roadmap), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Interview Questions & Answers</b>", styles["Heading2"]))
    for key, value in user_answers.items():
        story.append(Paragraph(f"<b>{key}:</b> {value}", styles["Normal"]))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Final Score:</b> {score} / 10", styles["Normal"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"<b>Feedback:</b> {feedback}", styles["Normal"]))

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    doc.build(story)
