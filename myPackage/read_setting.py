import os
import json

def read_setting():
    if os.path.exists('setting.json'):
        with open('setting.json', 'r') as f:
            setting = json.load(f)
            if not os.path.exists(setting["filefolder"]):
                setting["filefolder"] = "./"
            return setting
        
    else:
        print("找不到設定檔，重新生成一個新的設定檔")
        return {
            "filefolder": "./"
        }
        
def write_setting(setting):
    print('write_setting')
    with open("setting.json", "w") as outfile:
        outfile.write(json.dumps(setting, indent=4))