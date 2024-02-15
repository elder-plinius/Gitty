import streamlit as st
from streamlit import session_state as state
import os
import re
import shutil
import tempfile
import logging
# Assuming these modules are in your project's directory structure
from agents import (IdeaIntakeAgent, CodebasePlanningAgent, FileWritingAgent, 
                    CodeReviewAgent, CodeRefactoringAgent, GitHubPushAgent)
from gemini_chat import GeminiChat
from workflow_manager import WorkflowManager

# Initialize the chat and workflow manager
gemini_chat = GeminiChat()
workspace_path = 'workspace'  # Adjust this path as necessary
repo_path = 'path/to/your/repo'  # Placeholder path

# Load environment variables for GitHub token and username
github_token = os.getenv('GITHUB_TOKEN')
github_username = os.getenv('GITHUB_USERNAME')

logging.basicConfig(level=logging.INFO)

# Ensure session state variables are initialized
if 'chat_history' not in state:
    state.chat_history = []

def zip_workspace(workspace_path, output_filename):
    """
    Zips the specified workspace directory and returns the path to the zipped file.
    Ensure the output_filename does not have .zip extension as it's added by make_archive.
    """
    temp_dir = tempfile.mkdtemp()
    # Remove .zip if present in output_filename to avoid duplication
    base_output_path = os.path.join(temp_dir, output_filename.replace('.zip', ''))
    zip_path = shutil.make_archive(base_output_path, 'zip', workspace_path)
    return zip_path  # make_archive already appends .zip

def sanitize_file_path(file_path):
    """
    Cleans and sanitizes the file path to be valid for Windows.
    """
    sanitized_path = file_path.replace('`', '').strip()
    # Replace any invalid characters here with an underscore or remove them
    sanitized_path = re.sub(r'[<>:"/\\|?*]', '_', sanitized_path)
    return sanitized_path

def remove_code_block_markers(content):
    """
    Removes the Markdown code block markers from the content.
    """
    # Remove the starting code block marker that includes "python"
    content = re.sub(r'^```python\n', '', content, flags=re.MULTILINE)
    # Remove any ending code block marker "```"
    content = re.sub(r'```$', '', content, flags=re.MULTILINE)
    return content


def parse_tagged_output(output, workspace_path):
    """
    Parses tagged output and saves files to the workspace directory.
    Adds logging for each step of the process.
    """
    pattern = r'<!--START_FILE_PATH-->(.*?)<!--END_FILE_PATH-->(.*?)<!--START_CONTENT-->(.*?)<!--END_CONTENT-->'
    files = re.findall(pattern, output, re.DOTALL)
    if not files:
        logging.error("No files found in the output to parse.")
        return

    for file_path, _, content in files:
        sanitized_path = sanitize_file_path(file_path)
        content = remove_code_block_markers(content)  # Remove code block markers
        full_path = os.path.join(workspace_path, sanitized_path)
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as file:
                file.write(content.strip())
            logging.info(f"File saved: {full_path}")
        except Exception as e:
            logging.error(f"Failed to save file {sanitized_path}: {e}")

def process_idea(user_idea):
    """
    Processes the user's idea through various stages, from idea intake to file generation, review, refactoring, and offering a download of the generated code.
    """
    state.chat_history.append(("User", user_idea))

    # Idea Intake
    intake_response = IdeaIntakeAgent.process_idea(user_idea)
    state.chat_history.append(("Idea Intake Agent", intake_response))

    # Codebase Planning
    planning_response = CodebasePlanningAgent.plan_codebase(intake_response)
    state.chat_history.append(("Codebase Planning Agent", planning_response))

    # File Generation
    files_response = FileWritingAgent.generate_files(planning_response)
    state.chat_history.append(("File Writing Agent", files_response))
    # parse_tagged_output(files_response, workspace_path)

    # Code Review
    review_response = CodeReviewAgent.review_code(files_response)
    state.chat_history.append(("Code Review Agent", review_response))

    improvement_suggestions = review_response  # This might need adjustment based on your actual data structure
    code_to_refactor = files_response  # Ensure this contains the code you want to refactor

    # Now call the refactor_code method with both required arguments
    refactoring_response = CodeRefactoringAgent.refactor_code(improvements=improvement_suggestions, code=code_to_refactor)
    state.chat_history.append(("Code Refactoring Agent", refactoring_response))
    # Assuming refactoring agent outputs in the same tagged format
    parse_tagged_output(refactoring_response, workspace_path)

    # Simulate or Implement GitHub repository push
    github_response = "Simulated push to GitHub repository."
    state.chat_history.append(("GitHub Push Agent", github_response))

    # Download button for zipped code
    zip_path = zip_workspace(workspace_path, 'generated_code.zip')
    with open(zip_path, "rb") as fp:
        st.download_button("Download Generated Code", fp, "generated_code.zip", "application/zip")


# Streamlit UI Setup
st.title("AI Development Assistant")
user_idea = st.text_input("What's your project idea?", "")

if st.button("Submit Idea"):
    if user_idea:
        process_idea(user_idea)
    else:
        st.error("Please enter an idea to proceed.")

with st.expander("See detailed process steps"):
    for role, message in state.chat_history:
        st.markdown(f"**{role}:** {message}\n")



