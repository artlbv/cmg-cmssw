#!/usr/bin/env python
from CMGTools.TTHAnalysis.treeReAnalyzer import *

class LepTreeProducer(Module):
    def __init__(self,name,booker,pdgId):
        Module.__init__(self,name,booker)
        print "Booked ",name," for ",pdgId
        self.pdgId = pdgId
    def beginJob(self):
        self.t = PyTree(self.book("TTree","fitter_tree","fitter_tree"))
        self.t.branch("mass","F")
        self.t.branch("tag_pt","F")
        self.t.branch("tag_eta","F")
        self.t.branch("pt","F")
        self.t.branch("eta","F")
        self.t.branch("abseta","F")
        self.t.branch("SIP","F")
        self.t.branch("relIso03","F")
        self.t.branch("mvaId","F")
        self.t.branch("run","F")
        self.t.branch("pair_probeMultiplicity","F")
        self.t.branch("nVert","F")
        #tight charge cuts
        self.t.branch("tightCharge","F")
        self.t.branch("convVeto","F")
        self.t.branch("lostHits","F")  ## needs to be re-structured
    def analyze(self,event):
        if event.nLepGood < 2: return True
        lep = Collection(event,"LepGood","nLepGood",8)
        #mu = [ m for m in lep if abs(m.pdgId) == 13 and e.relIso < 0.4 ]
        mu = [ m for m in lep if abs(m.pdgId) == self.pdgId ]
        if len(mu) < 2: return True
        self.t.run = event.run
        self.t.nVert = event.nVert
        for i,tag in enumerate(mu):
            pairs = []
            if tag.relIso03 > 0.2: continue
            if tag.sip3d  > 4:   continue
            if tag.pt  < 20:     continue
            for j,probe in enumerate(mu):
                if i == j: continue
                pairs.append((tag,probe))
            self.t.pair_probeMultiplicity = len(pairs)
            for tag,probe in pairs:
                self.t.tag_pt = tag.pt
                self.t.tag_eta = tag.eta
                self.t.pt = probe.pt
                self.t.eta = probe.eta
                self.t.SIP = probe.sip3d
                self.t.relIso03 = probe.relIso03
                self.t.mvaId = probe.mvaId
                self.t.abseta = abs(probe.eta)
                self.t.tightCharge = probe.tightCharge
                self.t.convVeto = probe.convVeto
                self.t.lostHits = probe.lostHits
                self.t.mass = (tag.p4() + probe.p4()).M()
                self.t.fill()
                
from sys import argv
f = ROOT.TFile.Open(argv[1])
#t = f.Get("ttHLepTreeProducerBase")
t = f.Get("treeProducerSusySingleLepton")
t.vectorTree = True # new added since the tree definition is changed!
#t.AddFriend("newMVA/t", argv[3])
print "Reading %s (%d entries)" % (argv[1], t.GetEntries())

booker = Booker(argv[2] if len(argv) >= 3 else "lepTree.root")
el = EventLoop([ LepTreeProducer("tpTree",booker,13), LepTreeProducer("tpTreeEl",booker,11),  ])
el.loop([t])
booker.done()
