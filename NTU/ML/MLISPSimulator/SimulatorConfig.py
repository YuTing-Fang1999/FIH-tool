# \Chromatix\Scenario.Default\Sensor.0\Usecase.Snapshot\Feature1.None\Feature2.MMFPostFilter\XML\IPE\

class SimulatorConfig():
    def __init__(self) -> None:
        self.config = \
        {
            "c7_config":{
                "gen_num": 200,
                "modify_key": ["ANR","ASF"],
                "tune_key": ["ANR","ASF"],
                "ISP":{
                    "ANR": {
                        "file_path": "/Chromatix/oem/qcom/tuning/sm8550_shinetech_s5kgnksp03/Scenario.Default/Sensor.0/Usecase.Snapshot/Feature1.None/Feature2.MMFPostFilter/XML/IPE/anr14_ipe_v2.xml",
                        "enable_tag": [".//enable_luma_noise_reduction[1]", ".//enable_chroma_noise_reduction[1]"],
                        "tag": {
                            # FULL PASS
                            "FULL_PASS_luma_filter_detection_thresholds_y_threshold_per_y": {
                                "path": [
                                    [".//region", 4, ".//anr14_rgn_data", 0, ".//luma_filter_detection_thresholds", 0 ,".//y_threshold_per_y", 0],
                                    [".//region", 5, ".//anr14_rgn_data", 0, ".//luma_filter_detection_thresholds", 0 ,".//y_threshold_per_y", 0],
                                ],
                                "units": [1],
                                "bounds": [[0, 30]]
                            },
                            "FULL_PASS_luma_filter_detection_thresholds_u_threshold_per_y": {
                                "path": [
                                    [".//region", 4, ".//anr14_rgn_data", 0, ".//luma_filter_detection_thresholds", 0 ,".//u_threshold_per_y", 0],
                                    [".//region", 5, ".//anr14_rgn_data", 0, ".//luma_filter_detection_thresholds", 0 ,".//u_threshold_per_y", 0],
                                ],
                                "units": [1],
                                "bounds": [[0, 30]]
                            },
                            "FULL_PASS_luma_filter_detection_thresholds_v_threshold_per_y": {
                                "path": [
                                    [".//region", 4, ".//anr14_rgn_data", 0, ".//luma_filter_detection_thresholds", 0 ,".//v_threshold_per_y", 0],
                                    [".//region", 5, ".//anr14_rgn_data", 0, ".//luma_filter_detection_thresholds", 0 ,".//v_threshold_per_y", 0],
                                ],
                                "units": [1],
                                "bounds": [[0, 30]]
                            },
                            "FULL_PASS_chroma_filter_detection_thresholds_y_threshold_per_y": {
                                "path": [
                                    [".//region", 4, ".//anr14_rgn_data", 0, ".//chroma_filter_detection_thresholds", 0, ".//y_threshold_per_y", 0],
                                    [".//region", 5, ".//anr14_rgn_data", 0, ".//chroma_filter_detection_thresholds", 0, ".//y_threshold_per_y", 0],
                                ],
                                "units": [1],
                                "bounds": [[0, 30]]
                            },
                            "FULL_PASS_chroma_filter_detection_thresholds_u_threshold_per_y": {
                                "path": [
                                    [".//region", 4, ".//anr14_rgn_data", 0, ".//chroma_filter_detection_thresholds", 0, ".//u_threshold_per_y", 0],
                                    [".//region", 5, ".//anr14_rgn_data", 0, ".//chroma_filter_detection_thresholds", 0, ".//u_threshold_per_y", 0],
                                ],
                                "units": [1],
                                "bounds": [[0, 30]]
                            },
                            "FULL_PASS_chroma_filter_detection_thresholds_v_threshold_per_y": {
                                "path": [
                                    [".//region", 4, ".//anr14_rgn_data", 0, ".//chroma_filter_detection_thresholds", 0, ".//v_threshold_per_y", 0],
                                    [".//region", 5, ".//anr14_rgn_data", 0, ".//chroma_filter_detection_thresholds", 0, ".//v_threshold_per_y", 0],
                                ],
                                "units": [1],
                                "bounds": [[0, 30]]
                            },
                        }
                    },
                    "ASF": {
                        "file_path": "/Chromatix/oem/qcom/tuning/sm8550_shinetech_s5kgnksp03/Scenario.Default/Sensor.0/Usecase.Snapshot/Feature1.None/Feature2.MMFPostFilter/XML/IPE/asf35_ipe_v2.xml",
                        "enable_tag": [".//asf_enable[1]"],
                        "tag": {
                            "layer_1_hpf_symmetric_coeff": {
                                "path": [
                                    [".//layer_1_hpf_symmetric_coeff[1]", 4],
                                    [".//layer_1_hpf_symmetric_coeff[1]", 5],
                                    [".//layer_1_hpf_symmetric_coeff[1]", 12],
                                    [".//layer_1_hpf_symmetric_coeff[1]", 13],
                                    [".//layer_1_hpf_symmetric_coeff[1]", 19],
                                    [".//layer_1_hpf_symmetric_coeff[1]", 20],
                                ],
                                "units": [1],
                                "bounds": [
                                    [
                                        0, # thin kernel 
                                        1  # mid kernel 
                                    ],
                                ]
                            },
                            "layer_1_gain_positive_lut":{
                                "path": [
                                    [".//layer_1_gain_positive_lut[1]", 4],
                                    [".//layer_1_gain_positive_lut[1]", 5],
                                    [".//layer_1_gain_positive_lut[1]", 12],
                                    [".//layer_1_gain_positive_lut[1]", 13],
                                    [".//layer_1_gain_positive_lut[1]", 19],
                                    [".//layer_1_gain_positive_lut[1]", 20],
                                ],
                                "units": [1, 1, 1],
                                "bounds": [
                                    [
                                        2,
                                        28
                                    ],
                                    [
                                        0,
                                        30
                                    ],
                                    [
                                        0,
                                        15
                                    ],
                                ]
                            },
                            "layer_1_gain_negative_lut":{
                                "path": [
                                    [".//layer_1_gain_negative_lut[1]", 4],
                                    [".//layer_1_gain_negative_lut[1]", 5],
                                    [".//layer_1_gain_negative_lut[1]", 12],
                                    [".//layer_1_gain_negative_lut[1]", 13],
                                    [".//layer_1_gain_negative_lut[1]", 19],
                                    [".//layer_1_gain_negative_lut[1]", 20],
                                ],
                            },
                            "layer_1_clamp_ul":{
                                "path": [
                                    [".//layer_1_clamp_ul[1]", 4],
                                    [".//layer_1_clamp_ul[1]", 5],
                                    [".//layer_1_clamp_ul[1]", 12],
                                    [".//layer_1_clamp_ul[1]", 13],
                                    [".//layer_1_clamp_ul[1]", 19],
                                    [".//layer_1_clamp_ul[1]", 20],
                                ],
                                "units": [5],
                                "bounds": [
                                    [
                                        0,
                                        255
                                    ],
                                ]
                            },
                            "layer_1_clamp_ll":{
                                "path": [
                                    [".//layer_1_clamp_ll[1]", 4],
                                    [".//layer_1_clamp_ll[1]", 5],
                                    [".//layer_1_clamp_ll[1]", 12],
                                    [".//layer_1_clamp_ll[1]", 13],
                                    [".//layer_1_clamp_ll[1]", 19],
                                    [".//layer_1_clamp_ll[1]", 20],
                                ],
                            },
                            "layer_1_gain_weight_lut":{
                                "path": [
                                    [".//layer_1_gain_weight_lut[1]", 4],
                                    [".//layer_1_gain_weight_lut[1]", 5],
                                    [".//layer_1_gain_weight_lut[1]", 12],
                                    [".//layer_1_gain_weight_lut[1]", 13],
                                    [".//layer_1_gain_weight_lut[1]", 19],
                                    [".//layer_1_gain_weight_lut[1]", 20],
                                ],
                                "units": [1, 0.05],
                                "bounds": [
                                    [
                                        1,
                                        10
                                    ],
                                    [
                                        0,
                                        0.5
                                    ],
                                ]
                            },
                            "layer_2_gain_positive_lut":{
                                "path": [
                                    [".//layer_2_gain_positive_lut[1]", 4],
                                    [".//layer_2_gain_positive_lut[1]", 5],
                                    [".//layer_2_gain_positive_lut[1]", 12],
                                    [".//layer_2_gain_positive_lut[1]", 13],
                                    [".//layer_2_gain_positive_lut[1]", 19],
                                    [".//layer_2_gain_positive_lut[1]", 20],
                                ],
                                "units": [1, 1, 1],
                                "bounds": [
                                    [
                                        2,
                                        28
                                    ],
                                    [
                                        0,
                                        30
                                    ],
                                    [
                                        0,
                                        15
                                    ],
                                ]
                            },
                            "layer_2_gain_negative_lut":{
                                "path": [
                                    [".//layer_2_gain_negative_lut[1]", 4],
                                    [".//layer_2_gain_negative_lut[1]", 5],
                                    [".//layer_2_gain_negative_lut[1]", 12],
                                    [".//layer_2_gain_negative_lut[1]", 13],
                                    [".//layer_2_gain_negative_lut[1]", 19],
                                    [".//layer_2_gain_negative_lut[1]", 20],
                                ],
                            },
                            "layer_2_clamp_ul":{
                                "path": [
                                    [".//layer_2_clamp_ul[1]", 4],
                                    [".//layer_2_clamp_ul[1]", 5],
                                    [".//layer_2_clamp_ul[1]", 12],
                                    [".//layer_2_clamp_ul[1]", 13],
                                    [".//layer_2_clamp_ul[1]", 19],
                                    [".//layer_2_clamp_ul[1]", 20],
                                ],
                                "units": [5],
                                "bounds": [
                                    [
                                        0,
                                        255
                                    ],
                                ]
                            },
                            "layer_2_clamp_ll":{
                                "path": [
                                    [".//layer_2_clamp_ll[1]", 4],
                                    [".//layer_2_clamp_ll[1]", 5],
                                    [".//layer_2_clamp_ll[1]", 12],
                                    [".//layer_2_clamp_ll[1]", 13],
                                    [".//layer_2_clamp_ll[1]", 19],
                                    [".//layer_2_clamp_ll[1]", 20],
                                ],
                            },
                            "layer_2_gain_weight_lut":{
                                "path": [
                                    [".//layer_2_gain_weight_lut[1]", 4],
                                    [".//layer_2_gain_weight_lut[1]", 5],
                                    [".//layer_2_gain_weight_lut[1]", 12],
                                    [".//layer_2_gain_weight_lut[1]", 13],
                                    [".//layer_2_gain_weight_lut[1]", 19],
                                    [".//layer_2_gain_weight_lut[1]", 20],
                                ],
                                "units": [1, 0.05],
                                "bounds": [
                                    [
                                        1,
                                        10
                                    ],
                                    [
                                        0,
                                        0.5
                                    ],
                                ]
                            },
                        }
                    },
                }
            }
        }