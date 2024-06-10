"""
给指定issue删除labels

"""

import requests
import ast

def delete_labels(repo, issues, token):
    # 创建一个字典来存储delete labels的结果
    delete_labels_infos = {}
    label_list = []
    success = 0
    fail = 0
    result_path = "./result/delete_labels_result.txt"

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    proxies = {
        "http": None,
        "https": None,
    }


    for issue in issues:
        # Labels 的信息
        labels = ast.literal_eval(issue['label'])
        for label in labels:
            # 构造请求 URL
            url = f"https://api.github.com/repos/{repo}/issues/{issue['number']}/labels/{label}"

            response = requests.delete(url, headers=headers, proxies=proxies)

            try:
                assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
            except AssertionError as err:
                label_list.append(f"An error occurred when delete {label} in issue {issue['number']}. The error message is: {err}")
                delete_labels_infos[issue['number']] = label_list
                fail += 1
            else:
                label_list.append(label)
                delete_labels_infos[issue['number']] = label_list
                success += 1
        label_list = []

    # 保存最终的add assignees信息
    with open(result_path, 'w') as file:
        for issue_number, infos in delete_labels_infos.items():
            for info in infos:
                if('error' in info):
                    file.write(f'{info}\n')
                else:
                    file.write(f'Deleted label {info} in Issue {issue_number} successfully\n')

    # 汇总
    print('='*92)
    print(f'Total: {success + fail}    success: {success}    fail: {fail}\nPlease check the delete labels results from delete_labels_result.txt in the result directory')
    print('='*92)
