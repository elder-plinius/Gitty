import requests
import os
from git import Repo

class GitHubPusher:
    def __init__(self, github_token, github_username, repo_name, workspace_path):
        self.github_token = github_token
        self.github_username = github_username
        self.repo_name = repo_name
        self.workspace_path = workspace_path
        self.repo_url = f"https://github.com/{self.github_username}/{self.repo_name}.git"

    def create_github_repo(self, private=True, description="Created via API"):
        """
        Creates a new GitHub repository.
        """
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "name": self.repo_name,
            "private": private,
            "description": description
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            print(f"Repository {self.repo_name} created successfully.")
            return True
        else:
            print(f"Failed to create repository. Status code: {response.status_code}, Response: {response.json()}")
            return False

    def initialize_local_repo(self):
        """
        Initializes the local directory as a Git repository and sets the remote origin.
        """
        if not os.path.exists(self.workspace_path):
            os.makedirs(self.workspace_path)
        self.repo = Repo.init(self.workspace_path)
        try:
            self.repo.create_remote('origin', self.repo_url)
        except Exception as e:
            print(f"Remote 'origin' already exists. Updating URL to {self.repo_url}.")
            self.repo.delete_remote('origin')
            self.repo.create_remote('origin', self.repo_url)

    def add_commit_push(self, commit_message="Updated files based on GPT output"):
        """
        Adds all changes, commits, and pushes them to the remote repository.
        """
        self.repo.git.add(A=True)
        self.repo.index.commit(commit_message)
        origin = self.repo.remote(name='origin')
        origin.push('--set-upstream', origin, self.repo.active_branch.name)

    def setup_and_push_files(self, gpt_output, commit_message="Initial project setup"):
        """
        Comprehensive method to handle repository creation, file parsing, and pushing.
        """
        # Check and create GitHub repo if doesn't exist
        if self.create_github_repo():
            self.initialize_local_repo()
            # Assuming method to parse GPT output and create files
            self.parse_and_create_files(gpt_output)
            self.add_commit_push(commit_message)
        else:
            print("Repository setup failed.")
