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
   input = cms.untracked.int32(20)
)

### =====================================================================================================
usePrivateSQlite =False

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag.globaltag = '75X_mcRun2_asymptotic_v1'   # for Simulation #same globalTag

if usePrivateSQlite:
    from CondCore.DBCommon.CondDBSetup_cfi import *
    era="Summer15_V5_MC"
    process.jec = cms.ESSource("PoolDBESSource",CondDBSetup,
                               connect = cms.string( "sqlite_file:PhysicsTools/PatAlgos/test/"+era+".db" ),
                               toGet =  cms.VPSet(
            cms.PSet(
                record = cms.string("JetCorrectionsRecord"),
                tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PF"),
                label= cms.untracked.string("AK4PF")
                ),
            cms.PSet(
                record = cms.string("JetCorrectionsRecord"),
                tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PFchs"),
                label= cms.untracked.string("AK4PFchs")
                ),
            )
                               )
    process.es_prefer_jec = cms.ESPrefer("PoolDBESSource",'jec')

### =====================================================================================================


# Define the input source
process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring([
<<<<<<< HEAD
            "root://eoscms//eos/cms/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/009D49A5-7314-E511-84EF-0025905A605E.root",
            "root://eoscms//eos/cms/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/00C0BECF-6F14-E511-96F8-0025904B739A.root",
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
                                  computeUncertainties=False,
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
=======
            #"file:patMiniAOD_standard.root"
            "root://eoscms//eos/cms/store/relval/CMSSW_7_5_0/RelValTTbar_13/MINIAODSIM/PU25ns_75X_mcRun2_asymptotic_v1_FastSim-v1/00000/2C2B7040-042B-E511-9888-0025905A60D6.root",
    ])
)

from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

#default configuration for miniAOD reprocessing
runMetCorAndUncFromMiniAOD(process)
>>>>>>> dfe32e5... update the MET XY correction and met reprocessing example


process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
<<<<<<< HEAD
    outputCommands = cms.untracked.vstring( "keep *_patPFMetT1Txy_*_RERUN",
                                            "keep *_patPFMetT1Txy*En*_*_RERUN",
                                            "keep *_patPFMetT1Txy*Res*_*_RERUN",
                                            "keep *_slimmedMETs_*_*",
=======
    outputCommands = cms.untracked.vstring( "keep *_slimmedMETs_*_RERUN",
                                        #    "keep *_*_*_PAT"
>>>>>>> dfe32e5... update the MET XY correction and met reprocessing example
                                            ),
    fileName = cms.untracked.string('corMETMiniAOD.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    fastCloning = cms.untracked.bool(False),
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)


process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)
