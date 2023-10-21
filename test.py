import json

list_str = '[[0, 0], [0, 128], [0, 256], [0, 384], [0, 512], [0, 640], [0, 768], [0, 896], [0, 1024]]'
my_list = json.loads(list_str)  # 将 JSON 格式的字符串转换回列表
print(my_list)