import streamlit as st
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

from utils.pdf_report import generate_user_report
from config.gemini_config import load_gemini
from ingestion.resume_loader import load_resume_text
from chains.skill_extractor import extract_skills
from chains.gap_analysis import skill_gap_analysis
from chains.roadmap_generator import generate_roadmap
from chains.interview_agent import (
    generate_interview_questions,
    evaluate_interview
)

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Career Mentor",
    layout="centered"
)

st.title("AI Career Mentor")
st.caption("Skill analysis • Learning roadmap • Mock interview")

# -------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------
for key in ["skills", "gap_report", "roadmap", "questions"]:
    if key not in st.session_state:
        st.session_state[key] = None

# -------------------------------------------------
# LOAD LLM
# -------------------------------------------------
llm = load_gemini()

# -------------------------------------------------
# INPUT SECTION
# -------------------------------------------------
st.subheader("Profile Input")

resume_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

target_role = st.text_input(
    "Target Role",
    placeholder="e.g. Data Scientist"
)

# -------------------------------------------------
# MAIN ANALYSIS (CACHED BY SESSION)
# -------------------------------------------------
if resume_file and target_role:

    try:
        with st.spinner("Analyzing your profile..."):

            resume_text = load_resume_text(resume_file)

            # ---- Skill Extraction ----
            if st.session_state.skills is None:
                st.session_state.skills = extract_skills(
                    llm,
                    resume_text
                )

            # ---- Skill Gap Analysis ----
            if st.session_state.gap_report is None:
                st.session_state.gap_report = skill_gap_analysis(
                    llm,
                    st.session_state.skills,
                    target_role
                )

            # ---- Roadmap Generation ----
            if st.session_state.roadmap is None:
                st.session_state.roadmap = generate_roadmap(
                    llm,
                    st.session_state.gap_report
                )

        # -------------------------------------------------
        # DISPLAY RESULTS
        # -------------------------------------------------
        st.divider()
        st.subheader("Skill Summary")
        st.write(st.session_state.skills)

        st.subheader("Learning Roadmap")
        st.write(st.session_state.roadmap)

        # -------------------------------------------------
        # INTERACTIVE INTERVIEW
        # -------------------------------------------------
        st.divider()
        st.subheader("Mock Interview")

        # Generate interview only once
        if st.session_state.questions is None:
            st.session_state.questions = generate_interview_questions(
                llm,
                st.session_state.gap_report
            )

        questions = st.session_state.questions
        user_answers = {}

        # ---- MCQs ----
        for i, q in enumerate(questions["mcqs"], start=1):
            user_answers[f"mcq_{i}"] = st.radio(
                f"Q{i}. {q['question']}",
                q["options"],
                key=f"mcq_{i}"
            )

        # ---- Subjective ----
        user_answers["subjective"] = st.text_area(
            f"Q{len(questions['mcqs']) + 1}. {questions['subjective']['question']}",
            height=120
        )

        # ---- Submit Interview ----
        if st.button("Submit Interview"):
            try:
                with st.spinner("Evaluating your answers..."):
                    result = evaluate_interview(
                        llm,
                        questions,
                        user_answers
                    )

                st.divider()
                st.subheader("Interview Result")

                st.metric(
                    label="Final Score",
                    value=f"{result['score']} / 10"
                )

                st.success(result["feedback"])

                # -------------------------------------------------
                # PDF REPORT GENERATION (NEW FEATURE)
                # -------------------------------------------------
                pdf_path = "AI_Career_Mentor_Report.pdf"

                generate_user_report(
                    file_path=pdf_path,
                    target_role=target_role,
                    skills=st.session_state.skills,
                    roadmap=st.session_state.roadmap,
                    questions=questions,
                    user_answers=user_answers,
                    score=result["score"],
                    feedback=result["feedback"]
                )

                with open(pdf_path, "rb") as pdf:
                    st.download_button(
                        label="Download Full Report (PDF)",
                        data=pdf,
                        file_name="AI_Career_Mentor_Report.pdf",
                        mime="application/pdf"
                    )

            except ChatGoogleGenerativeAIError:
                st.warning(
                    "Rate limit reached. Please wait about one minute and try again."
                )

    except ChatGoogleGenerativeAIError:
        st.warning(
            "Gemini API rate limit reached. Please wait one minute and refresh."
        )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.divider()
st.caption("Built with Gemini Flash • LangChain • Streamlit")
