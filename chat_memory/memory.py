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

memory = []

def update_meory(data):
    memory.append(data)

def get_memory():
    return memory