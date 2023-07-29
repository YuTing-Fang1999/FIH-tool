import re

# 假设您的输入字符串如下：
input_string = ",      //uint32_t fbt_ns_bvsz;      /*Night_BVSize, max size AE_RATIOTBL_MAXSIZE*/"
input_string2 = ",      //uint32_t fbt_ns_bvsz;      /*Night_BVSize, max size AE_RATIOTBL_MAXSIZE*/"

# 使用正则表达式来匹配数字部分
match = re.search(r'\b\d+\b', input_string+input_string2)

# 检查是否找到匹配项
if match:
    result = int(match.group())  # 将匹配到的字符串转换为整数
    print(result)
else:
    print("未找到匹配的数字")
