import os
import xml.etree.ElementTree as ET
import json
import numpy as np

from TraditionalParamTuning.myPackage.Array_Parser import Array_Parser
# from myPackage.func import curve_converter

def set_param_value_c7(key, key_config, file_path, trigger_idx, param_value):
    # 從檔案載入並解析 XML 資料
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 子節點與屬性
    mod_aec_datas = root.findall(key_config["xml_node"])
    # expand param
    param_value = np.concatenate([[p]*n for p,n in zip(param_value, key_config["expand"])])
    # if key=="ASF":
    #     param_value = np.concatenate([param_value[:-1], curve_converter(np.arange(64), param_value[-1])])

    for i, ele in enumerate(mod_aec_datas):
        if i==trigger_idx:
            rgn_data = ele.find(key_config["data_node"])
            dim = 0
            for param_name in key_config['param_names']:
                parent = rgn_data.find(param_name+'_tab')
                if parent:

                    length = int(parent.attrib['length'])

                    param_value_new = param_value[dim: dim+length]
                    param_value_new = [str(x) for x in param_value_new]
                    param_value_new = ' '.join(param_value_new)

                    # print('old param', wnr24_rgn_data.find(param_name+'_tab/'+param_name).text)
                    rgn_data.find(param_name+'_tab/' + param_name).text = param_value_new
                    # print('new param',wnr24_rgn_data.find(param_name+'_tab/'+param_name).text)

                else:
                    parent = rgn_data.find(param_name)

                    length = int(parent.attrib['length'])

                    param_value_new = param_value[dim: dim+length]
                    param_value_new = [str(x) for x in param_value_new]
                    param_value_new = ' '.join(param_value_new)

                    # print('old param', wnr24_rgn_data.find(param_name+'_tab/'+param_name).text)
                    parent.text = param_value_new
                    # print('new param',wnr24_rgn_data.find(param_name+'_tab/'+param_name).text)

                dim += length
            break

    # write the xml file
    tree.write(file_path, encoding='UTF-8', xml_declaration=True)

def set_param_value_c6(key, key_config, file_path, trigger_idx, param_value):
    with open(file_path, 'r', encoding='cp1252') as f:
        text = f.read()

    arr_phaser = Array_Parser(list(text))
    main_node = arr_phaser
    for i in key_config["main_node"]:
        main_node = main_node.get(i)

    param_node = main_node.get(trigger_idx)

    idx = 0
    for param_idx in key_config["param_node"]:
        if key == "ASF" and param_idx==9: # 只需更改乘號後面的數值
            for i in range(param_node.get(param_idx).length()):
                # t = param_node.get(param_idx).get(i).text
                # t[''.join(t).find('*')+1:] = str(param_value[idx])
                # param_node.get(param_idx).get(i).text = t
                param_node.get(param_idx).get(i).text = "{0:.6f}f".format(param_value[idx]) # 小數浮點6位
            idx+=1
        else:
            for i in range(param_node.get(param_idx).length()):
                param_node.get(param_idx).get(i).text = "{0:.6f}f".format(param_value[idx]) # 小數浮點6位
                idx+=1

    with open(file_path, 'w', encoding='cp1252') as f:
        f.write(''.join(arr_phaser.reconstruct()))