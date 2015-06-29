import FWCore.ParameterSet.Config as cms

# Define the CMSSW process
process = cms.Process("RERUN")

# Load the standard set of configuration modules
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Message Logger settings
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Set the process options -- Display summary at the end, enable unscheduled execution
process.options = cms.untracked.PSet( 
    allowUnscheduled = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False) 
)

# How many events to process
process.maxEvents = cms.untracked.PSet( 
   input = cms.untracked.int32(100)
)

### =====================================================================================================
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag.globaltag = 'MCRUN2_74_V9A::All'   # for Simulation #same globalTag

### =====================================================================================================


# Define the input source
process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring([
"root://eoscms//eos/cms/store/relval/CMSSW_7_4_1/RelValTTbar_13/MINIAODSIM/PU25ns_MCRUN2_74_V9_gensim_740pre7-v1/00000/40D9C504-07ED-E411-811D-00259059642E.root"
    ])
)

from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMETCorrectionsAndUncertainties

#recomputation only available for T1 and Txy. T0 is copied from the miniAOD, and smearing is not consudered
# necessitates both T1 and T1Txy in the recomputation

#MET T1 uncertainties
runMETCorrectionsAndUncertainties(process, metType="PF",
                                  correctionLevel=["T1"],
                                  computeUncertainties=True,
                                  produceIntermediateCorrections=False,
                                  addToPatDefaultSequence=False,
                                  jetCollection="selectedPatJets",
                                  electronCollection="slimmedElectrons",
                                  muonCollection="slimmedMuons",
                                  tauCollection="slimmedTaus",
                                  reclusterJets = True,
                                  pfCandCollection = "packedPFCandidates",
                                  onMiniAOD=True,
                                  postfix="",
                                  )

#MET T1+Txy
runMETCorrectionsAndUncertainties(process, metType="PF",
                                  correctionLevel=["T1","Txy"],
                                  computeUncertainties=True,
                                  produceIntermediateCorrections=False,
                                  addToPatDefaultSequence=False,
                                  jetCollection="selectedPatJets",
                                  electronCollection="slimmedElectrons",
                                  muonCollection="slimmedMuons",
                                  tauCollection="slimmedTaus",
                                  reclusterJets = True,
                                  pfCandCollection = "packedPFCandidates",
                                  onMiniAOD=True,
                                  postfix="",
                                  )


process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = cms.untracked.vstring( "keep *_ak4PFJets_*_RERUN",
                                            "keep *_pfMet_*_RERUN",
                                            "keep *_patPFMetT1Txy_*_RERUN",
                                            "keep *_patPFMetT1*En*_*_RERUN",
                                            "keep *_patPFMetT1*Res*_*_RERUN",
                                            "keep *_patPFMet_*_RERUN",
                                           # "keep *_*_*_PAT",
                                            "keep *_patJets_*_*",
                                            "keep *_slimmedMETs_*_*",
                                            "keep *_patJetCorrFactors_*_*",
                                            "keep *_selectedPatJetsForMetT1T2Corr_*_*",
                                            "keep *_fixedGridRhoFastjetAll_*_*"
                                            #"keep *_patMETs*_*_RERUN",
                                           ),
    fileName = cms.untracked.string('testminiAOD.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    fastCloning = cms.untracked.bool(False),
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)


process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)
