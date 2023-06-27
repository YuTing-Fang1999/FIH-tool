from scipy.stats import qmc
import numpy as np
import csv
import math
import json

class ParamGenerater:
    def __init__(self, bounds, gen_num):
        self.bounds = bounds
        self.gen_num = gen_num
        self.param_num = len(bounds)

    def gen_param(self):
        sampler = qmc.LatinHypercube(d=self.param_num) 
        p = sampler.random(n=self.gen_num) # 隨機產生 gen_num 組

        return p

    def norm_param(self, param):
        # norm
        min_b, max_b = np.asarray(self.bounds).T
        diff = np.fabs(min_b - max_b)

        param = (param-min_b)/diff
        return param
    
    def denorm_param(self, param, step):
        min_b, max_b = np.asarray(self.bounds).T
        diff = np.fabs(min_b - max_b)

        param = min_b + param * diff #denorm
        param = self.round_step_size(param, step)
        return param

    def round_step_size(self, x, step) -> float:
        # https://stackoverflow.com/questions/7859147/round-in-numpy-to-nearest-step
        """Rounds a given quantity to a specific step size
        :param quantity: required
        :param step_size: required
        :return: decimal
        """
        precision: int = int(np.round(-math.log(step, 10), 0))
        return np.round(x, precision)
    
    def save_to_csv(self, filename, param):
        # 儲存csv
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(param)

# if __name__ == "__main__":
#     # 參數範圍
#     config_path = "config/c7project.json"
#     with open(config_path, 'r') as f:
#             config = json.load(f)
#     bounds = None
#     for key in config["param"]:
#         if bounds is None:
#             bounds = np.array(config["param"][key]["bounds"])
#         else:
#             bounds = np.concatenate((bounds, np.array(config["param"][key]["bounds"])))
#     print(bounds)
    
#     param_generater = ParamGenerater(bounds=bounds, gen_num=int(config["gen_num"]))
#     param_norm = param_generater.gen_param()
#     param_norm[0] = [0]*len(bounds)
#     param_norm[1] = [1]*len(bounds)
#     param_denorm = param_generater.denorm_param(param_norm, step=float(config["step"]))
#     param_norm = param_generater.norm_param(param_denorm)
#     param_generater.save_to_csv('param_norm.csv', param_norm)
#     param_generater.save_to_csv('param_denorm.csv', param_denorm)



        