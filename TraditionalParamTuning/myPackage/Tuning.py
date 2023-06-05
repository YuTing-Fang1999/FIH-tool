from PyQt5.QtWidgets import QHBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal, QThread, QObject, Qt

from .MplCanvasTiming import MplCanvasTiming
from .ImageMeasurement import *

import numpy as np
from time import sleep
from subprocess import call
import xml.etree.ElementTree as ET
from scipy import stats  # zcore
import os
import sys
import cv2
import math
import threading
import shutil
import json
from random import randrange
import csv
from decimal import Decimal
import copy
from scipy.stats import qmc
import datetime

class Tuning(QObject):  # 要繼承QWidget才能用pyqtSignal!!
    finish_signal = pyqtSignal(bool)
    # UI
    set_score_signal = pyqtSignal(str)
    set_generation_signal = pyqtSignal(str)
    set_individual_signal = pyqtSignal(str)
    set_statusbar_signal = pyqtSignal(str)
    # param window
    show_param_window_signal = pyqtSignal()
    setup_param_window_signal = pyqtSignal(int, int, np.ndarray) # popsize, param_change_num, IQM_names
    update_param_window_signal = pyqtSignal(int, np.ndarray, float, np.ndarray)
    update_param_window_scores_signal = pyqtSignal(list)
    # logger
    log_info_signal = pyqtSignal(str)
    run_cmd_signal = pyqtSignal(str)
    alert_info_signal = pyqtSignal(str, str)

    def __init__(self, logger, run_page_lower_part, setting, config, capture, set_param_value, build_and_push, get_file_path):
        super().__init__()
        self.logger = logger
        self.run_page_lower_part = run_page_lower_part
        self.set_param_value = set_param_value
        self.build_and_push = build_and_push
        self.get_file_path = get_file_path
        
        self.setting = setting
        self.config = config
        self.capture = capture

        self.is_run = False
        self.TEST_MODE = False
        self.is_rule = False
        if self.is_rule:
            # 退火
            self.T = 0.8
            self.T_rate = 0.95

        self.calFunc = get_cal_func()

        # plot
        self.tab_info = self.run_page_lower_part.tab_info
        self.best_score_plot = MplCanvasTiming(
            self.run_page_lower_part.tab_score.label_plot, color=['r', 'g'], name=['score'], axis_name=["Generation", "Score"]
        )
        self.hyper_param_plot = MplCanvasTiming(
            self.run_page_lower_part.tab_hyper.label_plot, color=['g', 'r'], name=['F', 'Cr'], axis_name=["Generation", "HyperParam Value"]
        )
        self.update_rate_plot = MplCanvasTiming(
            self.run_page_lower_part.tab_update.label_plot, color=['b', 'k'], name=['using ML', 'no ML'], axis_name=["Generation", "Update Rate"]
        )

    
    def run(self):
        ##### param setting #####
        self.key = self.setting["key"]
        self.key_config = self.config[self.setting["platform"]][self.setting["root"]][self.setting["key"]]
        self.key_data = self.setting[self.setting["root"]][self.setting["key"]]
        self.file_path = self.get_file_path[self.setting["platform"]](self.setting["project_path"], self.key_config["file_path"])

        # config
        self.rule = self.key_config["rule"]
        self.step = self.key_config["step"]
        
        # project setting
        self.platform = self.setting["platform"]
        self.exe_path = self.setting["exe_path"]
        self.project_path = self.setting["project_path"]
        self.bin_name = self.setting["bin_name"]

        # hyperparams
        self.capture_num = self.setting['capture num']
        
        self.bounds = []
        col = sum(self.key_config["col"], [])
        for i in range(len(col)):
            self.bounds.append([self.key_data["coustom_range"][i]]*col[i])
        self.bounds = sum(self.bounds, [])
        # print(self.bounds)

        self.param_value = np.array(self.key_data['param_value']) # 所有參數值
        self.param_change_idx = self.key_data['param_change_idx'] # 需要tune的參數位置
        self.param_change_num = len(self.param_change_idx) # 需要tune的參數個數
        
        self.trigger_idx = self.setting["trigger_idx"]
        self.trigger_name = self.setting["trigger_name"]

        # target region
        self.my_rois = self.setting['my_rois']
        self.target_rois = self.setting['target_rois']

        # target score
        if self.TEST_MODE:
            self.setting["target_type"]=["TEST", "TEST2", "TEST3"]
            self.setting["target_score"]=[0]*len(self.setting["target_type"])
            self.setting["target_weight"]=[1]*len(self.setting["target_type"])

        self.target_type = np.array(self.setting["target_type"])
        self.target_IQM_min = np.array(self.setting["target_score_min"])
        self.target_IQM_max = np.array(self.setting["target_score_max"])
        self.weight_IQM = np.array(self.setting["target_weight"])
        self.target_num = len(self.target_type)
        # 暫時設成1
        self.std_IQM = np.ones(self.target_num)

        # get the bounds of each parameter
        self.min_b, self.max_b = np.asarray(self.bounds).T
        self.min_b = self.min_b[self.param_change_idx]
        self.max_b = self.max_b[self.param_change_idx]
        self.diff = np.fabs(self.min_b - self.max_b)

        # score
        self.best_score = 1e9
        self.fitness = []  # 計算popsize個individual所產生的影像的分數
        self.IQMs = []
        self.pop = []

        # 防呆
        if len(self.setting["target_type"])==0:
            self.alert_info_signal.emit("請先圈ROI", "請先圈ROI")
            self.finish_signal.emit(False)
            return

        if self.param_change_num==0:
            self.alert_info_signal.emit("請選擇要調的參數", "目前參數沒打勾\n請打勾要調的參數")
            self.finish_signal.emit(False)
            return

        self.show_info()
        

        # save target ROI
        if os.path.exists("target_ROI"): shutil.rmtree("target_ROI")
        self.mkdir("target_ROI")
        self.target_roi_imgs = []
        # self.resize_scale = np.ones(len(self.target_rois))

        for i, target in enumerate(self.target_rois):
            
            print(target)
            target_img = cv2.imdecode(np.fromfile(file=target[0], dtype=np.uint8), cv2.IMREAD_COLOR)
            x0, y0, w0, h0 = self.my_rois[i]
            x1, y1, w1, h1 = target[1]

            target_roi_img = target_img[y1: y1+h1, x1:x1+w1]

            # if h1>h0:
            #     target_roi_img = cv2.resize(target_roi_img, (int(w1*(h0/h1)), int(h1*(h0/h1))), interpolation=cv2.INTER_AREA)
            # elif h0>h1:
            #     self.resize_scale[i] = h1/h0

            
            name = target[0].split('/')[-1].split('.')[0]
            self.target_roi_imgs.append([name, target_roi_img])
            cv2.imwrite("target_ROI/target_ROI{}_{}.jpg".format(i+1, name), target_roi_img)
        
        # csv data
        title = ["name", "score"]
        for t in self.target_type: title.append(t)
        title.append(self.key_config["param_names"])
        title.append("weight")
        self.csv_data = [title]
        self.best_csv_data = [title]

        # csv target
        data = ["target", 0]
        for i in range(len(self.target_IQM_min)): 
            data.append([self.target_IQM_min[i], self.target_IQM_max[i]])
        data.append("")
        data.append(self.weight_IQM)
        self.csv_data.append(data)
        self.best_csv_data.append(data)


        ##### start tuning #####
        # setup
        if not self.TEST_MODE:
            # 刪除資料夾
            if os.path.exists('log'): shutil.rmtree('log')
            if os.path.exists('best_photo'): shutil.rmtree('best_photo')
            self.mkdir('log')
            self.mkdir('best_photo')
        self.setup()

        print(self.setting["method"])
        if self.setting["method"] == "global search":
            # hyperparams
            self.popsize = self.setting['population size']
            self.generations = self.setting['generations']
            self.setup_param_window_signal.emit(self.popsize, self.param_change_num, self.target_type)
            self.DE()
        elif self.setting["method"] == "local search":
            self.setup_param_window_signal.emit(self.param_change_num+1, self.param_change_num, self.target_type)
            self.Nelder_Mead()
        
        self.finish_signal.emit(True)
        

    def DE(self):
        # test mode 下沒改動的地方為0
        if self.TEST_MODE: self.param_value = np.zeros(len(self.param_value))
        
        self.F = 0.7
        self.Cr = 0.5

        # Generate samples from a Latin hypercube generator
        sampler = qmc.LatinHypercube(d=self.param_change_num)
        self.pop = sampler.random(n=self.popsize)
        # self.pop = np.random.random((self.popsize, self.param_change_num))
        self.pop = self.min_b + self.pop * self.diff #denorm
        self.pop = self.round_nearest(self.pop)
        self.log_info_signal.emit(str(self.pop))
        self.pop = ((self.pop-self.min_b)/self.diff) #norm
        no_improv = 0
        no_improv_break = 5

        # update rate
        self.update_count=0
        self.update_rate=0

        self.initial_individual()

        # Do Differential Evolution
        for gen_idx in range(self.generations):
            self.run_DE_for_a_generation(gen_idx)

            print('\nupdate_rate',self.update_rate)
            if self.update_rate == 0: no_improv+=1
            else: no_improv=0
            
            if self.best_score<1e-4:
                self.log_info_signal.emit('finish')
                self.finish_signal.emit(True)
            if no_improv >= no_improv_break:
                self.log_info_signal.emit('stop because no improvement')
                self.finish_signal.emit(True)
                

    def Nelder_Mead(self):
        ##### Nelder-Mead algorithm #####
        step = 0.1
        max_iter = 100
        no_improve_thr = 1e-4
        no_improv_break = 10
        alpha=1
        gamma=2
        rho=-0.5
        sigma=0.5

        # init
        self.IQMs = []
        now_IQM = self.measure_IQM_by_param_value('log/init_0', self.param_value)
        self.IQMs.append(now_IQM)
        prev_best = self.cal_score_by_weight(now_IQM)

        data = ["init_0", prev_best]
        for IQM in now_IQM: data.append(IQM)
        data.append(self.param_value.copy())
        self.csv_data.append(data)
        
        no_improv = 0
        dim = self.param_change_num
        x_start = (self.param_value[self.param_change_idx]-self.min_b)/self.diff #norm
        self.pop = [x_start]
        self.fitness = [prev_best]
        
        # res = [[x_start, prev_best]]
        self.update_param_window_signal.emit(0, self.param_value[self.param_change_idx], prev_best, now_IQM)

        self.set_generation_signal.emit("initialize")
        for i in range(dim):
            x = copy.copy(x_start)
            x[i] = x[i] + step
            self.param_value[self.param_change_idx] = self.min_b + x * self.diff #denorm
            now_IQM = self.measure_IQM_by_param_value('log/init_{}'.format(i+1), self.param_value)
            self.IQMs.append(now_IQM)
            score = self.cal_score_by_weight(now_IQM)
            self.log_info_signal.emit('init: {}'.format([x, score]))
            self.update_param_window_signal.emit(i+1, self.param_value[self.param_change_idx], score, now_IQM)
            self.pop.append(x)
            self.fitness.append(score)

            data = ["init_{}".format(i+1), score]
            for IQM in now_IQM: data.append(IQM)
            data.append(self.param_value.copy())
            self.csv_data.append(data)
            # res.append([x, score])

        self.pop = self.min_b + self.pop * self.diff #denorm
        self.pop = self.round_nearest(self.pop)
        self.pop = ((self.pop-self.min_b)/self.diff) #norm

        # 更新經由標準差後的分數
        # self.std_IQM = np.array(self.IQMs).std(axis=0)

        # fitness = []
        # for i in range(dim+1):
        #     res[i][1] = self.cal_score_by_weight(self.IQMs[i])
        #     fitness.append(res[i][1])
        # self.update_param_window_scores_signal.emit(fitness)

        # simplex iter
        iters = 0
        while 1:
            if not self.TEST_MODE:
                with open('log/iter{}.csv'.format(iters), 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(self.csv_data)
            self.set_generation_signal.emit(str(iters))
            # self.log_info_signal.emit(str(iters))
            # order
            # res.sort(key=lambda x: x[1])
            self.pop, self.fitness = zip(*sorted(zip(self.pop, self.fitness), key=lambda x: x[1]))
            self.pop = list(self.pop)
            self.fitness = list(self.fitness)
            best = self.fitness[0]

            # break after max_iter
            if max_iter and iters >= max_iter:
                return self.fitness[0]
            iters += 1

            # break after no_improv_break iterations with no improvement
            self.log_info_signal.emit('...best so far: {}'.format(best))
            
            

            if best < prev_best - no_improve_thr:
                no_improv = 0
                prev_best = best
            else:
                no_improv += 1

            if no_improv >= no_improv_break:
                self.log_info_signal.emit('...best so far: {}'.format(best))
                self.log_info_signal.emit('stop because no improvement')

                if not self.TEST_MODE:
                    with open('log/iter{}.csv'.format(iters), 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(self.csv_data)

                return self.pop[0]

            # centroid
            x0 = [0.] * dim
            for tup in self.pop[:-1]:
                for i, c in enumerate(tup):
                    x0[i] += c / (len(self.pop)-1)

            # reflection
            xr = x0 + alpha*(x0 - self.pop[-1])
            xr = np.clip(xr, 0, 1)

            xr = self.min_b + xr * self.diff #denorm
            xr = self.round_nearest(xr)
            self.param_value[self.param_change_idx] = xr
            xr = ((xr-self.min_b)/self.diff) #norm

            now_IQM = self.measure_IQM_by_param_value('log/iter_{}_reflection'.format(iters), self.param_value)
            rscore = self.cal_score_by_weight(now_IQM)

            data = ["iter_{}_reflection".format(iters), rscore]
            for IQM in now_IQM: data.append(IQM)
            data.append(self.param_value.copy())
            self.csv_data.append(data)

            if self.fitness[0] <= rscore < self.fitness[-2]:
                del self.pop[-1]
                del self.fitness[-1]
                self.pop.append(xr)
                self.fitness.append(rscore)
                self.update_param_window_signal.emit(self.param_change_num, self.param_value[self.param_change_idx], rscore, now_IQM)
                continue

            # expansion
            if rscore < self.fitness[0]:
                xe = x0 + gamma*(x0 - self.pop[-1])
                xe = np.clip(xe, 0, 1)

                xe = self.min_b + xe * self.diff #denorm
                xe = self.round_nearest(xe)
                self.param_value[self.param_change_idx] = xe
                xe = ((xe-self.min_b)/self.diff) #norm

                now_IQM = self.measure_IQM_by_param_value('log/iter_{}_expansion'.format(iters), self.param_value)
                escore = self.cal_score_by_weight(now_IQM)

                data = ["iter_{}_expansion".format(iters), escore]
                for IQM in now_IQM: data.append(IQM)
                data.append(self.param_value.copy())
                self.csv_data.append(data)

                if escore < rscore:
                    del self.pop[-1]
                    del self.fitness[-1]
                    self.pop.append(xe)
                    self.fitness.append(escore)
                    # del res[-1]
                    # res.append([xe, escore])
                    self.update_param_window_signal.emit(self.param_change_num, self.param_value[self.param_change_idx], escore, now_IQM)
                    continue
                else:
                    del self.pop[-1]
                    del self.fitness[-1]
                    self.pop.append(xr)
                    self.fitness.append(rscore)
                    # del res[-1]
                    # res.append([xr, rscore])
                    self.update_param_window_signal.emit(self.param_change_num, self.param_value[self.param_change_idx], rscore, now_IQM)
                    continue

            # contraction
            xc = x0 + rho*(x0 -self.pop[-1])
            xc = np.clip(xc, 0, 1)

            xc = self.min_b + xc * self.diff #denorm
            xc = self.round_nearest(xc)
            self.param_value[self.param_change_idx] = xc
            xc = ((xc-self.min_b)/self.diff) #norm

            now_IQM = self.measure_IQM_by_param_value('log/iter_{}_contraction'.format(iters), self.param_value)
            cscore = self.cal_score_by_weight(now_IQM)

            data = ["iter_{}_contraction".format(iters), cscore]
            for IQM in now_IQM: data.append(IQM)
            data.append(self.param_value.copy())
            self.csv_data.append(data)

            if cscore < self.fitness[-1]:
                del self.pop[-1]
                del self.fitness[-1]
                self.pop.append(xc)
                self.fitness.append(cscore)
                # del res[-1]
                # res.append([xc, cscore])
                self.update_param_window_signal.emit(self.param_change_num, self.param_value[self.param_change_idx], cscore, now_IQM)
                continue

            # reduction
            x1 = self.pop[0]
            nres = []
            for tup_i, tup in enumerate(self.pop[0]):
                redx = x1 + sigma*(tup - x1)
                redx = np.clip(redx, 0, 1)

                redx = self.min_b + redx * self.diff #denorm
                redx = self.round_nearest(redx)
                self.param_value[self.param_change_idx] = redx
                redx = ((redx-self.min_b)/self.diff) #norm

                self.param_value[self.param_change_idx] = self.min_b + redx * self.diff #denorm
                now_IQM = self.measure_IQM_by_param_value('log/iter_{}_reduction_{}'.format(iters, tup_i), self.param_value)
                score = self.cal_score_by_weight(now_IQM)

                data = ["iter_{}_reduction_{}".format(iters, tup_i), score]
                for IQM in now_IQM: data.append(IQM)
                data.append(self.param_value.copy())
                self.csv_data.append(data)

                nres.append([redx, score])
                self.update_param_window_signal.emit(tup_i, self.param_value[self.param_change_idx], score, now_IQM)

            res = nres

    def initial_individual(self):
        
        self.set_generation_signal.emit("initialize")

        # initial individual
        for ind_idx in range(self.popsize):
            self.set_individual_signal.emit(str(ind_idx))
            self.log_info_signal.emit('\ninitial individual: {}'.format(ind_idx))

            # denormalize to [min_b, max_b]
            trial_denorm = self.min_b + self.pop[ind_idx] * self.diff
            # update param_value
            self.param_value[self.param_change_idx] = trial_denorm
            # measure score
            now_IQM = self.measure_IQM_by_param_value('log/ind{}_init'.format(ind_idx), self.param_value)
            score = np.around(self.cal_score_by_weight(now_IQM), 9)
            self.fitness.append(score)
            self.IQMs.append(now_IQM)

            # update_param_window
            self.update_param_window_signal.emit(ind_idx, trial_denorm, self.fitness[ind_idx], now_IQM)
            
            if not self.TEST_MODE:
                # csv data
                data = ["ind{}_init".format(ind_idx), score]
                for IQM in now_IQM: data.append(IQM)
                data.append(self.param_value.copy())
                self.csv_data.append(data)
                self.best_csv_data.append(data)


        self.IQMs = np.array(self.IQMs)
        # 暫時設成1
        # self.std_IQM = self.IQMs.std(axis=0)

        # 依據標準差重新計算
        for ind_idx in range(self.popsize):
            self.fitness[ind_idx] = np.around(self.cal_score_by_weight(self.IQMs[ind_idx]), 5)
            if not self.TEST_MODE:
                self.csv_data[ind_idx+2][1] = self.fitness[ind_idx]
                self.best_csv_data[ind_idx+2][1] = self.fitness[ind_idx]

            # 將圖片複製到best資料夾
            if not self.TEST_MODE:
                for i in range(self.capture_num):
                    if self.capture_num==1:
                        src_img = 'ind{}_init.jpg'.format(ind_idx)
                        des_img = '{}.jpg'.format(ind_idx) 
                        
                    else:
                        src_img = 'ind{}_{}_init.jpg'.format(ind_idx, i)
                        des_img = '{}_{}.jpg'.format(ind_idx, i) 

                    src='log/{}'.format(src_img)
                    des='best_photo/{}'.format(des_img) 

                    if os.path.exists(des): os.remove(des)
                    shutil.copyfile(src, des)

        # 更新經由標準差後的分數
        self.update_param_window_scores_signal.emit(self.fitness)

        if not self.TEST_MODE:
            with open('log/init.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.csv_data)

            with open('best_photo/init.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.best_csv_data)

    def run_DE_for_a_generation(self, gen_idx):
        self.set_generation_signal.emit(str(gen_idx))

        # create dir
        gen_dir = 'generation{}'.format(gen_idx)

        # update hyperparam
        F = self.F
        Cr = self.Cr

        self.update_count=0

        for ind_idx in range(self.popsize):
            self.run_DE_for_a_individual(F, Cr, gen_idx, ind_idx, gen_dir)
        
        self.update_rate=self.update_count/self.popsize

        if not self.TEST_MODE:
            with open('log/gen{}.csv'.format(gen_idx), 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.csv_data)

            with open('best_photo/gen{}.csv'.format(gen_idx), 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.best_csv_data)
        
    def run_DE_for_a_individual(self, F, Cr, gen_idx, ind_idx, gen_dir):
        self.set_individual_signal.emit(str(ind_idx))

        is_return, trial, trial_denorm = self.generate_parameters(ind_idx, F, Cr)
        if(is_return): 
            self.log_info_signal.emit('return because no generate new parameters')
            return
        
        # update param_value
        self.param_value[self.param_change_idx] = trial_denorm

        # mesure score
        now_IQM = self.measure_IQM_by_param_value('log/ind{}_gen{}'.format(ind_idx, gen_idx), self.param_value)
        f = np.around(self.cal_score_by_weight(now_IQM), 9)

        data = ['ind{}_gen{}'.format(ind_idx, gen_idx), f]
        for IQM in now_IQM: data.append(IQM)
        data.append(self.param_value.copy())
        self.csv_data.append(data)

        # self.log_info_signal.emit('pre score: {}'.format(self.fitness[ind_idx]))
        # self.log_info_signal.emit('now score: {}'.format(f))

        # 如果突變種比原本的更好
        if f < self.fitness[ind_idx]:
            # update_param_window
            self.update_param_window_signal.emit(ind_idx, trial_denorm, f, now_IQM)
            
            self.update_count+=1

            # 替換原本的個體
            self.log_info_signal.emit('replace with better score {}'.format(f))
            self.set_statusbar_signal.emit('generation {} individual {} replace with better score'.format(gen_dir, ind_idx))
            
            self.fitness[ind_idx] = f
            self.IQMs[ind_idx] = now_IQM
            self.pop[ind_idx] = trial

            # 將圖片複製到best資料夾
            if not self.TEST_MODE:
                self.best_csv_data[ind_idx+2] = data
                for i in range(self.capture_num):
                    if self.capture_num==1:
                        src_img = 'ind{}_gen{}.jpg'.format(ind_idx, gen_idx)
                        des_img = '{}.jpg'.format(ind_idx) # 根據量化分數命名
                        
                    else:
                        src_img = 'ind{}_{}_gen{}.jpg'.format(ind_idx, i, gen_idx)
                        des_img = '{}_{}.jpg'.format(ind_idx, i) # 根據量化分數命名

                    src='log/{}'.format(src_img)
                    des='best_photo/{}'.format(des_img) # 根據量化分數命名

                    if os.path.exists(des): os.remove(des)
                    shutil.copyfile(src, des)

        self.hyper_param_plot.update([F, Cr])
        self.update_rate_plot.update([self.update_rate])

    # def is_bad_trial(self, trial_denorm):
    #     for rule in self.rule:
    #         val = 0
    #         p0 = trial_denorm[rule["idx"][0]]
    #         p1 = trial_denorm[rule["idx"][1]]

    #         for op in rule["op"]:
    #             if op == '-': val = p0-p1
    #             elif op == 'abs': val = np.abs(val)

    #         if not (rule["between"][0]<=val and val<=rule["between"][1]):
    #             if val>rule["between"][1]: dif = -(val-rule["between"][1])
    #             if val<rule["between"][0]: dif = (val-rule["between"][0])
    #             p = math.exp(dif/self.T) # 差越大p越小，越容易傳True
    #             if p<np.random.uniform(0.5, 0.8): 
    #                 self.log_info_signal.emit("bad param")
    #                 return True # p越小越容易比他大
        
    #     self.T *= self.T_rate
        
    #     return False

    def round_nearest(self, x):
        return np.around(self.step*np.around(x/self.step), 2)

    def generate_parameters(self, ind_idx, F, Cr):
        mutant = None
        times = 0
        while (not isinstance(mutant, np.ndarray) or (np.abs(trial_denorm-now_denorm)<=1e-5).all()):
            Cr+=0.1
            # select all pop except j
            idxs = [idx for idx in range(self.popsize) if idx != ind_idx]
            # random select three pop except j
            a, b, c = self.pop[np.random.choice(idxs, 3, replace=False)]
            # self.log_info_signal.emit('{}, {}'.format(b, c))
            vec = F * (b - c)
            # Mutation
            mutant = np.clip(a + vec, 0, 1)

            # random choose the dimensions
            cross_points = np.random.rand(self.param_change_num) < Cr
            # if no dimensions be selected
            if not np.any(cross_points):
                # random choose one dimensions
                cross_points[np.random.randint(0, self.param_change_num)] = True

            # random substitution mutation
            trial = np.where(cross_points, mutant, self.pop[ind_idx])

            # denormalize to [min_b, max_b]
            trial_denorm = self.min_b + trial * self.diff
            trial_denorm = self.round_nearest(trial_denorm)

            now_denorm = self.min_b + self.pop[ind_idx] * self.diff
            now_denorm = self.round_nearest(now_denorm)

            times+=1
            if times>20: 
                self.log_info_signal.emit("generate_times: {}".format(times))
                return True, [], []

        self.log_info_signal.emit("generate_times: {}".format(times))
        trial = (trial_denorm-self.min_b)/self.diff

        return False, trial, trial_denorm

    def update_best_score(self, score):
        # update log score
        self.best_score = np.round(score, 9)
        self.set_score_signal.emit(str(self.best_score))
            
        

    def measure_IQM_by_param_value(self, path, param_value):
        self.log_info_signal.emit('now param_value: {}'.format(param_value))
        if self.TEST_MODE: 
            return np.array([self.fobj(param_value)]*len(self.target_type))

        # write param_value to xml
        self.set_param_value[self.platform](self.key, self.key_config, self.file_path, self.trigger_idx, param_value)

        # compile project using bat. push bin code to camera
        self.log_info_signal.emit('push bin to camera...')
        self.run_cmd_signal.emit('adb shell input keyevent = KEYCODE_HOME')
        self.build_and_push[self.platform](self.logger, self.exe_path, self.project_path, self.bin_name)
        self.capture.clear_camera_folder()
        self.log_info_signal.emit('wait for reboot camera...')
        
        sleep(6)

        # 拍照
        self.capture.capture(path, capture_num=self.capture_num)

        # 計算分數
        now_IQM = self.measure_score_by_multiple_capture(path)
        
        return now_IQM

    def measure_score_by_multiple_capture(self, path):
        IQM_scores = []
        # print("\n---------IQM score--------\n")
        for i in range(self.capture_num):
            # 讀取image檔案
            if self.capture_num==1: p = str(path+".jpg")
            else: p = path+"_"+str(i)+".jpg"
            img = cv2.imread(p, cv2.IMREAD_COLOR)
            IQM_scores.append(self.calIQM(img))
            # print(i, IQM_scores[i])

        IQM_scores = np.array(IQM_scores)
        zscore = stats.zscore(IQM_scores)
        # print("\n---------zscore--------\n")
        # for i in range(capture_num):
        # print(i, zscore[i])
        select = (np.abs(zscore) < 1).all(axis=1)
        # print(select)

        # print("\n---------after drop outlier => [abs(zscore) > 1]--------\n")
        if (select == True).any():
            IQM_scores = IQM_scores[select]
        # print(IQM_scores)

        # 計算分數
        now_IQM = np.mean(IQM_scores, axis=0)
        return now_IQM

    def calIQM(self, img):
        now_IQM=[]
        for i, roi in enumerate(self.my_rois):
            if len(roi)==0: continue
            x, y, w, h = roi
            my_roi_img = img[y: y+h, x:x+w]

            if self.target_type[i] == "perceptual distance":
                my_roi_img_resize, target_roi_img_resize = resize_by_h(my_roi_img, self.target_roi_imgs[i][1])
                v = self.calFunc[self.target_type[i]](my_roi_img_resize, target_roi_img_resize )
            else:
                v = self.calFunc[self.target_type[i]](my_roi_img)
            now_IQM.append(v)
        
        now_IQM = np.array(now_IQM)
        return now_IQM

    def cal_score_by_weight(self, now_IQM):
        if self.TEST_MODE: 
            score = np.mean(now_IQM)
        else:
            dif_min = np.abs(self.target_IQM_min-now_IQM)
            dif_max = np.abs(self.target_IQM_max-now_IQM)
            dif = np.array([dif_min, dif_max]).min(axis=0)
            score = (dif/self.std_IQM).dot(self.weight_IQM.T)
        if score<self.best_score: 
            self.best_score = score
            self.update_best_score(self.best_score)
        self.best_score_plot.update([self.best_score])
        return score

    def mkdir(self, path):
        if self.TEST_MODE: 
            print('mkdir {} return because TEST_MODE'.format(path))
            return
        if not os.path.exists(path):
            os.makedirs(path)
            print("The", path, "dir is created!")

    def setup(self):
        # reset plot
        self.best_score_plot.reset()
        self.hyper_param_plot.reset()
        self.update_rate_plot.reset()

        # reset label
        self.set_score_signal.emit("#")
        self.set_generation_signal.emit("#")
        self.set_individual_signal.emit("#")

    # Ackley
    # objective function
    def fobj(self, X):
        firstSum = 0.0
        secondSum = 0.0
        for c in X:
            firstSum += c**2.0
            secondSum += math.cos(2.0*math.pi*c)
        n = float(len(X))
        return -20.0*math.exp(-0.2*math.sqrt(firstSum/n)) - math.exp(secondSum/n) + 20 + math.e

    def show_info_by_key(self, key, data):
        for k in key:
            self.tab_info.show_info("{}: {}".format(k,data[k]))

    def show_info(self):
        # show info
        self.tab_info.label.setAlignment(Qt.AlignLeft)
        self.tab_info.clear()

        key_config = self.config[self.setting["platform"]][self.setting["root"]][self.setting["key"]]
        key_data = self.setting[self.setting["root"]][self.setting["key"]]

        self.tab_info.show_info("\n###### Target ######")
        self.show_info_by_key(["target_type", "target_score_min", "target_score_max", "target_weight"], self.setting)

        self.tab_info.show_info("\n###### Tuning Block ######")
        self.show_info_by_key(["root", "key"], self.setting)
        self.show_info_by_key(["trigger_idx", "trigger_name"], self.setting)

        self.tab_info.show_info("\n###### Algorithm ######")
        self.show_info_by_key(["method"], self.setting)

        if self.setting["method"] == "global search":
            self.show_info_by_key(["population size","generations","capture num"], self.setting)
        elif self.setting["method"] == "local search":
            self.show_info_by_key(["init_param", "capture num"], self.setting)

        self.show_info_by_key(["coustom_range","param_change_idx"], key_data)
        self.tab_info.show_info("{}: {}".format("param_value", self.param_value))

        self.tab_info.show_info("\n###### Project Setting ######")
        self.show_info_by_key(["platform", "project_path", "exe_path", "bin_name"], self.setting)

    def finish(self):
        if self.TEST_MODE: return
        now = datetime.datetime.now() # current date and time
        dir_name = "Result_{}".format(now.strftime("%Y%m%d_%H%M"))
        self.mkdir(dir_name)

        # 搬移目標照片
        for i, target in enumerate(self.target_rois):
            src = target[0]
            des='{}/{}'.format(dir_name, src.split('/')[-1])
            if not os.path.exists(des):
                shutil.copyfile(src, des)

        # 搬移ROI照片
        for i, target in enumerate(self.target_roi_imgs):
            cv2.imwrite("{}/target_ROI{}_{}.jpg".format(dir_name, i+1, target[0]), target[1])

        # 搬移前五名的照片 
        self.csv_data[1:] = sorted(self.csv_data[1:], key=lambda x: x[1])
        self.csv_data = self.csv_data[:6]
        for i, data in enumerate(self.csv_data):
            if i>=2: # 0 1 is title target
                src = "log/{}.jpg".format(data[0])
                des = "{}/{}.jpg".format(dir_name, i-1)
                shutil.copyfile(src, des)
                data[0] = "{}.jpg".format(i-1)
                
        # 儲存csv
        with open('{}/result.csv'.format(dir_name), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.csv_data)

        self.run_cmd_signal.emit('adb shell input keyevent = KEYCODE_HOME')

    
