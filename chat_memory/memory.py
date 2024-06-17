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


class Memory:
    def __init__(self):
        """
        This class is used to store the memory of the chatbot
        """
        self.memory = []

    def update_meory(self,data):
        self.memory.append(data)

    def get_memory(self):
        return self.memory