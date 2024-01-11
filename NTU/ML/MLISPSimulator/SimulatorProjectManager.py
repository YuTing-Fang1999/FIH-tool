import os
import xml.etree.ElementTree as ET
import numpy as np
from NTU.ML.CMDRunner import CMDRunner
from .SimulatorConfig import SimulatorConfig


from abc import ABC, abstractmethod


class ProjectManager(ABC):
    @abstractmethod
    def get_file_path(self):
        pass

    @abstractmethod
    def set_param_value(self, param_value):
        pass

    @abstractmethod
    def build_and_push():
        pass
        

class SimulatorProjectManager(ProjectManager):
    def __init__(self, setting, config, cmd:CMDRunner):
        self.setting = setting
        self.config = config
        self.cmd = cmd
        self.isp_enable = 1
        
    def is_project(self):
        for ISP_key in self.config["modify_key"]:
            ISP_block = self.config["ISP"][ISP_key]
            file_path = self.get_file_path(ISP_block["file_path"])
            if not os.path.exists(file_path):
                print(file_path, "not found")
                return False
        return True
        
    def get_file_path(self, file_path):
        return self.setting["project_path"] + file_path

    def gen_gain_lut_tab(self, overall, shadow, highlight):
        curve = np.zeros(64)
        curve += overall/10
        
        highlight_x = np.linspace(0, 1, 24)
        highlight_x = (highlight_x**2) * (highlight/15 * 3.598638)
        curve[-24:] += highlight_x
        
        shadow_x = np.linspace(1, 0, 25)
        shadow_x = (shadow_x**3.4470155) * ((shadow-15)/15*1.24416)
        curve[:25] += shadow_x
        
        curve[curve<0] = 0
        return curve
    
    def get_gain_weight_lut(self, detail, noise):
        if detail==0 : return [0.996]*64
        x  = np.arange(64)
        return (1-(np.exp(-(x/detail)**3.96))*(1-noise))*0.996
                
    def update_config(self, param_value):
        print("param_value:", param_value)
        # update to config
        i = 0
        for ISP_key in self.config["modify_key"]:
            ISP_block = self.config["ISP"][ISP_key]
            for tag_key in ISP_block["tag"]:
                if "bounds" not in ISP_block["tag"][tag_key]: continue
                if ISP_key in self.config["tune_key"]:
                    param_num = len(ISP_block["tag"][tag_key]["bounds"])
                    p = np.array(param_value[i:i+param_num])
                    i += param_num
                else:
                    # disable value
                    p = np.zeros(len(ISP_block["tag"][tag_key]["bounds"]))
                
                print(tag_key, p)
                
                if tag_key == "layer_1_gain_positive_lut":
                    ISP_block["tag"][tag_key]["value"] = self.gen_gain_lut_tab(p[0], p[1], p[2])
                    ISP_block["tag"]["layer_1_gain_negative_lut"]["value"] = ISP_block["tag"][tag_key]["value"] + 0.3
                    ISP_block["tag"]["layer_1_gain_positive_lut"]["value"][ISP_block["tag"][tag_key]["value"]>3] = 3
                    ISP_block["tag"]["layer_1_gain_negative_lut"]["value"][ISP_block["tag"][tag_key]["value"]>3] = 3
                    
                elif tag_key == "layer_1_gain_weight_lut":
                    ISP_block["tag"][tag_key]["value"] = self.get_gain_weight_lut(p[0], p[1])
                    
                elif tag_key == "layer_1_hpf_symmetric_coeff":
                    if p[0]==0: # thin kernel 
                        ISP_block["tag"][tag_key]["value"] = [0, 0, 0, -1, -2, -25, -86, -173, -180, 1968]
                    elif p[0]==1: # mid kernel 
                        ISP_block["tag"][tag_key]["value"] = [0, 0, -3, -5, -10, -57, -106, -132, 65, 1232]
                    else:
                        print("layer_1_hpf_symmetric_coeff error")
                        
                elif tag_key == "layer_1_clamp_ul":
                        ISP_block["tag"][tag_key]["value"] = p
                        ISP_block["tag"]["layer_1_clamp_ll"]["value"] = -p
                        
                elif tag_key == "layer_2_gain_positive_lut":
                    ISP_block["tag"][tag_key]["value"] = self.gen_gain_lut_tab(p[0], p[1], p[2]) / 3
                    ISP_block["tag"]["layer_2_gain_negative_lut"]["value"] = ISP_block["tag"][tag_key]["value"]
                    ISP_block["tag"]["layer_2_gain_positive_lut"]["value"][ISP_block["tag"][tag_key]["value"]>0.8] = 0.8
                    ISP_block["tag"]["layer_2_gain_negative_lut"]["value"][ISP_block["tag"][tag_key]["value"]>0.8] = 0.8
                
                elif tag_key == "layer_2_gain_weight_lut":
                    ISP_block["tag"][tag_key]["value"] = self.get_gain_weight_lut(p[0], p[1])
                        
                elif tag_key == "layer_2_clamp_ul":
                        ISP_block["tag"][tag_key]["value"] = p
                        ISP_block["tag"]["layer_2_clamp_ll"]["value"] = -p
                        
                elif ISP_key == "ANR":
                    ISP_block["tag"][tag_key]["value"] = [p]*17
                    
                else:
                    ISP_block["tag"][tag_key]["value"] = p
                        
                
                
    def set_isp_enable(self, enable):
        self.isp_enable = enable
        
    def set_param_value(self, param_value):
        self.update_config(param_value)
        
        for ISP_key in self.config["modify_key"]:
            ISP_block = self.config["ISP"][ISP_key]
            print('set_param_value:', ISP_key)
            file_path = self.get_file_path(ISP_block["file_path"])
            # 從檔案載入並解析 XML 資料
            tree = ET.parse(file_path)
            
            # set isp enable
            for tag in ISP_block["enable_tag"]:
                tree.find(tag).text = str(self.isp_enable)
            
            for tag_key in ISP_block["tag"]:
                for path in ISP_block["tag"][tag_key]["path"]:
                    node = tree
                    for i in range(0, len(path), 2):
                        # print(node, 'find', path[i], path[i+1])
                        node = node.findall(path[i])[path[i+1]]
                    
                    param_value_new = ISP_block["tag"][tag_key]["value"]
                    # print(param_value_new)
                    param_value_new = [str(int(x)) if float(x).is_integer() else str(x) for x in param_value_new]
                    param_value_new = ' '.join(param_value_new)
                    node.text = param_value_new
                    # print(tag_key, node.text)
                    # print()

            # write the xml file
            tree.write(file_path, encoding='UTF-8', xml_declaration=True)
            
        # print(self.config)

    def build_and_push(self):
        origin_dir = os.getcwd()
        # os.chdir(self.setting["project_path"]+"/MMFBlend")
        os.chdir(self.setting["project_path"]+"/iso1600/MMFBlend")
        self.cmd.run("runsimulator.bat", show_detail=True)
        os.chdir(origin_dir)
        

class C6ProjectManager(ProjectManager):
    pass

# if __name__ == "__main__":
#     setting = {"project_path": "C:/Users/s830s/OneDrive/文件/github/ISPsimulator"}
#     config = SimulatorConfig().config["c7_config"]
#     cmd = CMDRunner()
#     Mgr = SimulatorProjectManager(setting, config, cmd)
#     Mgr.set_param_value([5,15,0])
#     # Mgr.set_param_value([1,1,1])
    
    
