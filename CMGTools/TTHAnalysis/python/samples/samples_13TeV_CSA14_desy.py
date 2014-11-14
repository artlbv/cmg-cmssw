from CMGTools.TTHAnalysis.samples.getFiles import getFiles
import CMGTools.RootTools.fwlite.Config as cfg
import os




################## Triggers (FIXME: update!)


triggers_mumu = ["HLT_Mu17_Mu8_v*","HLT_Mu17_TkMu8_v*"]
triggers_ee   = ["HLT_Ele17_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL_Ele8_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL_v*",
                 "HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*",
                 "HLT_Ele15_Ele8_Ele5_CaloIdL_TrkIdVL_v*"]

triggers_mue   = [
    "HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*",
    "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*"
    ]

triggersMC_mumu = ["HLT_Mu17_Mu8_v*","HLT_Mu17_TkMu8_v*"]

triggersMC_ee   = ["HLT_Ele17_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL_Ele8_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL_v*",
                   "HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*",
                   "HLT_Ele15_Ele8_Ele5_CaloIdL_TrkIdVL_v*"]

triggersMC_mue   = ["HLT_Ele17_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL_Ele8_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL_v*",
                    "HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*",
                    "HLT_Ele15_Ele8_Ele5_CaloIdL_TrkIdVL_v*",
                    "HLT_Mu17_Mu8_v*",
                    "HLT_Mu17_TkMu8_v*",
                    "HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*",
                    "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*"
                   ]

triggers_1mu = [ 'HLT_IsoMu24_eta2p1_v*' ]
triggersMC_1mu  = triggers_1mu;
triggersFR_1mu  = [ 'HLT_Mu5_v*', 'HLT_RelIso1p0Mu5_v*', 'HLT_Mu12_v*', 'HLT_Mu24_eta2p1_v*', 'HLT_Mu40_eta2p1_v*' ]
triggersFR_mumu = [ 'HLT_Mu17_Mu8_v*', 'HLT_Mu17_TkMu8_v*', 'HLT_Mu8_v*', 'HLT_Mu17_v*' ]
triggersFR_1e   = [ 'HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*', 'HLT_Ele17_CaloIdL_CaloIsoVL_v*', 'HLT_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*', 'HLT_Ele8__CaloIdL_CaloIsoVL_v*']
triggersFR_mue  = triggers_mue[:]
triggersFR_MC = triggersFR_1mu + triggersFR_mumu + triggersFR_1e + triggersFR_mue


#####COMPONENT CREATOR

from CMGTools.TTHAnalysis.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

## CENTRALLY PRODUCED MINIAODs (from global DBS)
TTJets_PU20bx25_V52 = kreator.makeMCComponent("TTJets_PU20bx25_V52",    "/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM", "CMS", ".*root")
TTJets_PU40bx25_V52 = kreator.makeMCComponent("TTJets_PU40bx25_V52",    "/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU40bx25_POSTLS170_V5-v2/MINIAODSIM", "CMS", ".*root")

ZprimeToMuMu_1000_PU20bx25_V52 = kreator.makeMCComponent("ZprimeToMuMu_1000_PU20bx25_V52",    "/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM", "CMS", ".*root")

## LOCALLY PRODUCED SIGNAL SAMPLES
def _grep(x,l): return [ i for i in l if x in i ]

t1tttt_800_450_Files = [ f.strip() for f in open("%s/src/CMGTools/TTHAnalysis/python/samples/fullSim-t1tttt_800_450.txt" % os.environ['CMSSW_BASE'], "r") ]
sq_gl_1300_Files = [ f.strip() for f in open("%s/src/CMGTools/TTHAnalysis/python/samples/fullSim-gl-sq-1300.txt" % os.environ['CMSSW_BASE'], "r") ]
fullSim_t1qqqq_Files = [ f.strip() for f in open("%s/src/CMGTools/TTHAnalysis/python/samples/fullSim-t1qqqq-1400-15.txt" % os.environ['CMSSW_BASE'], "r") ]

