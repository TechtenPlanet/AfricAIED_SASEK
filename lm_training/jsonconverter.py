import json

# Define the input and output file paths
input_file_path = './evaluation_data_1.jsonl'
output_file_path = './converted_data.jsonl'

# Function to read JSONL file
def read_jsonl(file_path):
    data = []
    with open(file_path, 'r') as infile:
        for line in infile:
            data.append(json.loads(line.strip()))
    return data

# Function to convert to llama-2 format
def convert_to_llama2_format(data):
    converted_data = []
    for entry in data:
        input_text = entry['input']
        output_text = entry['output']
        formatted_entry = {
            "prompt": f"<s>[INST] <<SYS>>\nSystem prompt\n<</SYS>>\n\n{input_text} [/INST] {output_text}</s>"
        }
        converted_data.append(formatted_entry)
    return converted_data

# Read the input JSONL file
data = read_jsonl(input_file_path)

# Convert data
converted_data = convert_to_llama2_format(data)

# Save the converted data as a JSONL file
with open(output_file_path, 'w') as outfile:
    for entry in converted_data:
        json.dump(entry, outfile)
        outfile.write('\n')

print(f"Converted data has been saved to {output_file_path}")
