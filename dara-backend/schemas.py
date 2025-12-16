from enum import Enum
from typing import Optional
from pydantic import BaseModel

class IntentType(str, Enum):
    CONVERSATION = "CONVERSATION"
    INSTRUCTION = "INSTRUCTION"

class Action(str, Enum):
    TURN_ON = "TURN_ON"
    TURN_OFF = "TURN_OFF"
    CHECK = "CHECK"
    NONE = "NONE"

class Device(str, Enum):
    LIGHT = "LIGHT"
    FAN = "FAN"
    TEMPERATURE = "TEMPERATURE"
    NONE = "NONE"

class Language(str, Enum):
    EN = "en"
    YO = "yo"
    HA = "ha"
    IG = "ig"

class Intent(BaseModel):
    type: IntentType
    language: str = "en" # Using string to be flexible or use Language enum
    action: Action = Action.NONE
    device: Device = Device.NONE
    response_text: str = "Done."

class VoiceResponse(BaseModel):
    transcript: str
    language: str
    intent: Intent
    response_audio: str
