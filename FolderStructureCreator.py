import os
import json

class FolderStructureCreator:
    def __init__(self, links_file):
        self.links_file = links_file

    def create_folder_structure(self):
        try:
            with open(self.links_file, 'r', encoding='utf-8') as file:
                links = json.load(file)
            
            departments = {}
            
            for link in links:
                parts = link.split('/')
                department = parts[3]
                category = parts[4]
                if department not in departments:
                    departments[department] = set()
                departments[department].add(category)

            for department, categories in departments.items():
                department_folder = os.path.join(department)
                os.makedirs(department_folder, exist_ok=True)
                for category in categories:
                    category_folder = os.path.join(department_folder, category)
                    os.makedirs(category_folder, exist_ok=True)

            print(departments)
        except Exception as e:
            print(f"Error while creating folders: {e}")
