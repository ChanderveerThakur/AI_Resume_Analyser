from langchain_core.prompts import PromptTemplate

def generate_roadmap(llm, gap_report):

    prompt = PromptTemplate(
        input_variables=["gaps"],
        template="""
        Create an 8-week structured learning roadmap.

        Skill Gap Report:
        {gaps}
        """
    )

    chain = prompt | llm
    return chain.invoke({"gaps": gap_report}).content
