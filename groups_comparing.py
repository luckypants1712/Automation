from pathlib import Path
import requests
import base64
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--project-url', type=str, required=True)
parser.add_argument('--token', type=str, required=True)
parser.add_argument('--var_group_1_name', type=str, required=True)
parser.add_argument('--var_group_2_name', type=str, required=True)

args = parser.parse_args()

token = args.token
project_url = args.project_url
search_str = args.search_str
var_group_1_name = args.var_group_1_name
var_group_2_name = args.var_group_2_name

url = f'{project_url}/_apis/distributedtask/variablegroups?api-version=6.0-preview.2'
headers = {"Authorization": 'Basic ' + base64.b64encode((':' + token).encode()).decode()}
response = requests.get(url, headers=headers)
r = response.json()

groups = r['value']


var_group_1_results = list(filter(lambda x: x['name'] == var_group_1_name, groups))
var_group_2_results = list(filter(lambda x: x['name'] == var_group_2_name, groups))

if len(var_group_1_results) == 0:
    print('ERROR: Incorrect var_group_1_name')
    exit()
elif len(var_group_2_results) == 0:
    print('ERROR: Incorrect var_group_2_name')
    exit()

var_group_1 = var_group_1_results[0]
var_group_2 = var_group_2_results[0]

vars_1 = list(map(lambda x: x.lower(), var_group_1['variables']))
vars_2 = list(map(lambda x: x.lower(), var_group_2['variables']))

# Sorting Var_groups
group_a = list(filter(lambda x: x not in vars_2, vars_1))
group_b = list(filter(lambda x: x not in vars_1, vars_2))

print(f'vars missing in {var_group_1_name} :')
for var in group_b:
    print(var)

print('-' * 50)

print(f'vars missing in {var_group_2_name} :' )
for var in group_a:
    print(var)
