import xml.etree.ElementTree as ET
import os
from TraditionalParamTuning.myPackage.Array_Parser import Array_Parser

def read_trigger_data_c7(key_config, file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 子節點與屬性
    mod_wnr24_aec_datas  =  root.findall(key_config["xml_node"])
    # hdr_aec_data 下面有多組 gain 的設定 (mod_wnr24_aec_data)
    # 每組mod_wnr24_aec_data分別有 aec_trigger 與 wnr24_rgn_data
    # 其中 aec_trigger 代表在甚麼樣的ISO光源下觸發
    # wnr24_rgn_data 代表所觸發的參數

    aec_trigger_datas = []
    for ele in mod_wnr24_aec_datas:
        data = []
        aec_trigger = ele.find("aec_trigger")
        data.append(aec_trigger.find("lux_idx_start").text)
        data.append(aec_trigger.find("lux_idx_end").text)
        data.append(aec_trigger.find("gain_start").text)
        data.append(aec_trigger.find("gain_end").text)
        aec_trigger_datas.append(data)

    return aec_trigger_datas

def read_trigger_data_c6(key_config, file_path):
    with open(file_path, 'r', encoding='cp1252') as f:
        text = f.read()

    main_node = Array_Parser(list(text))
    for i in key_config["main_node"]:
        main_node = main_node.get(i)
    
    aec_trigger_datas = []
    for i in range(main_node.length()):
        data = []
        data.append(''.join(main_node.get(i).get(key_config["trigger_node"]).get(2).text))
        data.append(''.join(main_node.get(i).get(key_config["trigger_node"]).get(3).text))
        data.append(''.join(main_node.get(i).get(key_config["trigger_node"]).get(0).text))
        data.append(''.join(main_node.get(i).get(key_config["trigger_node"]).get(1).text))
        data = [float(d.replace('f','')) for d in data]
        aec_trigger_datas.append(data)

    return aec_trigger_datas