#!/bin/usr/env python
import Utilities.scalePDFUncertainties as Uncertainty
import Utilities.helper_functions as helper

variations = helper.getWeightsFromEDMFile("/store/mc/RunIISpring15MiniAODv2/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/0CE5F76D-2E7A-E511-9F05-008CFA0516BC.root")
scales = Uncertainty.getScaleUncertainty(helper.excludeKeysFromDict(
    variations["1000"], ["1001", "1006", "1008"])
)
pdf_unc = Uncertainty.getFullNNPDFUncertainty(helper.excludeKeysFromDict(
    variations["2000"], ["2101", "2102"]),
    [variations["2000"]["2101"], variations["2000"]["2102"]]
)
print "Scales are %s" % scales
print "Pdf uncertainty is %s" % pdf_unc
