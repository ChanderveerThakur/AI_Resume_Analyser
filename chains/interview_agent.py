from langchain_core.prompts import PromptTemplate
import json
import re


def _extract_text(response):
    """Normalize Gemini response into plain text"""
    if isinstance(response.content, str):
        return response.content.strip()

    if isinstance(response.content, list):
        text = ""
        for part in response.content:
            if isinstance(part, dict) and "text" in part:
                text += part["text"]
        return text.strip()

    return str(response.content).strip()


def _safe_json(text):
    """Safely extract JSON from LLM output"""
    text = re.sub(r"```json|```", "", text).strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found in LLM response")
    return json.loads(match.group(0))


# ---------------- INTERVIEW QUESTIONS ----------------

def generate_interview_questions(llm, gap_report):
    """
    Generates:
    - 2 MCQs
    - 1 subjective question
    """

    prompt = PromptTemplate(
        input_variables=["gaps"],
        template="""
        You are a technical interviewer.

        Create:
        - 2 multiple-choice questions (4 options each)
        - 1 subjective question

        Respond ONLY in valid JSON:

        {{
          "mcqs": [
            {{
              "question": "MCQ question text",
              "options": ["A", "B", "C", "D"],
              "correct_answer": "A"
            }}
          ],
          "subjective": {{
            "question": "Subjective question text"
          }}
        }}

        Skill gaps:
        {gaps}
        """
    )

    chain = prompt | llm
    response = chain.invoke({"gaps": gap_report})

    return _safe_json(_extract_text(response))


# ---------------- INTERVIEW EVALUATION ----------------

def evaluate_interview(llm, questions, user_answers):
    """
    Evaluates answers and returns score + feedback
    """

    prompt = PromptTemplate(
        input_variables=["questions", "answers"],
        template="""
        Evaluate the interview answers.

        Scoring:
        - Each MCQ: 2 points
        - Subjective answer: 6 points
        - Total: 10 points

        Give:
        - Final score out of 10
        - Short improvement feedback

        Respond ONLY in valid JSON:

        {{
          "score": 7,
          "feedback": "Concise feedback text"
        }}

        Questions:
        {questions}

        User Answers:
        {answers}
        """
    )

    chain = prompt | llm
    response = chain.invoke({
        "questions": questions,
        "answers": user_answers
    })

    return _safe_json(_extract_text(response))
