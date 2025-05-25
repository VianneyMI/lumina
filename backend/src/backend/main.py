from backend.core_agent import agent
import time

# Frequency in seconds between agent scans
DEFAULT_SCAN_FREQUENCY = 60 * 30  # 1.5 minutes
DEFAULT_NB_EMAILS_TO_SCAN = 10
DEFAULT_NB_REMINDERS = 3
DEFAULT_NB_ACTIONS = 3


def main(
    scan_frequency: int = DEFAULT_SCAN_FREQUENCY,
    nb_emails_to_scan: int = DEFAULT_NB_EMAILS_TO_SCAN,
    nb_reminders: int = DEFAULT_NB_REMINDERS,
    nb_actions: int = DEFAULT_NB_ACTIONS,
) -> None:
    """Entry Point to run the agent."""

    f""""
    Examine my last {nb_emails_to_scan} emails. 
    Based on this scan, identify the top {nb_reminders} reminders that you think are important to me. 
    
    Finally, identify the top {nb_actions} actions that I need to perform in the next 7 days.
    """

    while True:
        # Prompt the agent
        agent.run(
            f"Examine my last {nb_emails_to_scan} emails. If there is something very very important, please use the phone calling tool to call me."
        )

        # Sleep for the specified frequency
        time.sleep(scan_frequency)


if __name__ == "__main__":
    main()
