import ROOT

class Ntuple(object):
    def __init__(self, weights_branch):
        self.lhe_weights_branch = weights_branch
        self.proof_path = ''
        self.chain = ''
    def setInitSumWeights(self, sum_weights):
        self.init_sum_weights = sum_weights
    def setChain(self, chain):
        self.chain = chain
    def setProofPath(self, proof_path):
        self.proof_path = proof_path
    def getSumWeights(self, cut_string):
        if self.proof_path != '':
            return self.getSumWeightsProof(cut_string)
        else:
            return []
    def getSumWeightsProof(self, cut_string):
        proof = ROOT.gProof
        proof.Load("sumWeights.C+")
        sumWeights = ROOT.sumWeights()
        print "cut_string is %s" % cut_string
        proof.Process(self.proof_path, sumWeights, cut_string)
        summedWeightsHist = sumWeights.GetOutputList().FindObject('summedWeights')
        summedWeightsHist.Draw("hist")
        sums = []
        for i in xrange(1, summedWeightsHist.GetSize() + 1):
            sums.append(summedWeightsHist.GetBinContent(i))
        sums = sums[:sums.index(0.0)]
        return sums
