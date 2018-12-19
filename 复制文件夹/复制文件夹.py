# 复制一个文件夹,创建一个进程去复制文件夹,复制使用多进程
# 太过烧脑,绝不碰第二次
import os


def find_file(src_cwd, des_cwd, first):
    """重复分类并创建文件操作并递归进入首个文件夹"""
    src_list = os.listdir(src_cwd)
    # 如果当前文件夹内有东西,重复执行
    if src_list:
        return creat_file(src_cwd, des_cwd)
    # 否则返回上一层,并返回上层目录地址
    return first


def creat_file(src_cwd, des_cwd):
    """搜索源文件中的文件及文件夹信息,并在对应文件夹地址创建文件及文件夹"""
    filelist = []
    fileslist = []
    # 更改当前目录
    first = os.getcwd()  # first 是上一级的目录
    os.chdir(des_cwd)  # des_cwd 是当前目录
    # 将目录中文件与文件夹分类
    for i in os.listdir(src_cwd):
        if '.' in i:
            filelist.append(i)
        else:
            fileslist.append(i)
    # 首先将文件都创建好
    for file in filelist:
        with open(file, 'w') as d:
            with open(src_cwd+'\\'+file, 'r') as s:
                src_file_data = s.read()
            d.write(src_file_data)
            print(file, '文件已创建')
    # 然后递归进入第一个文件夹并返回该文件夹的目录,重复分类并创建文件操作
    for files in fileslist:
        os.mkdir(files)
        print(files, '文件夹已创建')
        current_src_cwd = src_cwd + '\\' + files
        current_des_cwd = os.getcwd() + '\\' + files
        os.chdir(find_file(current_src_cwd, current_des_cwd, des_cwd))
    return first


def main():
    # 输入想要复制的文件夹名称
    src_file = input('请输入源文件名称:')
    # 获取当前文件夹存在的文件名
    listdir = os.listdir('./')
    # 匹配是否存在
    # 如果存在,复制文件名,创建新文件夹,并输入新名
    if src_file in listdir:
        des_file = input('请为新文件夹命名:')
        os.mkdir(des_file)
        # 查找文件夹内部是否有文件
        src_cwd = os.getcwd() + '\\' + src_file
        des_cwd = os.getcwd() + '\\' + des_file
        find_file(src_cwd, des_cwd, des_cwd)

    # 如果不存在,打印错误提示
    else:
        print('未找到该文件夹名称  ')


if __name__ == '__main__':
    main()
