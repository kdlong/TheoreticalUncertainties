#!/usr/bin/env python
import logging
import argparse
import sys
import os
import datetime
import ROOT
import Utilities.scalePDFUncertainties as Uncertainty
import Utilities.Ntuple as Ntuple
import Utilities.UserInput as UserInput
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
def excludeKeysFromDict(values, exclude):
    return [x for key, x in values.iteritems()
            if key not in exclude]

def main():
    args = getComLineArgs()
    ROOT.gROOT.SetBatch(True)
    ROOT.TProof.Open('workers=24')
    num_sel = getWeightsFromFile(args.numerator, args.num_cut)
    denom_sel = getWeightsFromFile(args.denominator, args.denom_cut)
    variations = num_sel
    central = num_sel["1001"]["1001"]/denom_sel["1001"]["1001"]
    for weight_set in num_sel.keys():
        for weight_id in num_sel[weight_set].keys():
            variations[weight_set][weight_id] /= denom_sel[weight_set][weight_id]
            if weight_id != "1001":
                variations[weight_set][weight_id] /= central
    scales = Uncertainty.getScaleUncertainty(excludeKeysFromDict(
        variations["1001"], ["1001", "1006", "1008"])
    )
    pdf_unc = Uncertainty.getFullNNPDFUncertainty(excludeKeysFromDict(
        variations["2001"], ["2101", "2102"]),
        [variations["2001"]["2101"], variations["2001"]["2102"]]
    )
    print variations
    print '-'*80
    print 'Script called at %s' % datetime.datetime.now()
    print 'The command was: %s' % ' '.join(sys.argv)
    print '-'*40
    print "Final Result in %:"
    print "%0.2f^{+%0.2f%%}_{-%0.2f%%} \pm %0.2f%%" % tuple(round(x*100, 2)
            for x in [central, scales["up"], scales["down"], pdf_unc["up"]])
    print ''.join(["%0.2f" % round(central*100, 2), 
            "^{+%0.2f}_{-%0.2f} \pm %0.2f" % tuple(round(x*central*100, 2)
            for x in [scales["up"], scales["down"], pdf_unc["up"]])])
    print '-'*40
    print pdf_unc
  
def getWeightsFromFile(filename, cut):
    path = "/cms/kdlong" if "hep.wisc.edu" in os.environ['HOSTNAME'] else \
        "/afs/cern.ch/user/k/kelong/work"
    config_factory = ConfigHistFactory(
        "%s/AnalysisDatasetManager" % path,
        "WZGenAnalysis/isHardProcess"
    )
    #config_factory.setProofAliases()
    all_files = config_factory.getFileInfo()
    hist_factory = OrderedDict() 
    selection = "WZGenAnalysis/isHardProcess"
    if filename not in all_files.keys():
        logging.warning("%s is not a valid file name (must match a definition in FileInfo/%s.json)" % \
            (filename, selection))
    ntuple = Ntuple.Ntuple("LHEweights")
    proof_name = "-".join([filename, "%s#/%s" % (selection.replace("/", "-"), "analyzeWZ/Ntuple")])
    ntuple.setProofPath(proof_name)
    metaTree = ROOT.TChain("analyzeWZ/MetaData")
    metaTree.Add(all_files[filename]["file_path"])
    weight_ids = []
    for row in metaTree:
        for weight_id in row.LHEweightIDs:
            weight_ids.append(weight_id)
        break
    weight_sums = ntuple.getSumWeights(config_factory.hackInAliases(cut))
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
