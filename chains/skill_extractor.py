from langchain_core.prompts import PromptTemplate

def extract_skills(llm, resume_text):

    prompt = PromptTemplate(
        input_variables=["resume"],
        template="""
        You are an expert technical recruiter.

        Extract:
        - Technical skills
        - Tools & frameworks
        - Experience level

        Resume:
        {resume}
        """
    )

    chain = prompt | llm
    response = chain.invoke({"resume": resume_text})

    return response.content
