__author__ = 'zuoxianqing'

"""
扫描指定目录中，指定文件中的中文字符串，并提取到output.txt文件中
"""

import os
import re
import sys
import getopt

# 定义需要扫描的文件夹
path = ""

# 定义需要扫描的目标文件列表
target_file_list = []

# 定义需要扫描的文件后缀
suffix = ".cs"


def usage():
    """
    此脚本的使用说明
    :return:None
    """
    print("通过输入-h或--help可以获取帮助")
    print("通过输入-p或--path可以设定程序扫描的路径（C#中对应解决方案的绝对路径）")
    print("通过输入-f或--file可以设定程序扫描的文件（犬夜叉中为SystemStringConstantForClient.cs），如果有多个文件则以,分隔")
    sys.exit(0)


def scan_dir(dir_path: str) -> []:
    """
    扫描指定目录下的所有文件，并返回一个包含文件完整路径的列表
    :param dir_path:目录路径
    :return:文件列表
    """
    l = []
    for dirpath, dirnames, filenames in os.walk(dir_path):
        l.extend([os.path.join(dirpath, item) for item in filenames if item.endswith(suffix)])

    return l


def find_file(file_list: []) -> []:
    """
    查找目标文件，并返回目标文件的绝对路径列表
    :param file_list:待查找的文件列表
    :return:目标文件的绝对路径列表
    """
    final_file_list = []
    for file in file_list:
        if os.path.basename(file) in target_file_list:
            final_file_list.append(file)

    return final_file_list


def scan_chinese(file_list: []) -> []:
    """
    扫描文件列表中的中文，并返回包含每一行中文的列表
    :param file_list:中文列表
    :return:
    """
    # 定义所有的中文列表
    chinese_list = []

    # 定义中文的正则表达式匹配模式
    zh_line_pattern = re.compile(u'^[^/#]*\".*[\u4e00-\u9fa5]+.*\"')
    zh_pattern = re.compile(u'\".*[\u4e00-\u9fa5]+.*\"')

    # 查找文件中的中文
    try:
        for file in file_list:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if zh_line_pattern.match(line):
                        for item in zh_pattern.findall(line):
                            # 先将中文两边的“”去掉
                            item = item.replace('"', '')
                            # 判断是否有重复（因为有可能会有重复使用的中文）
                            if item in chinese_list:
                                continue

                            chinese_list.append(item)
    except:
        print(sys.exc_info())

    return chinese_list


def write_result(chinese_list: []) -> None:
    """
    将中文保存到文件中
    :param chinese_list:中文列表
    :return:None
    """
    with open("output.txt", "w", encoding="utf-8") as file:
        for item in chinese_list:
            print(item)
            file.writelines(item + os.linesep)


def main():
    """
    程序的主处理逻辑
    :return:None
    """
    # 获取传入的参数
    try:
        options, args = getopt.getopt(sys.argv[1:], "hp:f:", ["help", "path=", "file="])
    except getopt.GetoptError:
        sys.exit(0)

    # 解析参数
    for name, value in options:
        if name in ["-h", "--help"]:
            usage()
        if name in ["-p", "--path"]:
            global path
            path = value
        if name in ["-f", "--file"]:
            [target_file_list.append(item) for item in value.split(",")]

    # 判断参数是否合法
    if path == "" or len(target_file_list) == 0:
        usage()

    # 获取目录下的所有文件列表
    file_list = scan_dir(path)

    # 找出需要扫描的文件的绝对路径列表
    final_file_list = find_file(file_list)

    # 定义所有的中文列表
    chinese_list = scan_chinese(final_file_list)

    # 将内容保存到文件中
    write_result(chinese_list)

    print("总共发现{0}条不重复的中文".format(len(chinese_list)))


main()
