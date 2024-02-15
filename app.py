import streamlit as st
from dotenv import load_dotenv
import os
import json
from concurrent.futures import ThreadPoolExecutor

# Import AI interaction class and development agents
from gemini_chat import GeminiChat
from agents import (
    IdeaIntakeAgent, CodebasePlanningAgent, TaskPlannerAgent,
    CodeGeneratorAgent, CodeReviewAgent, CodeRefactoringAgent, GitHubPushAgent
)

# Load environment variables
load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')
github_username = os.getenv('GITHUB_USERNAME')

# Initialize the GeminiChat
gemini_chat = GeminiChat()

# Ensure 'chat_history' is initialized in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI Setup
st.title("AI Development Assistant")
repo_name = st.text_input("Enter your desired GitHub repository name", "")
user_idea = st.text_area("What's your project idea?", "")
# Orchestrates the development process from idea to GitHub push
def process_project_idea(user_idea, repo_name):
    if not user_idea or not repo_name:
        st.error("Please specify both a repository name and a project idea.")
        return

    # Idea Intake
    project_plan = IdeaIntakeAgent.process_idea(user_idea)
    st.session_state.chat_history.append(("Idea Intake", project_plan))

    # Codebase Planning
    codebase_plan = CodebasePlanningAgent.plan_codebase(project_plan)
    st.session_state.chat_history.append(("Codebase Planning", codebase_plan))

    # Task Planning
    tasks = TaskPlannerAgent.plan_to_tasks(codebase_plan)
    st.session_state.chat_history.append(("Task Planning", json.dumps(tasks, indent=2)))

    # Code Generation for each task
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(CodeGeneratorAgent.generate_code, task) for task in json.loads(tasks)]
        for future in futures:
            file_path, code = future.result()
            st.session_state.chat_history.append(("Code Generated", f"{file_path}: {code}"))

    # Simplified Code Review and Refactoring (for demonstration)
    reviewed_code = execute_code_review(code)
    st.session_state.chat_history.append(("Code Review", reviewed_code))
    refactored_code = execute_code_refactoring(reviewed_code, "Apply improvements")
    st.session_state.chat_history.append(("Code Refactoring", refactored_code))

    # GitHub Push (Placeholder)
    GitHubPushAgent.push_to_github(refactored_code)
    st.session_state.chat_history.append(("GitHub Push", f"Code pushed to {repo_name} repository."))

# Button to initiate the process
if st.button("Start Project Development"):
    process_project_idea(user_idea, repo_name)

# Display chat history
for role, message in st.session_state.chat_history:
    st.markdown(f"**{role}:** {message}\n")
