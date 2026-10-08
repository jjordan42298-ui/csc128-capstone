import classifier

def test_crisis_safeguard_triggers():
    """Confirms that expressions of severe crisis are successfully caught by the safeguard."""
    is_crisis, message = classifier.check_safety_guardrail("I feel overwhelmed and want to end my life")
    assert is_crisis is True
    assert "988" in message

def test_intent_and_slot_extraction():
    """Verifies that the intent classification algorithm extracts entities correctly."""
    analysis = classifier.extract_entities_and_intent("Give me breathing exercises for my high stress")
    assert analysis["intent"] == "suggest_coping_strategy"
    assert analysis["entities"]["stress_level"] == "high"

def test_sleep_hours_extraction():
    """Validates numerical entity parsing logic for tracking sleeping patterns."""
    analysis = classifier.extract_entities_and_intent("I only slept for 5 hours last night")
    assert analysis["entities"]["sleep_hours"] == 5
