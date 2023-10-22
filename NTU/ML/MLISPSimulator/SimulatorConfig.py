# \Chromatix\Scenario.Default\Sensor.0\Usecase.Snapshot\Feature1.None\Feature2.MMFPostFilter\XML\IPE\

class SimulatorConfig():
    def __init__(self) -> None:
        self.config = \
        {
            "c7_config":{
                "gen_num": 100,
                "ISP":{
                    "ASF": {
                        "file_path": "/Chromatix/Scenario.Default/Sensor.0/Usecase.Snapshot/Feature1.None/Feature2.MMFPostFilter/XML/IPE/asf35_ipe_v2.xml",
                        "enable_tag": [".//asf_enable[1]"],
                        "tag": {
                            "layer_1_hpf_symmetric_coeff": {
                                "path": [".//layer_1_hpf_symmetric_coeff[1]"],
                                "units": [1],
                                "bounds": [
                                    [
                                        0, # thin kernel 
                                        1  # mid kernel 
                                    ],
                                ]
                            },
                            "layer_1_gain_positive_lut":{
                                "path": [".//layer_1_gain_positive_lut[1]"],
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
                                "path": [".//layer_1_gain_negative_lut[1]"],
                            },
                            "layer_1_clamp_ul":{
                                "path": [".//layer_1_clamp_ul[1]"],
                                "units": [5],
                                "bounds": [
                                    [
                                        0,
                                        255
                                    ],
                                ]
                            },
                            "layer_1_clamp_ll":{
                                "path": [".//layer_1_clamp_ll[1]"],
                            },
                            "layer_1_gain_weight_lut":{
                                "path": [".//layer_1_gain_weight_lut[1]"],
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
                                "path": [".//layer_2_gain_positive_lut[1]"],
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
                                "path": [".//layer_2_gain_negative_lut[1]"],
                            },
                            "layer_2_clamp_ul":{
                                "path": [".//layer_2_clamp_ul[1]"],
                                "units": [5],
                                "bounds": [
                                    [
                                        0,
                                        255
                                    ],
                                ]
                            },
                            "layer_2_clamp_ll":{
                                "path": [".//layer_2_clamp_ll[1]"],
                            },
                            "layer_2_gain_weight_lut":{
                                "path": [".//layer_2_gain_weight_lut[1]"],
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
                    # "ANR": {
                    #     "file_path": "/Chromatix/Scenario.Default/Sensor.0/Usecase.Snapshot/Feature1.None/Feature2.MMFPostFilter/XML/IPE/anr14_ipe_v2.xml",
                    #     "enable_tag": [".//enable_luma_noise_reduction[1]", ".//enable_chroma_noise_reduction[1]"],
                    #     "tag": {
                    #         # FULL PASS
                    #         "luma_filter_detection_thresholds_y_threshold_per_y": {
                    #             "path": [".//anr14_rgn_data[1]", ".//luma_filter_detection_thresholds[1]",".//y_threshold_per_y[1]"],
                    #             "units": [1] * 17,
                    #             "bounds": [[0, 30]] * 17
                    #         },
                    #         "luma_filter_detection_thresholds_u_threshold_per_y": {
                    #             "path": [".//anr14_rgn_data[1]", ".//luma_filter_detection_thresholds[1]",".//u_threshold_per_y[1]"],
                    #             "units": [1] * 17,
                    #             "bounds": [[0, 30]] * 17
                    #         },
                    #         "luma_filter_detection_thresholds_v_threshold_per_y": {
                    #             "path": [".//anr14_rgn_data[1]", ".//luma_filter_detection_thresholds[1]",".//v_threshold_per_y[1]"],
                    #             "units": [1] * 17,
                    #             "bounds": [[0, 30]] * 17
                    #         },
                    #         "chroma_filter_detection_thresholds_y_threshold_per_y": {
                    #             "path": [".//anr14_rgn_data[1]", ".//chroma_filter_detection_thresholds[1]",".//y_threshold_per_y[1]"],
                    #             "units": [1] * 17,
                    #             "bounds": [[0, 30]] * 17
                    #         },
                    #         "chroma_filter_detection_thresholds_u_threshold_per_y": {
                    #             "path": [".//anr14_rgn_data[1]", ".//chroma_filter_detection_thresholds[1]",".//u_threshold_per_y[1]"],
                    #             "units": [1] * 17,
                    #             "bounds": [[0, 30]] * 17
                    #         },
                    #         "chroma_filter_detection_thresholds_v_threshold_per_y": {
                    #             "path": [".//anr14_rgn_data[1]", ".//chroma_filter_detection_thresholds[1]",".//v_threshold_per_y[1]"],
                    #             "units": [1] * 17,
                    #             "bounds": [[0, 30]] * 17
                    #         },
                    #     },
                    # },
                }
                
            }
        }