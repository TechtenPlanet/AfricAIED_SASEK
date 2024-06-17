import requests
import json

url = "http://127.0.0.1:8000/process"

# input_data = {
#     "messages": [
#         {
#             "input": "Hello",
#             "output": "Hi, how can I help you today"
#         },
#         {
#             "input": "What is one plus one"
#         }
#     ]
# }

def send_chat_request(input_data):
    response = requests.post(url, json=input_data)
    result  = response.json()
    return result.ai_response
