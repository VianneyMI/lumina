import litellm
from smolagents import CodeAgent, LiteLLMModel
from backend.aci_gmail_agent import agent as gmail_agent
from backend.phone_calling_tool import PhoneCallingTool
import os

litellm.drop_params = True  # 👈 KEY CHANGE

AGENT_NAME = "Lumina"
DESCRIPTION = "Lumina is my personal assistant. It helps me with my daily tasks."
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
model = LiteLLMModel(
    "mistral/mistral-large-latest",
    api_key=MISTRAL_API_KEY,
)

agent = CodeAgent(
    name=AGENT_NAME,
    description=DESCRIPTION,
    tools=[PhoneCallingTool()],
    model=model,
    add_base_tools=True,
    managed_agents=[gmail_agent],
)
