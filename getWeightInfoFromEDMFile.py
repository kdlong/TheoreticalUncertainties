import argparse
import re
import xml.etree.ElementTree as ET
from Utilities import EDMWeightInfo
from Utilities import LHAPDFInfo

lhapdf_info = LHAPDFInfo.getPDFIds()
def getComLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True,
            help="EDM file name (should be full path, starting"
                "with '/store' for file on DAS"
                )
    return parser.parse_arguments()
def getWeightSet(entry):
    weight_set = re.findall(r'\d+', entry)
    if len(weight_set) == 0:
        return ""
    weight_set = int(weight_set[0])
    for i in range(0,3):
        central_id = str(weight_set - (weight_set % 10**i))
        if central_id in lhapdf_info.keys():
            return lhapdf_info[central_id]
    return ""
def main():
    args = getComLineArgs()
    weight_info = EDMWeightInfo.getWeightIDs('/store/mc/RunIISpring15DR74/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/20469B1E-9F18-E511-A402-0002C94CD12E.root')
    weight_info = "<header>" + weight_info + "</header>"
    root = ET.fromstring(weight_info)
    root = ET.fromstring(weight_info)
    for block in root:
        for entry in block:
            print entry.tag, entry.attrib, entry.text
            print getWeightSet(entry.text) 
