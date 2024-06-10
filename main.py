import json
import yaml
from src.add_assignees import add_assignees
from src.delete_assignees import delete_assignees
from src.find_assignees import find_assignees
from src.find_labels import find_labels
from src.add_labels import add_labels
from src.delete_labels import delete_labels

with open('./config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

#github仓库
repo = config['repo']

# 替换为你的 GitHub token
token = config['token']

# 人员列表
peoples = config['peoples']

# delete info
with open('./data/delete.json', 'r') as file:
    delete_info = json.load(file)

# add info
with open('./data/add.json', 'r') as file:
    add_info = json.load(file)



if __name__ == '__main__':
    # delete_assignees(repo, delete_info, token)
    # add_assignees(repo, issues, peoples, token)
    # assignees = find_assignees(repo, 1, token)
    # labels = find_labels(repo, 1, token)
    # print("Labels:", labels)
    # add_labels(repo, add_info, token)
    delete_labels(repo, delete_info, token)