# 导入 re 模块，用于正则表达式匹配
import re

# 打开 main.py 文件
with open("main.py", "r") as f:
    # 读取文件内容
    lines = f.readlines()

# 创建一个空列表，用于存储没有注释和空白的行
no_comments_no_blanks = []

# 遍历每一行
for line in lines:
    # 检查是否包含 # 符号，如果有，就用正则表达式替换掉 # 及其后面的内容为空字符串
    if "#" in line:
        line = re.sub(r"#.*", "", line)
    # 检查是否是空白的行，如果不是，就添加到列表中
    if line.strip():
        no_comments_no_blanks.append(line)

# 打开 main_no_comments.py 文件，用写入模式
with open("main_no_comments.py", "w") as f:
    # 把列表中的每一行写入文件
    for line in no_comments_no_blanks:
        f.write(line)
