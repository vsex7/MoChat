import json

class Persona:
    def __init__(self, persona_file=None):
        self.persona_data = {}
        if persona_file:
            self.load_persona(persona_file)

    def load_persona(self, persona_file):
        try:
            with open(persona_file, 'r') as f:
                self.persona_data = json.load(f)
        except FileNotFoundError:
            print(f"Persona file not found: {persona_file}")
        except json.JSONDecodeError:
            print(f"Invalid JSON format in persona file: {persona_file}")

    def get_persona_prompt(self):
        if not self.persona_data:
            return ""
        prompt = "You are a helpful assistant. "
        if "name" in self.persona_data:
            prompt += f"Your name is {self.persona_data['name']}. "
        if "description" in self.persona_data:
            prompt += f"Your description is: {self.persona_data['description']}. "
        if "instructions" in self.persona_data:
            prompt += f"Follow these instructions: {self.persona_data['instructions']}. "
        return prompt