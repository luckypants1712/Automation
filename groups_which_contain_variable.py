import re
from pathlib import Path
import requests
import base64
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--project-url',type=str, required=True)
parser.add_argument('--token', type=str, required=True)
parser.add_argument('--search-str', type=str, required=True)
args = parser.parse_args()

pat = args.token
project_url = args.project_url
search_str = args.search_str

url = f'{project_url}/_apis/distributedtask/variablegroups?api-version=6.0-preview.2'
headers = {"Authorization": 'Basic ' + base64.b64encode((':' + pat).encode()).decode()}
response = requests.get(url, headers=headers)
r = response.json()

# Error check
try:r['value']
except:
    print(r['message'])
    exit()

groups = r['value']
groups_containing_wanted_var = {}

for group in groups:
    group_vars = group['variables']
    for var in group_vars:
        if var.lower() == search_str:
            wanted_var_value = group_vars[var]
            groups_containing_wanted_var[group['name']] = wanted_var_value
print(groups_containing_wanted_var)


