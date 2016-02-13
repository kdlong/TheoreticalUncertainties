#!/usr/bin/env python
import argparse
import re
import xml.etree.ElementTree as ET
from Utilities import EDMWeightInfo
from Utilities import LHAPDFInfo
from Utilities import prettytable

lhapdf_info = LHAPDFInfo.getPDFIds()
def getComLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_name", required=True,
            help="EDM file name (should be full path, starting"
                "with '/store' for file on DAS"
                )
    return parser.parse_args()
def getPDFSetInfo(entry):
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
    weight_info = EDMWeightInfo.getWeightIDs(args.file_name)
    root = ET.fromstring("<header>" + weight_info + "</header>")
    other_weights_table = prettytable.PrettyTable(["LHE weight ID", "LHE Weight Name"])
    pdf_weights_table = prettytable.PrettyTable(["LHE weight ID", "LHE Weight Name", "PDF set name", "LHAPDF set path"])
    for block in root:
        for entry in block:
            pdf_info = getPDFSetInfo(entry.text) 
            if pdf_info == "":
                other_weights_table.add_row([entry.attrib["id"], entry.text])
            else:
                pdf_weights_table.add_row([entry.attrib["id"], entry.text, pdf_info["name"],
                    pdf_info["path"]])
    print other_weights_table
    print pdf_weights_table

if __name__ == "__main__":
        main()
