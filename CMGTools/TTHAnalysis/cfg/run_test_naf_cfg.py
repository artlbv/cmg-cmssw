##########################################################
##       CONFIGURATION FOR SUSY SINGLELEPTON TREES      ##
##  condition: >= 1 loose leptons, no pt cuts or id     ##
##########################################################

import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps
from CMGTools.RootTools.RootTools import *

#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import * 

ttHLepAna.loose_muon_pt  = 10
ttHLepAna.loose_muon_relIso = 0.2
ttHLepAna.loose_electron_pt  = 10
ttHLepAna.loose_electron_relIso = 0.2
ttHLepAna.ele_isoCorr = "deltaBeta"

# Event Analyzer for susySingleLepton  (at the moment, it's still he TTH one)
ttHEventAna = cfg.Analyzer(
    'ttHLepEventAnalyzer',
    minJets25 = 0,
    )


ttHIsoTrackAna = cfg.Analyzer(
            'ttHIsoTrackAnalyzer',
            candidates='packedPFCandidates',
            candidatesTypes='std::vector<pat::PackedCandidate>',
            ptMin = 5, # for pion 
            ptMinEMU = 5, # for EMU
            dzMax = 0.1,
            isoDR = 0.3,
            ptPartMin = 0,
            dzPartMax = 0.1,
            maxAbsIso = 8,
            MaxIsoSum = 0.1, ### unused
            MaxIsoSumEMU = 0.2, ### unused
            doSecondVeto = False
            )

# Tree Producer
treeProducer = cfg.Analyzer(
    'treeProducerSusySingleLepton',
    vectorTree = True,
    saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
    PDFWeights = PDFWeights,

    )

#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.TTHAnalysis.samples.samples_13TeV_CSA14_desy import *
selectedComponents = [ TTJets_PU40bx25_V52, TTJets_PU20bx25_V52 ]

#-------- SEQUENCE

sequence = cfg.Sequence(susyCoreSequence+[
    ttHEventAna,
    ttHIsoTrackAna,
    treeProducer,
    ])


#-------- HOW TO RUN
test = 4
if test==1:
    # test a single component, using a single thread.
    comp = TTJets_PU40bx25_V52
    comp.files = comp.files[:1]
    selectedComponents = [comp]
    comp.splitFactor = 1
elif test==2:
    # test all components (1 thread per component).
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.files = comp.files[:1]
elif test==3:
#    # test a single component, using a single thread.
    comp = TTJets_PU40bx25_V52
    comp.files = comp.files[:10]
    selectedComponents = [comp]
    comp.splitFactor = len(comp.files)
elif test==4:
    # test all components (1 thread per component).
    for comp in selectedComponents:
        comp.files = comp.files[:10]
        comp.splitFactor = 10

config = cfg.Config( components = selectedComponents,
                     sequence = sequence )

printComps(config.components, True)
