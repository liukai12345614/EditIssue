"""
给指定issue添加assignees

"""

import requests

def add_assignees(repo, issues, peoples, token):
    # 创建一个字典来存储问题的分配情况
    assignment = {}
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

    # 遍历问题列表并分配给相应人员
    for i, issue in enumerate(issues):
        people = peoples[i % len(peoples)]
        url = f"https://api.github.com/repos/{repo}/issues/{issue['number']}/assignees"
        
        response = requests.post(url, headers=headers, json={'assignees': people}, proxies=proxies)
        try:
            assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
        except AssertionError as err:
            assignment[issue['number']] = f"An error occurred when assign issue {issue['number']}. The error message is: {err}"
            fail += 1
        else:
            assignment[issue['number']] = people
            success += 1

    # 保存最终的add assignees信息
    with open(result_path, 'w') as file:
        for issue_number, info in assignment.items():
            if(info in peoples):
                file.write(f'Issue {issue_number} is assigned to {info}\n')
            else:
                file.write(f'{info}\n')

    # 汇总
    print('='*72)
    print(f'Total: {len(issues)}    success: {success}    fail: {fail}\nPlease check the assign results from add_assignees_result.txt in the result directory')
    print('='*72)