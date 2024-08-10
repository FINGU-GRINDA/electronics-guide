
import random
import re


class ProjectMemory:
    def __init__(self, max_memory=25):
        self.project_titles = []
        self.max_memory = max_memory

    def add_projects(self, new_projects):
        # Extract only the titles from the new projects
        new_titles = [self.extract_title(project) for project in new_projects]
        self.project_titles.extend(new_titles)
        if len(self.project_titles) > self.max_memory:
            self.project_titles = self.project_titles[-self.max_memory:]

    def get_previous_projects(self, n=5):
        return random.sample(self.project_titles, min(n, len(self.project_titles)))

    @staticmethod
    def extract_title(project):
        # Extract the title from a project idea string
        match = re.match(r'\d+\.\s*(.+)', project)
        return match.group(1) if match else project
