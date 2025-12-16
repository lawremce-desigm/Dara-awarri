import os
import json
import requests
import asyncio
from dotenv import load_dotenv
# Modal N-ATLaS Endpoint
ATLAS_ENDPOINT = "https://lawrenceokosao--dara-atlas-inference.modal.run"

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
                return {
                    "intent": Intent(type=IntentType.CONVERSATION, language=language, response_text="I didn't understand that."),
                    "response_text": "I didn't understand that."
                }
                
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print(f"JSON Parse Error: {e}")
            return {
                "intent": Intent(type=IntentType.CONVERSATION, language=language, response_text="I didn't understand that."),
                "response_text": "I didn't understand that."
            }

    except requests.exceptions.Timeout:
        # Modal is probably starting up, just wait properly next time
        print("Modal timeout (cold start)")
        print("Modal timeout (cold start)")
        return {
            "intent": Intent(type=IntentType.CONVERSATION, language=language, response_text="Please wait, system warming up."),
            "response_text": "Please wait, system warming up."
        }
    except Exception as e:
        print(f"N-ATLaS Error ({type(e).__name__}): {e}")
        return {
            "intent": Intent(type=IntentType.CONVERSATION, language=language, response_text="System error."),
            "response_text": "System error."
        }
