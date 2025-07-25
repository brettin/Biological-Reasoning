def get_reflection_agent_prompt():
    """
    The Reflection Agent critically evaluates each idea for plausibility, novelty,
    potential flaws, and citation quality, providing structured feedback.
    """
    return (
        "You are the Reflection Agent in a multi-agent AI co-scientist system. "
        "Analyze each idea's hypothesis and citations for plausibility, novelty, "
        "and potential weaknesses. Provide detailed, structured feedback for "
        "improving each idea."
    )

