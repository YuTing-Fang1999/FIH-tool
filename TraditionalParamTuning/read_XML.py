import xml.etree.ElementTree as ET
import json


xml_path = "D:/FIH/s5k3l6_c7project/Scenario.Default/XML/OPE/bpcabf41_ope.xml"
xml_node = "chromatix_bpcabf41_core/mod_bpcabf41_drc_gain_data/drc_gain_data/mod_bpcabf41_hdr_aec_data/hdr_aec_data/mod_bpcabf41_aec_data"
param_names = [
                "noise_prsv_lo",
                "edge_softness"
            ]

data_node = "bpcabf41_rgn_data"
print(xml_path)
tree = ET.parse(xml_path)
root = tree.getroot()
print(root.tag)
node = root.findall(xml_node)

for i, ele in enumerate(node):
    print(ele.tag)
    rgn_data = ele.find(data_node)
    for param_name in param_names:
        parent = rgn_data.find(param_name+'_tab')
        if parent:
            param_value = parent.find(param_name).text.split(' ') 
            param_value = [float(x) for x in param_value]

            bound = json.loads(parent.attrib['range'])
            length = int(parent.attrib['length'])
            
        else:
            parent = rgn_data.find(param_name)
            param_value = parent.text.split(' ') 
            param_value = [float(x) for x in param_value]

            bound = json.loads(parent.attrib['range'])
            length = int(parent.attrib['length'])
        print(parent.tag)
        print(param_value)
