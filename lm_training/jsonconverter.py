import json

def convert_to_text_format(input_file_path, output_file_path):
    # Load the input JSON file
    with open(input_file_path, 'r') as file:
        data = json.load(file)
    
    # Process the data to match the custom training format
    text_data = ""
    for item in data:
        text_data += f"<s>[INST] <<SYS>> System prompt <</SYS>> {item['prompt']}\n"
        text_data += f"/INST {item['completion']}.\n\n"
    
    # Save the converted data to a new text file
    with open(output_file_path, 'w') as file:
        file.write(text_data)

# Example usage
input_json_path = './training_data/2021C38.json'
output_txt_path = './training_data/2021C38.txt'

convert_to_text_format(input_json_path, output_txt_path)
