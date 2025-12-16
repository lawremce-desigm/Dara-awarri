import os
import json
import requests
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from schemas import Intent, IntentType, Action, Device

load_dotenv()

# Modal N-ATLaS Endpoint
ATLAS_ENDPOINT = "https://lawrenceokosao--dara-atlas-inference.modal.run"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def classify_intent_openai(transcript: str, language: str) -> dict:
    """Fallback to OpenAI if the main model is cold."""
    system_prompt = f"""You are Dára Home, a Nigerian multilingual smart home assistant (like Alexa or Google Home).

You help users control their smart home devices and have friendly conversations. The user may speak in: English, Yoruba, Hausa, or Igbo.

Your job:
1. Detect the intent: CONVERSATION (general chat, questions, greetings) or INSTRUCTION (device control commands)
2. If INSTRUCTION: Extract the device and action from the user's request
3. Always respond in the SAME LANGUAGE the user spoke (User Language Code: {language})
4. Use warm, natural Nigerian phrasing and be helpful like a friendly home assistant

Supported devices: LIGHT, FAN, TEMPERATURE
Supported actions: TURN_ON, TURN_OFF, CHECK

Return ONLY valid JSON:
{{
  "type": "CONVERSATION | INSTRUCTION",
  "language": "{language}",
  "action": "TURN_ON | TURN_OFF | CHECK | NONE",
  "device": "LIGHT | FAN | TEMPERATURE | NONE",
  "response_text": "REQUIRED: Non-empty string. NEVER null."
}}
"""
    
    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript}
        ],
        response_format={"type": "json_object"},
        temperature=0.7
    )
    
    content = response.choices[0].message.content
    print(f"DEBUG OpenAI Output: {content}")
    data = json.loads(content)
    
    return parse_intent_data(data, language)

def parse_intent_data(data: dict, language: str) -> dict:
    intent_type = data.get("type", "CONVERSATION")
    action = data.get("action", "NONE")
    device = data.get("device", "NONE")
    resp_lang = data.get("language", language)
    response_text = data.get("response_text") or "Done."
    
    return {
        "intent": Intent(
            type=IntentType(intent_type),
            language=resp_lang,
            action=Action(action),
            device=Device(device),
            response_text=response_text
        ),
        "response_text": response_text
    }

async def classify_intent(transcript: str, language: str) -> dict:
    """
    Hits the N-ATLaS endpoint on Modal.
    Falls back to OpenAI if it times out clearly.
    Returns: {"intent": Intent, "response_text": str}
    """
    if not transcript:
        return {
            "intent": Intent(type=IntentType.CONVERSATION, language=language, response_text="..."),
            "response_text": "..."
        }

    try:
        # Try our Modal endpoint first
        print("Sending to N-ATLaS (Modal transformers)...")
        
        # Need to offload this since requests is blocking
        response = await asyncio.to_thread(
            requests.post,
            ATLAS_ENDPOINT,
            json={"transcript": transcript, "language": language},
            timeout=120  # Allow time for cold start
        )
        
        response.raise_for_status()
        result = response.json()
        
        generated_text = result.get("generated_text", "")
        print(f"DEBUG N-ATLaS Output: {generated_text}")
        
        # Parse the JSON blob from the model output
        try:
            # Find JSON in the response
            start = generated_text.find("{")
            end = generated_text.rfind("}")
            if start != -1 and end != -1:
                json_str = generated_text[start:end+1]
                data = json.loads(json_str)
                return parse_intent_data(data, language)
            else:
                # No JSON block found
                print("No JSON found in N-ATLaS output")
                # return await classify_intent_openai(transcript, language)
                return {
                    "intent": Intent(type=IntentType.CONVERSATION, language=language, response_text="I didn't understand that."),
                    "response_text": "I didn't understand that."
                }
                
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            # return await classify_intent_openai(transcript, language)
            return {
                "intent": Intent(type=IntentType.CONVERSATION, language=language, response_text="I didn't understand that."),
                "response_text": "I didn't understand that."
            }

    except requests.exceptions.Timeout:
        # Modal is probably starting up, just wait properly next time
        print("Modal timeout (cold start)")
        # return await classify_intent_openai(transcript, language)
        return {
            "intent": Intent(type=IntentType.CONVERSATION, language=language, response_text="Please wait, system warming up."),
            "response_text": "Please wait, system warming up."
        }
    except Exception as e:
        print(f"N-ATLaS Error ({type(e).__name__}): {e}")
        # print("Falling back to OpenAI...")
        # try:
        #     return await classify_intent_openai(transcript, language)
        # except Exception as e2:
        #     print(f"Fallback Error: {e2}")
        return {
            "intent": Intent(type=IntentType.CONVERSATION, language=language, response_text="System error."),
            "response_text": "System error."
        }
