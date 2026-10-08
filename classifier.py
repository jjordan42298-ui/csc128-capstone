import re
from typing import Dict, Any, Tuple

CRISIS_MESSAGE = (
    "I am an automated wellness tracker, not a licensed medical professional or crisis counselor. "
    "I cannot provide diagnostic or clinical help. If you are experiencing an immediate crisis, "
    "please call or text 988 for the Suicide & Crisis Lifeline immediately, or go to the nearest emergency room."
)
CRISIS_KEYWORDS = ["suicide", "self-harm", "kill myself", "hurt myself", "want to die", "end my life"]

def check_safety_guardrail(text: str) -> Tuple[bool, str]:
    clean_text = text.lower().strip()
    if any(keyword in clean_text for keyword in CRISIS_KEYWORDS):
        return True, CRISIS_MESSAGE
    return False, ""

def extract_entities_and_intent(text: str) -> Dict[str, Any]:
    clean_text = text.lower().strip()
    result = {
        "intent": "unknown",
        "entities": {"stress_level": None, "current_mood": None, "university_name": None, "sleep_hours": None}
    }
    if "high" in clean_text or "severe" in clean_text:
        result["entities"]["stress_level"] = "high"
    elif "moderate" in clean_text or "medium" in clean_text:
        result["entities"]["stress_level"] = "moderate"

    for mood in ["anxious", "overwhelmed", "exhausted", "stressed", "tired", "calm"]:
        if mood in clean_text:
            result["entities"]["current_mood"] = mood
            break

    uni_match = re.search(r'(?:at|for)\s+([a-zA-Z\s]+(?:university|college|state))', clean_text)
    if uni_match:
        result["entities"]["university_name"] = uni_match.group(1).strip().title()

    sleep_match = re.search(r'(\d+)\s*hours?\s*(?:of\s*sleep|slept)?', clean_text)
    if sleep_match:
        result["entities"]["sleep_hours"] = int(sleep_match.group(1))

    if any(word in clean_text for word in ["breathe", "breathing", "coping", "exercise", "grounding", "mindfulness"]):
        result["intent"] = "suggest_coping_strategy"
    elif any(word in clean_text for word in ["log", "mood", "journal", "record"]):
        result["intent"] = "log_daily_mood"
    elif any(word in clean_text for word in ["campus", "clinic", "resource", "counseling", "center"]):
        result["intent"] = "find_campus_resources"
    elif any(word in clean_text for word in ["sleep", "tips", "hygiene", "insomnia", "bedtime"]):
        result["intent"] = "provide_sleep_tips"

    return result
