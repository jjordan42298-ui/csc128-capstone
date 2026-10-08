import json
from datetime import datetime

def save_mood_log(mood: str, rating: int, snippet: str) -> str:
    log_entry = {"timestamp": datetime.now().isoformat(), "current_mood": mood or "Not specified", "mood_score": rating, "journal_snippet": snippet or "No text provided"}
    try:
        with open("mood_history.json", "a") as file:
            file.write(json.dumps(log_entry) + "\n")
        return f"Successfully recorded. Your mood score is {rating}/10."
    except Exception as e:
        return f"Database Write Failure: {str(e)}"

def search_campus_resources(university_name: str) -> str:
    directory = {
        "state university": "State University Counseling Center\n📍 Location: 101 Wellness Lane\n🕒 Hours: M-F 8:00 AM - 5:00 PM\n📞 Contact: (555) 019-2831",
        "community college": "Campus Mental Health Hub\n📍 Location: Building C, Room 204\n🕒 Hours: M-Th 9:00 AM - 4:00 PM\n📞 Contact: (555) 014-9982"
    }
    if not university_name:
        return "Please specify your university name clearly."
    return directory.get(university_name.lower().strip(), f"No record found for '{university_name}'. Contact Student Affairs.")
