"""
查询指定issue的所有labels

"""

import requests

def find_labels(repo, issue_number, token):
    # 构造请求 URL
    url = f'https://api.github.com/repos/{repo}/issues/{issue_number}'
    print(url)
    # 构造请求头
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    proxies = {
        "http": None,
        "https": None,
    }

    try:
        # 发出 GET 请求
        response = requests.get(url, headers=headers, proxies=proxies)
        
        # 检查响应状态码是否表示成功
        response.raise_for_status()
        
        issue_data = response.json()
        
        # 获取 Labels 信息
        labels = issue_data.get('labels', [])
        label_names = [label['name'] for label in labels]
        
        return label_names
    except requests.exceptions.HTTPError as http_err:
        # 捕获并处理 HTTP 错误
        print(f"HTTP error occurred: {http_err}")
        print(f"Response: {response.json()}")
    except Exception as err:
        # 捕获并处理其他错误
        print(f"Other error occurred: {err}")
