import xml.etree.ElementTree as ET
from TraditionalParamTuning.myPackage.Array_Parser import Array_Parser
import os

def read_param_value_c7(key, key_config, file_path, trigger_idx):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 子節點與屬性
    node  =  root.findall(key_config["xml_node"])

    param_value = []
    for i, ele in enumerate(node):
        if i==trigger_idx:
            rgn_data = ele.find(key_config["data_node"])
            for param_name in key_config['param_names']:
                parent = rgn_data.find(param_name+'_tab')
                if parent:
                    p = parent.find(param_name).text.split(' ') 
                    p = [float(x) for x in p]
                    
                else:
                    parent = rgn_data.find(param_name)
                    p = parent.text.split(' ') 
                    p = [float(x) for x in p]

                # ASF 暫定64取1
                if param_name in ["layer_1_gain_positive_lut",
                                    "layer_1_gain_negative_lut",
                                ]:
                    p = [p[0]]
                
                # ABF 暫定4取1
                if param_name in ["noise_prsv_lo"]:
                    p = [p[0]]
                if param_name in ["noise_prsv_hi"]:
                    p = []

                # # WNR 暫定2取1
                # if param_name in ["denoise_weight_chroma"]:
                #     p = [p[0],p[2]]

                param_value.append(p)
            break

    # converting 2d list into 1d
    param_value = sum(param_value, [])
    print("read_param_value_c7", param_value)
    return param_value



def read_param_value_c6(key, key_config, file_path, trigger_idx):
    with open(file_path, 'r', encoding='cp1252') as f:
        text = f.read()

    main_node = Array_Parser(list(text))
    for i in key_config["main_node"]:
        main_node = main_node.get(i)

    param_node = main_node.get(trigger_idx)

    param_value = []
    for param_idx in key_config["param_node"]:
        if key == "ASF" and param_idx==9: # 只需更改乘號後面的數值，取第一個值就好
                t = ''.join(param_node.get(param_idx).get(i).text)
        #         t = t[t.find('*')+1:] # 取乘號後面的數
                param_value.append(float(t.replace('f','')))
        else:
            for i in range(param_node.get(param_idx).length()):
                param_value.append(float(''.join(param_node.get(param_idx).get(i).text).replace('f','')))

    # print('read_param_value_c6', param_value)
    return param_value


