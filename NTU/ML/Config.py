class Config():
    def __init__(self) -> None:
        self.gen_num = 50
        self.step = 0.1
        self.config = \
        {
            "c7_config":{
                "WNR": {
                    "file_path": "/Scenario.Default/XML/OPE/wnr24_ope.xml",
                    "xml_node": "chromatix_wnr24_core/mod_wnr24_post_scale_ratio_data/post_scale_ratio_data/mod_wnr24_pre_scale_ratio_data/pre_scale_ratio_data/mod_wnr24_total_scale_ratio_data/total_scale_ratio_data/mod_wnr24_drc_gain_data/drc_gain_data/mod_wnr24_hdr_aec_data/hdr_aec_data/mod_wnr24_aec_data",
                    "data_node": "wnr24_rgn_data",
                    "param_names": [
                        "denoise_weight_y",
                        "denoise_weight_chroma"
                    ],
                    "bounds": [
                        [
                            0,
                            1
                        ],
                        [
                            0,
                            1
                        ],
                        [
                            0,
                            1
                        ],
                        [
                            0,
                            0.5
                        ],
                        [
                            0,
                            0.5
                        ],
                        [
                            0,
                            0.5
                        ],
                        [
                            0,
                            0.5
                        ]
                    ],
                    "expand": None
                },
                "ASF": {
                    "file_path": "/Scenario.Default/XML/OPE/asf32_ope.xml",
                    "xml_node": "chromatix_asf32_core/mod_asf32_total_scale_ratio_data/total_scale_ratio_data/mod_asf32_drc_gain_data/drc_gain_data/mod_asf32_hdr_aec_data/hdr_aec_data/mod_asf32_aec_data",
                    "data_node": "asf32_rgn_data",
                    "param_names": [
                        "layer_1_gain_positive_lut",
                        "layer_1_gain_negative_lut"
                    ],
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
                        ]
                    ],
                    "expand": None
                },
                "ABF": {
                    "file_path": "/Scenario.Default/XML/OPE/bpcabf41_ope.xml",
                    "xml_node": "chromatix_bpcabf41_core/mod_bpcabf41_drc_gain_data/drc_gain_data/mod_bpcabf41_hdr_aec_data/hdr_aec_data/mod_bpcabf41_aec_data",
                    "data_node": "bpcabf41_rgn_data",
                    "param_names": [
                        "noise_prsv_lo",
                        "noise_prsv_hi",
                        "edge_softness"
                    ],
                    "bounds": [
                        [
                            0,
                            1
                        ],
                        [
                            0,
                            1
                        ],
                        [
                            0,
                            4
                        ]
                    ],
                    "expand":[
                        2,
                        2, 
                        1
                    ]
                }
            }
        }