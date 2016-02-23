#!/usr/bin/env python
import logging
import argparse
import sys
import os
import datetime
import ROOT
import Utilities.scalePDFUncertainties as Uncertainty
from InputTools import Ntuple, WeightTools

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
    parser.add_argument("-a", "--analysis", type=str, required=True,
                        help="Name of analysis (in AnalysisDatasetManager)")
    args = parser.parse_args()
    return args

def main():
    args = getComLineArgs()
    ROOT.gROOT.SetBatch(True)
    ROOT.TProof.Open('workers=24')
    sameFile = False
    if not args.denominator == args.numerator:
        sameFile = True

    num_sel = WeightTools.getWeightsFromROOTFile(args.numerator, args.analysis, args.num_cut, sameFile)
    denom_sel = WeightTools.getWeightsFromROOTFile(args.denominator, args.analysis, args.denom_cut, sameFile)
    variations = num_sel
    central = num_sel["1000"]["1001"]/denom_sel["1001"]["1001"]
    for weight_set in num_sel.keys():
        for weight_id in num_sel[weight_set].keys():
            variations[weight_set][weight_id] /= denom_sel[weight_set][weight_id]
            if weight_id != "1001":
                variations[weight_set][weight_id] /= central

    scales = Uncertainty.getScaleUncertainty(excludeKeysFromDict(
        variations["1000"], ["1001", "1006", "1008"])
    )
    pdf_unc = Uncertainty.getFullNNPDFUncertainty(excludeKeysFromDict(
        variations["2000"], ["2101", "2102"]),
        [variations["2000"]["2101"], variations["2001"]["2102"]]
    )
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

if __name__ == "__main__":
    main()
