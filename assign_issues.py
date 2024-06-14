import json, yaml
import ast, os
from colorama import Fore, Style, init
from src.add_assignees import add_assignees
from src.find_labels import find_labels
from src.add_labels import add_labels
from src.delete_labels import delete_labels
from src.common import *

with open('./config/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# 初始化 colorama
init()

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



# 从add_info中获取开始下一位assignees，并从序列中删除最小issueID的issue(该issue仅用于确认下一位assignees，并不需要进行assign操作)，返回需要进行assign的issue和下一位assignees的索引
def filter_add_info(add_info, peoples):
    last_assignees = ast.literal_eval(add_info[0]['assign'])[0]
    try:
        index = (peoples.index(last_assignees)+1) % len(peoples)
    except ValueError:
        print(f'{last_assignees} is not in {peoples}')

    # 删除add_info中的第一条数据
    latest_add_info = add_info[1:]

    return latest_add_info, index


# 对比latest_add_info中所有issue中的labels和它github中的labels，返回需要添加和删除的labels列表
def filter_labels_info(latest_add_info):
    need_add_list = []
    need_delete_list = []
    for issue in latest_add_info:
        github_labels_list = find_labels(repo, issue['number'], token)
        latest_labels_list = ast.literal_eval(issue['label'])

        #将它们转换成集合,获取需要向github labels添加和删除的元素
        set_github_labels_list = set(github_labels_list)
        set_latest_labels_list = set(latest_labels_list)
        need_add_labels = list(set_latest_labels_list - set_github_labels_list)
        need_delete_labels = list(set_github_labels_list - set_latest_labels_list)

        # 在每次迭代中创建新的字典对象
        need_add_dir = {'number': issue['number'], 'label': need_add_labels}
        need_add_list.append(need_add_dir)
        
        need_delete_dir = {'number': issue['number'], 'label': need_delete_labels}
        need_delete_list.append(need_delete_dir)

    return need_add_list, need_delete_list
        
    

def execute():
    while True:
        clear_screen()
        print_header()
        print_people_list(peoples)

        print("如果您要添加人员请输入add\n如果您要删除人员请输入delete\n如果不需要修改请输入continue")
        message = input(Fore.GREEN + "请您输入: ")
        if message == 'add':
            add_people = input("请输入想要添加的人员: ")
            with open('./data/peoples.json', 'r') as file:
                default_peoples = json.load(file)
            if add_people in default_peoples:
                print(f"{add_people}为peoples.json中存在的人员")
                index = default_peoples[add_people]
            else:
                while True:
                    index = input("请输入想要添加的位置(数字): ")
                    if int(index) >=1 :
                        break
                    else:
                        print("请输入一个大于等于1的数字")
            add_people_list(peoples, index, add_people)
        elif message == 'delete':
            delete_people = input("请输入想要删除的人员: ")
            delete_people_list(peoples, delete_people)
        elif message == 'continue':
            break
        else:
            print(Fore.RED + "非法输入，请输入(add, delete, continue)中任意一个值, 按任意键继续...")

        # 恢复默认颜色
        print(Style.RESET_ALL)
        os.system("pause")
    print(Style.RESET_ALL)

    # 写回 YAML 文件
    config['peoples'] = peoples
    with open('./config/config.yaml', 'w') as file:
        yaml.safe_dump(config, file, default_flow_style=False)

    # 更新labels
    print("正在进行更新labels...")
    result = filter_add_info(add_info, peoples)
    need_add_list = filter_labels_info(result[0])[0]
    need_delete_list = filter_labels_info(result[0])[1]
    add_labels(repo, need_add_list, token)
    delete_labels(repo, need_delete_list, token)
    print("完成labels更新")

    # assign issue
    print("正在进行assign issue...")
    result = filter_add_info(add_info, peoples)
    add_assignees(repo, result[0], peoples, token, result[1])
    print("完成assign issue")