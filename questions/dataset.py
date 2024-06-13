import pandas as pd
import json

# Load the spreadsheet
file_path = './2021C39.xlsx'
spreadsheet = pd.ExcelFile(file_path)

# Function to format data with label
def format_data_with_label(df):
    formatted_data = []
    for index, row in df.iterrows():
        prompt = f"NSMQ Question: {row['Question']}"
        completion = row['Answer']
        formatted_data.append({"prompt": prompt, "completion": completion})
    return formatted_data

# Process all sheets and combine the data with the new label
all_data_with_label = []
for sheet in spreadsheet.sheet_names:
    sheet_data = pd.read_excel(file_path, sheet_name=sheet)
    formatted_sheet_data_with_label = format_data_with_label(sheet_data)
    all_data_with_label.extend(formatted_sheet_data_with_label)

# Save the formatted data with label to a JSON file
output_path_with_label = '2021C39.json'
with open(output_path_with_label, 'w') as json_file:
    json.dump(all_data_with_label, json_file, indent=2)

print(f"Data saved to {output_path_with_label}")
