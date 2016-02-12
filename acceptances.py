#!/usr/bin/env python
import logging
import argparse
import sys
import os
import datetime
import ROOT
import Utilities.scalePDFUncertainties as Uncertainty
import Utilities.Ntuple as Ntuple
from Utilities.ConfigHistFactory import ConfigHistFactory
from collections import OrderedDict

def getComLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--denominator", type=str, required=True,
                        help="First file")
    parser.add_argument("-n", "--numerator", type=str, required=True,
                        help="Second file")
    parser.add_argument("--denom_cut", type=str, required=True,
                        help="first cut")
    parser.add_argument("--num_cut", type=str, required=True,
                        help="Second cut")
    args = parser.parse_args()
    return args
def getVariations(weight_ids, weight_sums):
    values = {"1001" : OrderedDict(), 
            "2001" : OrderedDict(), 
            "3001" : OrderedDict(),
            "4001" : OrderedDict()
    }
    if len(weight_ids) != len(weight_sums):
        print "Should have equal number of weights and IDs!!!"
        print "length of weight_ids: %i" % len(weight_ids) 
        print "length of weight_sums: %i" % len(weight_sums) 
        exit(1)
    for weight in zip(weight_ids, weight_sums):
        label = ''.join([weight[0][0], "001"]) 
        values[label][weight[0]] = weight[1]
    return values
def main():
    args = getComLineArgs()
    print args
    ROOT.gROOT.SetBatch(True)
    ROOT.TProof.Open('workers=24')
    
    file1_sel = getWeightsFromFile(args.denominator, args.denom_cut)
    file2_sel = getWeightsFromFile(args.numerator, args.num_cut)
    print file1_sel
    print file2_sel
    variations = file1_sel
    for weight_set in file1_sel.keys():
        for key in file1_sel[key].keys():
            variations[weight_set][key] /= file2_sel[weight_set][key]
    central = variations["1001"]["1001"]
    print "Central is %f" % central
    print central*2.
    scales = Uncertainty.getScaleUncertainty(variations)
    print scales
    print scales["up"]*2
    print "Scale up is %f" % scales["up"]*central
    print "Scale down is %f" % scales["down"]*central
    print "PDF is %f" % Uncertainty.getFullPDFUncertainty(variations)*central
#  
def getWeightsFromFile(filename, cut):
    path = "/cms/kdlong" if "hep.wisc.edu" in os.environ['HOSTNAME'] else \
        "/afs/cern.ch/user/k/kelong/work"
    config_factory = ConfigHistFactory(
        "%s/AnalysisDatasetManager" % path,
        "ZZGenAnalysis/isHardProcess"
    )
    #mc_info = config_factory.getMonteCarloInfo()
    all_files = config_factory.getFileInfo()
    hist_factory = OrderedDict() 
    selection = "ZZGenAnalysis/isHardProcess"
    if filename not in all_files.keys():
        logging.warning("%s is not a valid file name (must match a definition in FileInfo/%s.json)" % \
            (filename, selection))
    ntuple = Ntuple.Ntuple("LHEweights")
    proof_name = "-".join([filename, "%s#/%s" % (selection.replace("/", "-"), "analyzeZZ/Ntuple")])
    ntuple.setProofPath(proof_name)
    metaTree = ROOT.TChain("analyzeZZ/MetaData")
    metaTree.Add(all_files[filename]["file_path"])
    
    weight_ids = []
    for row in metaTree:
        for weight_id in row.LHEweightIDs:
            weight_ids.append(weight_id)
        break
    weight_sums = ntuple.getSumWeights(cut)
    return getVariations(weight_ids, weight_sums)

#    print 'Script called at %s' % datetime.datetime.now()
#    print 'The command was: %s\n' % ' '.join(sys.argv)
#    if args.print_scale and args.uncertainty:
#        central = variations["1001"]["1001"]
#        xsec = cross_secs["fid"]*1000
#        print "_______________________________________________________________"
#    if args.print_pdf and args.uncertainty:
#        print "Explicit values from pdf variations for fiducial region (in fb) were:"
#        central = variations["1001"]["1001"]
#        xsec = cross_secs["fid"]*1000
#        for weight_set in variations:
#            for key, value in variations[weight_set].iteritems():
#                print "%s %s" % (key, value)#/variations["1001"]["1001"]*xsec)
#            print "_______________________________________________________________"

if __name__ == "__main__":
    main()
