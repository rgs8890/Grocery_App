# utils.py -> Reusable Funct
import json
import os

def save_data(file_path, data):
    if not data:
        data = []

    # Save the list of dictionaries to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent = 4)
    

def load_data(file_path):
    data = []

    try:
        with open(file_path, 'r') as file:
            data = json.load(file) # Deserialize the data
            return data
    
    except FileNotFoundError: # Handle any file not found error within code
        return data
    

def check_file_exists(file_path) -> bool:

    return os.path.isfile(file_path)



def get_line_delimiter():

    delimiter = "------------"

    return delimiter


