import os

class Config:
    def __init__(self):
        self.google_api_key = os.environ.get('GOOGLE_API_KEY')
        self.speech_credentials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'google_credentials.json')
        self.default_persona_file = 'default_persona.json'
        self.default_knowledge_file = 'default_knowledge.json'
        self.port = 5008