SMS_T1tttt_2J_mGl800_mLSP450_PU_S14 = kreator.makePrivateMCComponent('SMS_T1tttt_2J_mGl800_mLSP450_PU_S14',  '/nfs/dust/cms/group/susy-desy/Run2/MC/MiniAOD/13TeV_T1tttt_gluino_800_LSP_450/',   _grep('T1tttt_gluino_800_LSP_450_', t1tttt_800_450_Files) )
SMS_Gl_Sq_mGl1300_mSq1300_PU_S14 = kreator.makePrivateMCComponent('SMS_Gl_Sq_mGl1300_mSq1300_PU_S14',  '/nfs/dust/cms/group/susy-desy/Run2/MC/MiniAOD/13TeV_Sq_Gl_4t_Gl1300_Sq1300_LSP100/',   _grep('13TeV_', sq_gl_1300_Files) )
SMS_Gl_Gl_mGl1400_mLSP300_mChi315_PU_S14 = kreator.makePrivateMCComponent('SMS_Gl_Gl_mGl1400_mLSP300_mChi315_PU_S14',  '/nfs/dust/cms/group/susy-desy/Run2/MC/MiniAOD/13TeV_Gl_Gl_4q_Gl1400_LSP300_Chi315/',   _grep('13TeV_', fullSim_t1qqqq_Files) )
#SMS_T1tttt_2J_mGl800_mLSP450_PU_S14_POSTLS170 = kreator.makePrivateMCComponent("SMS_T1tttt_2J_mGl800_mLSP450_PU_S14_POSTLS170", [ "/nfs/dust/cms/group/susy-desy/Run2/MC/MiniAOD/Merged/13TeV_T1tttt_gluino_800_LSP_450_MiniAOD.root" ])


mcSamples = [ TTJets_PU20bx25_V52,TTJets_PU40bx25_V52,ZprimeToMuMu_1000_PU20bx25_V52 ]
fullSimSamples= [ SMS_T1tttt_2J_mGl800_mLSP450_PU_S14, SMS_Gl_Sq_mGl1300_mSq1300_PU_S14, SMS_Gl_Gl_mGl1400_mLSP300_mChi315_PU_S14 ]

#-----------DATA---------------
dataDir = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/data"
#lumi: 12.21+7.27+0.134 = 19.62 /fb @ 8TeV

json=dataDir+'/json/Cert_Run2012ABCD_22Jan2013ReReco.json'

SingleMu = cfg.DataComponent(
    name = 'SingleMu',
    files = [ 'root://eoscms//eos/cms/store/cmst3/user/gpetrucc/miniAOD/v1/SingleMu-Run2012D-15Apr2014-v1_PAT_big.root' ],
    intLumi = 1,
    triggers = [],
    json = json
    )

DoubleElectron = cfg.DataComponent(
    name = 'DoubleElectron',
    files = [ 'root://eoscms//eos/cms/store/cmst3/user/gpetrucc/miniAOD/v1/DoubleElectron-Run2012D-15Apr2014-v1_PAT_big.root' ],
    intLumi = 1,
    triggers = [],
    json = json
    )
           
dataSamplesMu=[]
dataSamplesE=[DoubleElectron]
dataSamplesMuE=[]
dataSamples1Mu=[SingleMu,]
dataSamplesAll = dataSamplesMu+dataSamplesE+dataSamplesMuE+dataSamples1Mu


from CMGTools.TTHAnalysis.setup.Efficiencies import *


#Define splitting
for comp in mcSamples + fullSimSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 1 #  if comp.name in [ "WJets", "DY3JetsM50", "DY4JetsM50","W1Jets","W2Jets","W3Jets","W4Jets","TTJetsHad" ] else 100
    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
    comp.puFileData=dataDir+"/puProfile_Data12.root"
    comp.efficiency = eff2012

for comp in dataSamplesAll:
    comp.splitFactor = 1
    comp.isMC = False
    comp.isData = True
