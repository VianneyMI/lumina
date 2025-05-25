from backend.core_agent import agent
import time


def main() -> None:
    # Frequency in seconds between agent prompts
    prompt_frequency = 60  # Default to 1 minute
    agent.run(
        "Examine my last 10 emails. If there is something very very important, please use the phone calling tool to call me."
    )

    # while True:
    #     # Prompt the agent
    #     agent.run(
    #         "Examine my last 10 emails. If there is something very very important, please use the phone calling tool to call me."
    #     )

    #     # Sleep for the specified frequency
    #     time.sleep(prompt_frequency)


if __name__ == "__main__":
    main()
