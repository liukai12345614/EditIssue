"""
给指定issue添加assignees

"""

import requests
from src.find_assignees import find_assignees

def add_assignees(repo, issues, peoples, token, start_index=0):
    # 创建一个字典来存储问题的分配情况
    assignment = {}
    peoples_status  = {}
    success = 0
    fail = 0
    result_path = "./result/add_assignees_result.txt"

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    proxies = {
        "http": None,
        "https": None,
    }

    # 为所有人员设置assign状态，默认都是可分配状态(0为可分配，1为不可分配)
    for p in peoples:
        peoples_status[p] = 0

    # 遍历问题列表并分配给相应人员
    for i, issue in enumerate(issues, start=start_index):
        people = peoples[i % len(peoples)]
        url = f"https://api.github.com/repos/{repo}/issues/{issue['number']}/assignees"

        # 获取当前issue的assignees
        current_assignees = find_assignees(repo, issue['number'], token)

        #获取当前issue中存在于peoples中的人员列表
        common_assigness = [element for element in current_assignees if element in peoples]

        # 如果common_assigness不为空，则将该列表中人员状态设置为下次不分配
        if(len(common_assigness) != 0):
            for pe in common_assigness:
                peoples_status[pe] = 1

        # 执行assign之前判断当前人员的可分配状态，如果为0并且没有分配给已知人员则执行分配，否则跳过分配将该人员状态恢复为0
        if(peoples_status[people] == 0 and len(common_assigness) == 0):

            response = requests.post(url, headers=headers, json={'assignees': people}, proxies=proxies)
            try:
                assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
            except AssertionError as err:
                assignment[issue['number']] = f"An error occurred when assign issue {issue['number']}. The error message is: {err}"
                fail += 1
            else:
                assignment[issue['number']] = people
                success += 1
        else:
            peoples_status[people] = 0
        



    # 保存最终的add assignees信息
    with open(result_path, 'w') as file:
        for issue_number, info in assignment.items():
            if(info in peoples):
                file.write(f'Issue {issue_number} is assigned to {info}\n')
            else:
                file.write(f'{info}\n')

    # 汇总
    print('='*85)
    print(f'Total: {len(issues)}    success: {success}    fail: {fail}\nPlease check the assign results from add_assignees_result.txt in the result directory')
    print('='*85)