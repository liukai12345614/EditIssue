"""
给指定issue删除labels

"""

import requests
import ast
from src.find_labels import find_labels

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
        if issue['label']:
            # Labels 的信息
            if(isinstance(issue['label'], str)):
                try:
                    labels = ast.literal_eval(issue['label'])
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing label: {e}")
                    labels = issue['label']
            else:
                labels = issue['label']

            for label in labels:
                # 构造请求 URL
                url = f"https://api.github.com/repos/{repo}/issues/{issue['number']}/labels/{label}"

                response = requests.delete(url, headers=headers, proxies=proxies)

                try:
                    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
                except AssertionError as err:
                    # 当返回状态码为404的时候，去查找该issue的labels，若labels已经不存在，则视为删除成功，否则删除失败
                    if(response.status_code == 404):
                        current_labels = find_labels(repo, issue['number'], token)
                        if(label not in current_labels):
                            label_list.append(f"Deleted label {label} in Issue {issue['number']} fail. status_code = {response.status_code}, label {label} not exists in issue {issue['number']}")
                            delete_labels_infos[issue['number']] = label_list
                            success += 1
                    else:    
                        label_list.append(f"An error occurred when delete {label} in issue {issue['number']}. The error message is: {err}")
                        delete_labels_infos[issue['number']] = label_list
                        fail += 1
                else:
                    label_list.append(label)
                    delete_labels_infos[issue['number']] = label_list
                    success += 1
            label_list = []
        else:
            delete_labels_infos[issue['number']] = [f"issue {issue['number']} no need to delete labels"]

        # 保存最终的delete labels信息
        with open(result_path, 'w') as file:
            for issue_number, infos in delete_labels_infos.items():
                for info in infos:
                    if('error' in info or '404' in info or 'no need' in info):
                        file.write(f'{info}\n')
                    else:
                        file.write(f'Deleted label {info} in Issue {issue_number} successfully\n')

    # 汇总
    print('='*92)
    print(f'Total: {success + fail}    success: {success}    fail: {fail}\nPlease check the delete labels results from delete_labels_result.txt in the result directory')
    print('='*92)
