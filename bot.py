import streamlit as st
import json
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="MoneyGuard AI", page_icon="🛡️")

# 1. Setup Gemini (Replace 'YOUR_API_KEY' with your actual key)
genai.configure(api_key="AIzaSyBuaGhLnjZOmgheEXKCDR5W9toQ4J2UjcU")
model = genai.GenerativeModel('models/gemini-2.5-flash')

# 2. Load Your Data
def load_data():
    state = json.load(open('Monthly_Cashflow_State.json'))
    safety = json.load(open('Cashflow_Safety_Rules.json'))
    return state, safety

state_data, safety_rules = load_data()

# 3. Initialize Chat History (The Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI DISPLAY ---
st.title("🛡️ MoneyGuard Interactive Bot")
st.sidebar.write(f"**Current Balance:** ₹{state_data['current_balance']}")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Ask me anything about your spending..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare Context for AI
    # We give the AI your data so it knows what it's talking about
    context = f"""
    User Balance: {state_data['current_balance']}
    Min Safety Limit: {safety_rules['minimum_balance']}
    Rules: You are a strict Financial Guard. Use the data provided. 
    If a user asks to spend money, check if (Balance - Spend) > {safety_rules['minimum_balance']}.
    Never give investment advice.
    """

    # Generate Response
    with st.chat_message("assistant"):
        # Combine context with user question
        full_prompt = f"{context}\n\nUser Question: {prompt}"
        response = model.generate_content(full_prompt)
        
        # Add mandatory disclaimer
        final_answer = f"{response.text}\n\n*Disclaimer: This is informational, not a financial guarantee.*"
        st.markdown(final_answer)
        
    # Save bot message to history
    st.session_state.messages.append({"role": "assistant", "content": final_answer})