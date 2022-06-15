import json
import os

# Load the JSON file
with open(os.path.join(os.path.dirname(__file__),'data.json') )as json_file:
    data = json.load(json_file)
    print(data)