

def rewrite_to_american_english(text: str) -> str:
    """
    Very simple rule-based grammar fixes.
    This will evolve later into an LLM-based rewrite.
    """

    corrections = {
        "i'm name is": "my name is",
        "i am name is": "my name is",
        "i am having doubt": "i have a question",
        "i have doubt": "i have a question",
    }

    lower = text.lower()

    for wrong, correct in corrections.items():
        if wrong in lower:
            text = text.lower().replace(wrong, correct)

    # Capitalize first letter
    return text.capitalize()
