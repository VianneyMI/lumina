from backend.core_agent import agent


def test_phone_calling_tool() -> None:
    task = """
    I need to call Vianney to remind him about the following:

    1. Mother's day is today
    2. Today is the last day to apply to PIONNEERS
    3. The Hackathon he is attending submission deadline is at 2:00 PM

    Therfore below are the top 3 actions that Vianney need to perform next week:

    1. Apply to PIONNEERS
    2. Submit the Hackathon project
    3. Call his mom


    """

    result = agent.run(task)
    assert result is not None


if __name__ == "__main__":
    test_phone_calling_tool()
