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
                        "enable_tag": ".//asf_enable[1]",
                        "tag": {
                            "layer_1_hpf_symmetric_coeff": {
                                "idx": 1,
                                "units": [1],
                                "bounds": [
                                    [
                                        0, # thin kernel 
                                        1  # mid kernel 
                                    ],
                                ]
                            },
                            "layer_1_gain_positive_lut":{
                                "idx": 1,
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
                                "idx": 1,
                            },
                            "layer_1_clamp_ul":{
                                "idx": 1,
                                "units": [5],
                                "bounds": [
                                    [
                                        0,
                                        255
                                    ],
                                ]
                            },
                            "layer_1_clamp_ll":{
                                "idx": 1,
                            },
                            "layer_1_gain_weight_lut":{
                                "idx": 1,
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