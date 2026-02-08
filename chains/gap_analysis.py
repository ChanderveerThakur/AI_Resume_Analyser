from langchain_core.prompts import PromptTemplate

def skill_gap_analysis(llm, resume_skills, target_role):

    prompt = PromptTemplate(
        input_variables=["skills", "role"],
        template="""
        You are an AI career mentor.

        Resume Skills:
        {skills}

        Target Role:
        {role}

        Identify:
        - Strong skills
        - Weak skills
        - Missing skills
        """
    )

    chain = prompt | llm
    return chain.invoke({
        "skills": resume_skills,
        "role": target_role
    }).content
