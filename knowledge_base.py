import json

class KnowledgeBase:
    def __init__(self, knowledge_file=None):
        self.knowledge_data = {}
        if knowledge_file:
            self.load_knowledge(knowledge_file)

    def load_knowledge(self, knowledge_file):
        try:
            with open(knowledge_file, 'r') as f:
                self.knowledge_data = json.load(f)
        except FileNotFoundError:
            print(f"Knowledge file not found: {knowledge_file}")
        except json.JSONDecodeError:
            print(f"Invalid JSON format in knowledge file: {knowledge_file}")

    def get_relevant_knowledge(self, query):
        if not self.knowledge_data:
            return ""
        
        # Simple keyword matching for now
        relevant_knowledge = ""
        for key, value in self.knowledge_data.items():
            if key.lower() in query.lower():
                relevant_knowledge += f"{value}\n"
        return relevant_knowledge