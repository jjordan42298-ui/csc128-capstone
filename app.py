import streamlit as st
from groq import Groq
import classifier, retriever, tools

st.set_page_config(page_title="Student Wellness Hub", page_icon="🌱", layout="centered")
st.title("🌱 Student Wellness & Stress Management Assistant")
st.caption("CSC-128 Chatbot Programming I | Final Capstone Project Submission")

client = None
if "GROQ_API_KEY" in st.secrets:
    try: client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception as e: st.error(f"API Warning: {str(e)}")
else:
    st.warning("🔒 Running in Local Sandbox Mode (Secret key missing on host platform)")

user_input = st.text_input("How can I help support your mental wellness today?", placeholder="Type a request...")

if user_input:
    is_crisis, crisis_reply = classifier.check_safety_guardrail(user_input)
    if is_crisis:
        st.error(crisis_reply)
    else:
        analysis = classifier.extract_entities_and_intent(user_input)
        intent = analysis["intent"]
        entities = analysis["entities"]
        
        if intent == "unknown" and "stress" in user_input.lower():
            intent = "suggest_coping_strategy"
            entities["stress_level"] = "high"

        st.write("---")
        st.markdown(f"**Detected Intent Pipeline:** `{intent}`")
        try:
            if intent == "suggest_coping_strategy":
                st.info(retriever.fetch_grounded_strategy(entities["stress_level"]))
            elif intent == "log_daily_mood":
                mood_val = st.text_input("Extracted Mood:", value=entities["current_mood"] or "Anxious")
                score_val = st.slider("Evaluation Score:", 1, 10, 5)
                notes_val = st.text_area("Journal Capture:", value=user_input)
                if st.button("Commit Entry to Database File"):
                    st.success(tools.save_mood_log(mood_val, score_val, notes_val))
            elif intent == "find_campus_resources":
                target_uni = entities["university_name"] or st.text_input("Confirm University Name:")
                if target_uni: st.warning(tools.search_campus_resources(target_uni))
            elif intent == "provide_sleep_tips":
                if entities["sleep_hours"] is not None:
                    st.write(f"Logged tracking: **{entities['sleep_hours']} hours** of sleep.")
                    if entities["sleep_hours"] < 7: st.error("⚠️ Sleep duration falls below standard thresholds.")
                st.write(retriever.fetch_grounded_sleep_tips())
            else:
                if client:
                    with st.spinner("Formulating insight..."):
                        chat_completion = client.chat.completions.create(
                            messages=[{"role": "system", "content": "You are a polite wellness assistant. Give concise tips."}, {"role": "user", "content": user_input}],
                            model="llama-3.1-8b-instant",
                        )
                        st.chat_message("assistant").write(chat_completion.choices.message.content)
                else: 
                    st.info("👋 Hello! I am your student wellness assistant. Try asking me directly about **'coping strategies'**, **'tracking your mood'**, **'campus resources'**, or **'sleep tips'** so I can trigger my internal modules!")
        except Exception as runtime_err:
            st.error("⚠️ Operational Notice: Error processing this intent path.")
            st.caption(f"Diagnostic details: {str(runtime_err)}")
