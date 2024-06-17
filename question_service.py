from api_clients import chat_client
import json

class QuestionService:

    def __init__(self):
        pass
    
    def get_next_question(self,input):
        response = json.loads(chat_client.send_chat_request(input))
        return response
    
    

