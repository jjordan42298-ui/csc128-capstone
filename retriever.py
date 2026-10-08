GROUNDED_COPING_STRATEGIES = {
    "high": "Grounded Exercise (4-7-8 Breathing Technique):\n1. Inhale deeply through your nose for 4 seconds.\n2. Hold your breath calmly for 7 seconds.\n3. Exhale completely through your mouth making a whoosh sound for 8 seconds.\nRepeat this cycle 4 times.",
    "moderate": "Grounded Exercise (5-4-3-2-1 Technique):\nAcknowledge your surroundings deliberately:\n- 5 things you can see\n- 4 things you can touch\n- 3 things you can hear\n- 2 things you can smell\n- 1 thing you can taste"
}
GROUNDED_SLEEP_TIPS = "Evidence-Based Sleep Hygiene Rules:\n1. Wake up at the identical time daily.\n2. Turn off electronics 60 minutes before bedtime.\n3. Keep your ambient sleeping space cool.\n4. Reserve your bed strictly for sleeping."

def fetch_grounded_strategy(stress_level: str) -> str:
    level = stress_level or "moderate"
    return GROUNDED_COPING_STRATEGIES.get(level, GROUNDED_COPING_STRATEGIES["moderate"])

def fetch_grounded_sleep_tips() -> str:
    return GROUNDED_SLEEP_TIPS
