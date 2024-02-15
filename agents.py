from gemini_chat import GeminiChat  # Ensure this import path matches your project structure
import prompts
import logging

gemini = GeminiChat()

class IdeaIntakeAgent:
    @staticmethod
    def process_idea(idea):
        prompt = prompts.IDEA_INTAKE_PROMPT.format(idea=idea)
        response = gemini.send_message(prompt)
        return response

class CodebasePlanningAgent:
    @staticmethod
    def plan_codebase(requirements):
        prompt = prompts.CODEBASE_PLANNING_PROMPT.format(requirements=requirements)
        response = gemini.send_message(prompt)
        return response

class TaskPlannerAgent:
    @staticmethod
    def plan_to_tasks(codebase_plan):
        prompt = prompts.TASK_PLANNING_PROMPT.format(codebase_plan=codebase_plan)
        response = gemini.send_message(prompt)
        return response

class FileWritingAgent:
    @staticmethod
    def generate_files(details):
        prompt = prompts.FILE_WRITING_PROMPT.format(details=details)
        response = gemini.send_message(prompt)
        return response

class CodeReviewAgent:
    @staticmethod
    def review_code(code):
        prompt = prompts.CODE_REVIEW_PROMPT.format(code=code)
        response = gemini.send_message(prompt)
        return response

class CodeRefactoringAgent:
    @staticmethod
    def refactor_code(improvements, code):
        # Assuming the improvements and code are passed as strings or suitable data structures
        # The prompt should combine both the code and the improvements suggested for refactoring
        prompt = prompts.CODE_REFACTORING_PROMPT.format(improvements=improvements, code=code)
        response = gemini.send_message(prompt)
        return response

class GitHubPushAgent:
    @staticmethod
    def push_to_github(changes):
        prompt = prompts.GITHUB_PUSH_PROMPT.format(changes=changes)
        response = gemini.send_message(prompt)
        return response
