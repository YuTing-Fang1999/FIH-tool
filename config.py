main_config = \
[
    { 
        "MTK":[
            {
                "name":"MTK0",
                "btn_list":[
                    {
                        "name": "b0",
                        "widget": 1
                    },
                    {
                        "btn_name": "b0",
                        "widget": 2
                    },
                ]
            },
        ]
    }
]

for each_config in main_config:
    print(list(each_config.keys())[0])
