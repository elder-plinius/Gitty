# prompts.py

IDEA_INTAKE_PROMPT = """
Analyze the user's idea, extracting key concepts, requirements, and desired outcomes. Represent the user's idea in a structured format, including key features, constraints, and desired outcomes. Idea: {idea}
"""

CODEBASE_PLANNING_PROMPT = """
Develop a high-level plan for the codebase, including directory structure and file organization. Design the software architecture to determine the overall structure and components of the codebase based on the following requirements: {requirements}
"""

FILE_WRITING_PROMPT = """
Generate individual code files based on the codebase plan. Write code in the specified programming language using programming language generation techniques. Here are the details: {details}
"""

CODE_REVIEW_PROMPT = """
Analyze the generated code for correctness, efficiency, and adherence to best practices. Here is the code: {code}
"""

CODE_REFACTORING_PROMPT = """
Refactor the generated code to improve its structure, maintainability, and extensibility. Here are the areas to improve: {improvements}
"""

GITHUB_PUSH_PROMPT = """
Push the final codebase to a GitHub repository. Manage code changes and maintain a history of revisions using version control integration. Here are the final changes: {changes}
"""
