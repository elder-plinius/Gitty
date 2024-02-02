import streamlit as st
from streamlit import session_state as state
from agents import (IdeaIntakeAgent, CodebasePlanningAgent, FileWritingAgent, 
                    CodeReviewAgent, CodeRefactoringAgent, GitHubPushAgent)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in state:
    state.chat_history = []

# Function to process the user's idea through the agents
def process_idea(user_idea):
    # This is a simplified version; you'd replace the prints with appending to `state.chat_history`
    structured_idea = IdeaIntakeAgent.process_idea(user_idea)
    state.chat_history.append(("Idea Intake Agent", structured_idea))
    
    requirements = "Extracted requirements from the structured idea"  # Placeholder
    codebase_plan = CodebasePlanningAgent.plan_codebase(requirements)
    state.chat_history.append(("Codebase Planning Agent", codebase_plan))
    
    # Continue through the agents...
    # Finally, return the URL to the GitHub repo (as a placeholder here)
    return "URL to GitHub repo"

# Streamlit UI
st.set_page_config(page_title="AI Agents Chatbot", layout="wide", page_icon=":robot_face:", initial_sidebar_state="expanded")
st.title("AI Agents Chatbot")

# Enable dark mode through Streamlit theme customization (sidebar)
st.sidebar.header("Settings")
dark_mode = st.sidebar.checkbox("Enable Dark Mode", value=True)

if dark_mode:
    st.write('<style>body { background-color: #0e1117; color: #fff; }</style>', unsafe_allow_html=True)

# Chat input
user_input = st.text_input("Enter your idea:", "")

if st.button("Submit"):
    if user_input:
        state.chat_history.append(("User", user_input))
        repo_url = process_idea(user_input)  # Process the idea
        state.chat_history.append(("System", f"Your code has been processed and pushed to GitHub: {repo_url}"))

# Display chat history
for role, message in state.chat_history:
    if role == "User":
        st.text_area("", value=message, height=75, key=message[:10], label=f"{role}")
    else:
        st.text_area("", value=message, height=100, key=message[:10], label=f"{role}", style={"color": "green" if dark_mode else "black"})

