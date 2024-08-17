import re

# 读取
with open('settings.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 删除字符
filtered_content = re.sub(r'[^A-Za-z0-9=]', '', content)

# 写回文件
with open('settings.txt', 'w', encoding='utf-8') as file:
    file.write(filtered_content)

print("$root@127.0.0.1 Settings >>已经删除并转码")
