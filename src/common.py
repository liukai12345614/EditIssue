import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("\033[1;34m")  # 设置文本颜色为蓝色
    print(r"""
  /$$$$$$$$       /$$ /$$   /$$                                                   /$$                 /$$ /$$             /$$    
| $$_____/      | $$|__/  | $$                                                  | $$                | $$|__/            | $$    
| $$        /$$$$$$$ /$$ /$$$$$$          /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ | $$  /$$$$$$       | $$ /$$  /$$$$$$$ /$$$$$$  
| $$$$$    /$$__  $$| $$|_  $$_/         /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$| $$ /$$__  $$      | $$| $$ /$$_____/|_  $$_/  
| $$__/   | $$  | $$| $$  | $$          | $$  \ $$| $$$$$$$$| $$  \ $$| $$  \ $$| $$| $$$$$$$$      | $$| $$|  $$$$$$   | $$    
| $$      | $$  | $$| $$  | $$ /$$      | $$  | $$| $$_____/| $$  | $$| $$  | $$| $$| $$_____/      | $$| $$ \____  $$  | $$ /$$
| $$$$$$$$|  $$$$$$$| $$  |  $$$$/      | $$$$$$$/|  $$$$$$$|  $$$$$$/| $$$$$$$/| $$|  $$$$$$$      | $$| $$ /$$$$$$$/  |  $$$$/
|________/ \_______/|__/   \___/        | $$____/  \_______/ \______/ | $$____/ |__/ \_______/      |__/|__/|_______/    \___/  
                                        | $$                          | $$                                                      
                                        | $$                          | $$                                                      
                                        |__/                          |__/
    """)
    print("\033[0m")  # 重置文本颜色
    print("="*130)

# 打印人员列表
def print_people_list(people_list):
    print("\033[1;34m")  # 设置文本颜色为蓝色
    print("这是当前的人员列表：")
    print("\033[0m")  # 重置文本颜色
    for i,people in enumerate(people_list, start=1):
        print(f"{i}、{people}")

# 添加人员到人员列表
def add_people_list(people_list, index, people):
    if(people in people_list):
        print("\033[1;31m")    # 设置文本颜色为红色
        print(f"人员{people}已经存在！")
    else:
        people_list.insert(int(index)-1, people)
        print("\033[1;32m")    # 设置文本颜色为绿色
        print(f"人员{people}添加成功！")
    print("\033[0m")  # 重置文本颜色

# 从人员列表中删除人员
def delete_people_list(people_list, people):
    if(people not in people_list):
        print("\033[1;31m")    # 设置文本颜色为红色
        print(f"人员{people}已不存在于人员列表中！")
    else:
        people_list.remove(people)
        print("\033[1;32m")    # 设置文本颜色为绿色
        print(f"人员{people}删除成功！")
    print("\033[0m")  # 重置文本颜色
