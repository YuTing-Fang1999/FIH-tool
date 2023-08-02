import re

with open("AE.cpp", 'r') as cpp_file:
    # Read the entire content of the file
    data = cpp_file.read()

# 定义要替换的文本
replacement_text1 = """
                     123,  768,  768,  768,  768, 1000,  768,  768,  768,  768, // BV0
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV1
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV2
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV3
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV4
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV5
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV6
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV7
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV8
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV9
"""
replacement_text2 = """
                     0,  768,  768,  768,  768, 1000,  768,  768,  768,  768, // BV0
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV1
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV2
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV3
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV4
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV5
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV6
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV7
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV8
                     768,  768,  768,  768,  768,  768,  768,  768,  768,  768, // BV9
"""
# 使用正则表达式进行替换，count参数设置为1表示仅替换第一个匹配
pattern = r"//u4_FD_TH: FD brightness target.*?}"  # 匹配 "//u4_FD_TH: FD brightness target" 到下一个 "// BV9" 之间的内容

matches = list(re.finditer(pattern, data, flags=re.DOTALL))
if len(matches) >= 3:
    data = data[:matches[0].start()] + "//u4_FD_TH: FD brightness target" + replacement_text1 + "                }" + data[matches[0].end():]

matches = list(re.finditer(pattern, data, flags=re.DOTALL))
if len(matches) >= 3:
    data = data[:matches[2].start()] + "//u4_FD_TH: FD brightness target" + replacement_text2 + "                }" + data[matches[2].end():]
    # print(modified_data)
else:
    print("沒有匹配到。")
# print(modified_data)
with open("AE_tune.cpp", 'w') as output_file:
    output_file.write(data)
