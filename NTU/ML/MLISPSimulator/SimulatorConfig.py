# \Chromatix\Scenario.Default\Sensor.0\Usecase.Snapshot\Feature1.None\Feature2.MMFPostFilter\XML\IPE\

class SimulatorConfig():
    def __init__(self) -> None:
        self.config = \
        {
            "c7_config":{
                "gen_num": 200,
                "ISP":{
                    "ANR": {
                        "file_path": "/Chromatix/oem/qcom/tuning/sm8550_shinetech_s5kgnksp03/Scenario.Default/Sensor.0/Usecase.Snapshot/Feature1.None/Feature2.MMFPostFilter/XML/IPE/anr14_ipe_v2.xml",
                        "enable_tag": [".//enable_luma_noise_reduction[1]", ".//enable_chroma_noise_reduction[1]"],
                        "tag": {
                            # FULL PASS
                            "FULL_PASS_luma_filter_detection_thresholds_y_threshold_per_y": {
                                "path": [
                                    ['.//y_threshold_per_y', 32],
                                    ['.//y_threshold_per_y', 40]
                                ],
                                "units": [1],
                                "bounds": [[0, 30]]
                            },
                            "FULL_PASS_chroma_filter_detection_thresholds_y_threshold_per_y": {
                                "path": [
                                    ['.//y_threshold_per_y', 33],
                                    ['.//y_threshold_per_y', 41]
                                ],
                                "units": [1],
                                "bounds": [[0, 30]]
                            },
                            "FULL_PASS_luma_filter_detection_thresholds_u_threshold_per_y": {
                                "path": [
                                    ['.//u_threshold_per_y', 32],
                                    ['.//u_threshold_per_y', 40]
                                ],
                                "units": [1],
                                "bounds": [[0, 30]]
                            },
                            "FULL_PASS_chroma_filter_detection_thresholds_u_threshold_per_y": {
                                "path": [
                                   ['.//u_threshold_per_y', 33],
                                   ['.//u_threshold_per_y', 41]
                                ],
                                "units": [1],
                                "bounds": [[0, 30]]
                            },
                            "FULL_PASS_luma_filter_detection_thresholds_v_threshold_per_y": {
                                "path": [
                                   ['.//v_threshold_per_y', 32],
                                   ['.//v_threshold_per_y', 40]
                                ],
                                "units": [1],
                                "bounds": [[0, 30]]
                            },
                            "FULL_PASS_chroma_filter_detection_thresholds_v_threshold_per_y": {
                                "path": [
                                   ['.//v_threshold_per_y', 33],
                                   ['.//v_threshold_per_y', 41]
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
                                    [".//layer_1_hpf_symmetric_coeff", 4],
                                    [".//layer_1_hpf_symmetric_coeff", 5],
                                    [".//layer_1_hpf_symmetric_coeff", 12],
                                    [".//layer_1_hpf_symmetric_coeff", 13],
                                    [".//layer_1_hpf_symmetric_coeff", 19],
                                    [".//layer_1_hpf_symmetric_coeff", 20],
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
                                    [".//layer_1_gain_positive_lut", 4],
                                    [".//layer_1_gain_positive_lut", 5],
                                    [".//layer_1_gain_positive_lut", 12],
                                    [".//layer_1_gain_positive_lut", 13],
                                    [".//layer_1_gain_positive_lut", 19],
                                    [".//layer_1_gain_positive_lut", 20],
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
                                    [".//layer_1_gain_negative_lut", 4],
                                    [".//layer_1_gain_negative_lut", 5],
                                    [".//layer_1_gain_negative_lut", 12],
                                    [".//layer_1_gain_negative_lut", 13],
                                    [".//layer_1_gain_negative_lut", 19],
                                    [".//layer_1_gain_negative_lut", 20],
                                ],
                            },
                            "layer_1_clamp_ul":{
                                "path": [
                                    [".//layer_1_clamp_ul", 4],
                                    [".//layer_1_clamp_ul", 5],
                                    [".//layer_1_clamp_ul", 12],
                                    [".//layer_1_clamp_ul", 13],
                                    [".//layer_1_clamp_ul", 19],
                                    [".//layer_1_clamp_ul", 20],
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
                                    [".//layer_1_clamp_ll", 4],
                                    [".//layer_1_clamp_ll", 5],
                                    [".//layer_1_clamp_ll", 12],
                                    [".//layer_1_clamp_ll", 13],
                                    [".//layer_1_clamp_ll", 19],
                                    [".//layer_1_clamp_ll", 20],
                                ],
                            },
                            "layer_1_gain_weight_lut":{
                                "path": [
                                    [".//layer_1_gain_weight_lut", 4],
                                    [".//layer_1_gain_weight_lut", 5],
                                    [".//layer_1_gain_weight_lut", 12],
                                    [".//layer_1_gain_weight_lut", 13],
                                    [".//layer_1_gain_weight_lut", 19],
                                    [".//layer_1_gain_weight_lut", 20],
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
                                    [".//layer_2_gain_positive_lut", 4],
                                    [".//layer_2_gain_positive_lut", 5],
                                    [".//layer_2_gain_positive_lut", 12],
                                    [".//layer_2_gain_positive_lut", 13],
                                    [".//layer_2_gain_positive_lut", 19],
                                    [".//layer_2_gain_positive_lut", 20],
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
                                    [".//layer_2_gain_negative_lut", 4],
                                    [".//layer_2_gain_negative_lut", 5],
                                    [".//layer_2_gain_negative_lut", 12],
                                    [".//layer_2_gain_negative_lut", 13],
                                    [".//layer_2_gain_negative_lut", 19],
                                    [".//layer_2_gain_negative_lut", 20],
                                ],
                            },
                            "layer_2_clamp_ul":{
                                "path": [
                                    [".//layer_2_clamp_ul", 4],
                                    [".//layer_2_clamp_ul", 5],
                                    [".//layer_2_clamp_ul", 12],
                                    [".//layer_2_clamp_ul", 13],
                                    [".//layer_2_clamp_ul", 19],
                                    [".//layer_2_clamp_ul", 20],
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
                                    [".//layer_2_clamp_ll", 4],
                                    [".//layer_2_clamp_ll", 5],
                                    [".//layer_2_clamp_ll", 12],
                                    [".//layer_2_clamp_ll", 13],
                                    [".//layer_2_clamp_ll", 19],
                                    [".//layer_2_clamp_ll", 20],
                                ],
                            },
                            "layer_2_gain_weight_lut":{
                                "path": [
                                    [".//layer_2_gain_weight_lut", 4],
                                    [".//layer_2_gain_weight_lut", 5],
                                    [".//layer_2_gain_weight_lut", 12],
                                    [".//layer_2_gain_weight_lut", 13],
                                    [".//layer_2_gain_weight_lut", 19],
                                    [".//layer_2_gain_weight_lut", 20],
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