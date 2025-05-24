from pydantic import BaseModel
from typing import Any


AGENT_ID = "agent_01jw16cknyetgr98rpd790k7je"
AGENT_PHONE_NUMBER_ID = "phnum_01jw1ddgmyfagvqxw4fqvftbaj"
TO_NUMBER = "+33601267620"

DYNAMIC_VARIABLES = {"actions": "Remind Vianney about mother's day happening tomorrow"}


PROMPT_TEMPLATE = """
You are a friendly and virtual personal assistant named Lumina. You help me in my day to day life on personal and professional topics. You help me stay organized and focused. You help me prioritize what I need to do and send me useful reminders. You bring to my attention important facts that I might have missed.

Below is what you need to bring to Vianney's attention:
{{reminders}}




""".strip()


class AgentPrompt(BaseModel):
    prompt: str | None = PROMPT_TEMPLATE


class AgentConfig(BaseModel):
    prompt: AgentPrompt = AgentPrompt()
    first_message: str | None = None
    language: str | None = None


class TTSConfig(BaseModel):
    voice: str | None = None


class ConversationConfigOverride(BaseModel):
    agent: AgentConfig = AgentConfig()
    tts: TTSConfig = TTSConfig()


class ConversationInitiationClientData(BaseModel):
    conversation_config_override: ConversationConfigOverride = (
        ConversationConfigOverride()
    )
    custom_llm_extra_body: dict[str, Any] = {}
    dynamic_variables: dict[str, Any] = {}


class OutboundCallRequest(BaseModel):
    agent_id: str
    agent_phone_number_id: str
    to_number: str
    conversation_initiation_client_data: ConversationInitiationClientData = (
        ConversationInitiationClientData()
    )


class OutboundCallResponse(BaseModel):
    success: bool
    message: str
    conversation_id: str | None = None
    callSid: str | None = None


class OutboundCallRequestBuilder(BaseModel):
    agent_id: str = AGENT_ID
    agent_phone_number_id: str = AGENT_PHONE_NUMBER_ID

    def build(self) -> OutboundCallRequest:
        return OutboundCallRequest(
            agent_id=self.agent_id,
            agent_phone_number_id=self.agent_phone_number_id,
            to_number=TO_NUMBER,
            conversation_initiation_client_data=ConversationInitiationClientData(
                dynamic_variables=DYNAMIC_VARIABLES,
            ),
        )
