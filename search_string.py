from pathlib import Path
import requests
import base64
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--project-url', type=str, required=True)
parser.add_argument('--token', type=str, required=True)
parser.add_argument('--search-string', type=str, required=True)
args = parser.parse_args()

project_url = args.project_url
token = args.token
search_string = args.search_string

url = f'{project_url}/_apis/distributedtask/variablegroups?api-version=6.0-preview.2'
headers = {"Authorization": 'Basic ' + base64.b64encode((':' + token).encode()).decode()}
response = requests.get(url, headers=headers)
r = response.json()

# Error check
try:
    r['value']
except:
    print(r['message'])
    exit()

groups = r['value']
# group_vars = [group for group in groups]
for group in groups:
    group_vars = group['variables']
    for var in group_vars:
        group_vars[var] = str(group_vars[var]).lower()
        if search_string.lower() in group_vars[var]:
            print('output_name:', var, '|', group_vars[var], '|', 'Group witch contains variable:', group['name'])
