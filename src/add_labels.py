"""
给指定issue添加labels

"""

import requests
import ast

def add_labels(repo, issues, token):
    # 创建一个字典来存储add labels的结果
    add_labels_infos = {}
    success = 0
    fail = 0
    result_path = "./result/add_labels_result.txt"

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    proxies = {
        "http": None,
        "https": None,
    }

    for issue in issues:
        # 构造请求 URL
        url = f"https://api.github.com/repos/{repo}/issues/{issue['number']}/labels"

        # 构造请求体，传递 Labels 的信息
        labels = ast.literal_eval(issue['label'])
        response = requests.post(url, headers=headers, json=labels, proxies=proxies)
        try:
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        except AssertionError as err:
            add_labels_infos[issue['number']] = f"An error occurred when add labels to issue {issue['number']}. The error message is: {err}"
            fail += 1
        else:
            add_labels_infos[issue['number']] = labels
            success += 1

    # 保存最终的add assignees信息
    with open(result_path, 'w') as file:
        for issue_number, info in add_labels_infos.items():
            if('error' in info):
                file.write(f'{info}\n')
            else:
                file.write(f'Add labels {labels} in issue {issue_number} successfully\n')

    # 汇总
    print('='*72)
    print(f'Total: {len(issues)}    success: {success}    fail: {fail}\nPlease check the add labels results from add_labels_result.txt in the result directory')
    print('='*72)