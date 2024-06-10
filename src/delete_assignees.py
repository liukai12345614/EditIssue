"""
删除指定issue中指定的assignees

"""
import requests
import ast

def delete_assignees(repo, delete_info, token):
    # 创建一个字典来存储删除结果
    delete_result = {}
    people_list = []
    success = 0
    fail = 0
    result_path = "./result/delete_assignees_result.txt"

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    proxies = {
        "http": None,
        "https": None,
    }

    # 删除指定issue number中的指定assign人员
    for issue in delete_info:
        url = f"https://api.github.com/repos/{repo}/issues/{issue['number']}/assignees"

        peoples = ast.literal_eval(issue['peoples'])
        for people in peoples:
            response = requests.delete(url, headers=headers, json={'assignees': people}, proxies=proxies)
            try:
                assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
            except AssertionError as err:
                people_list.append(f"An error occurred when delete {people} in issue {issue['number']}. The error message is: {err}")
                delete_result[issue['number']] = people_list
                fail += 1
            else:
                people_list.append(people)
                delete_result[issue['number']] = people_list
                success += 1
        people_list = []

    # 保存最终的delete assignees信息
    with open(result_path, 'w') as file:
        for issue_number, infos in delete_result.items():
            for info in infos:
                if('error' in info):
                    file.write(f'{info}\n')
                else:
                    file.write(f'Deleted peoples {info} in Issue {issue_number} successfully\n')

    # 汇总
    print('='*78)
    print(f'Total: {success + fail}    success: {success}    fail: {fail}\nPlease check the delete results from delete_result.txt in the result directory')
    print('='*78)