import os
import xml.etree.ElementTree as ET
import json
import numpy as np
from NTU.ML.CMDRunner import CMDRunner
from NTU.ML.Config import Config

from abc import ABC, abstractmethod


class ProjectManager(ABC):
    @abstractmethod
    def get_file_path(self):
        pass
    
    @abstractmethod
    def get_trigger_data(self):
        pass

    @abstractmethod
    def set_param_value(self, param_value):
        pass

    @abstractmethod
    def build_and_push():
        pass
        

class C7ProjectManager(ProjectManager):
    def __init__(self, setting, cmd:CMDRunner):
        self.setting = setting
        self.config = Config().c7_config
        self.cmd = cmd
        
    # def read_config(self, config_path):
    #     assert os.path.exists(config_path)
    #     with open(config_path, 'r') as f:
    #         config = json.load(f)

        # return config
    def is_project(self):
        for key in self.config:
            file_path = self.get_file_path(self.config[key]["file_path"])
            if not os.path.exists(file_path):
                return False
        return True
        
    def get_file_path(self, file_path):
        return self.setting["project_path"] + file_path
    
    def get_trigger_data(self):
        # print(self.setting)
        aec_trigger_datas = []
        congfig_key = None
        for key in self.config:
            file_path = self.get_file_path(self.config[key]["file_path"])
            tree = ET.parse(file_path)
            root = tree.getroot()

            # 子節點與屬性
            mod_wnr24_aec_datas  =  root.findall(self.config[key]["xml_node"])
            # hdr_aec_data 下面有多組 gain 的設定 (mod_wnr24_aec_data)
            # 每組mod_wnr24_aec_data分別有 aec_trigger 與 wnr24_rgn_data
            # 其中 aec_trigger 代表在甚麼樣的ISO光源下觸發
            # wnr24_rgn_data 代表所觸發的參數

            for i, ele in enumerate(mod_wnr24_aec_datas):
                data = []
                aec_trigger = ele.find("aec_trigger")
                data.append(aec_trigger.find("lux_idx_start").text)
                data.append(aec_trigger.find("lux_idx_end").text)
                data.append(aec_trigger.find("gain_start").text)
                data.append(aec_trigger.find("gain_end").text)
                if i == len(aec_trigger_datas):
                    aec_trigger_datas.append(data)
                    congfig_key = key
                else:
                    if aec_trigger_datas[i][2]!=data[2] or aec_trigger_datas[i][3]!=data[3]:
                        print("Error", congfig_key, "與", key, "的 gain trigger 配置不同")
            # print(aec_trigger_datas)
        return aec_trigger_datas

    def set_param_value(self, param_value):
        # expand param
        expand_param_value = np.array([-1])
        i = 0
        for key in self.config:
            for e in self.config[key]["expand"]:
                # print([param_value[i]]*e)
                expand_param_value = np.concatenate((expand_param_value, [param_value[i]]*e))
                i += 1
        expand_param_value = expand_param_value[1:]
        # print('expand_param_value', expand_param_value)
        dim = 0
        for key in self.config:
            print('set_param_value:', key)
            file_path = self.get_file_path(self.config[key]["file_path"])
            # 從檔案載入並解析 XML 資料
            tree = ET.parse(file_path)
            root = tree.getroot()

            # 子節點與屬性
            mod_aec_datas = root.findall(self.config[key]["xml_node"])

            for i, ele in enumerate(mod_aec_datas):
                if i==self.setting["trigger_idx"]:
                    rgn_data = ele.find(self.config[key]["data_node"])
                    for param_name in self.config[key]['param_names']:
                        parent = rgn_data.find(param_name+'_tab')
                        if parent:

                            length = int(parent.attrib['length'])

                            param_value_new = expand_param_value[dim: dim+length]
                            print("length, param_value", length, param_value_new)
                            assert length == len(param_value_new)
                            param_value_new = [str(x) for x in param_value_new]
                            param_value_new = ' '.join(param_value_new)

                            print('old param', rgn_data.find(param_name+'_tab/'+param_name).text)
                            rgn_data.find(param_name+'_tab/' + param_name).text = param_value_new
                            print('new param',rgn_data.find(param_name+'_tab/'+param_name).text)

                        else:
                            parent = rgn_data.find(param_name)

                            length = int(parent.attrib['length'])

                            param_value_new = expand_param_value[dim: dim+length]
                            param_value_new = [str(x) for x in param_value_new]
                            param_value_new = ' '.join(param_value_new)

                            # print('old param', rgn_data.find(param_name+'_tab/'+param_name).text)
                            parent.text = param_value_new
                            # print('new param',rgn_data.find(param_name+'_tab/'+param_name).text)

                        dim += length
                    break

            # write the xml file
            tree.write(file_path, encoding='UTF-8', xml_declaration=True)

    def build_and_push(self):
        self.cmd.run("build_and_push.bat {} {} {}".format(self.setting["exe_path"], self.setting["project_path"], self.setting["bin_name"]), show_detail=True)

class C6ProjectManager(ProjectManager):
    pass

if __name__ == "__main__":
    cmd = CMDRunner()
    c7Mgr = C7ProjectManager(cmd)
    # c7Mgr.set_param_value([1,1,1,1,1,1,1])
    c7Mgr.set_param_value([0,0,0,0,0,0,0])
    c7Mgr.build_and_push()
    
    
