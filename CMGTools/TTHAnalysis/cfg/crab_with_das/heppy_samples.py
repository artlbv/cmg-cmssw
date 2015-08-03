#-------- SAMPLES AND TRIGGERS -----------
#from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14 import *
from CMGTools.RootTools.samples.samples_13TeV_74X import *
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
from CMGTools.RootTools.samples.triggers_13TeV_Spring15_1l import *


#selectedComponents =  [TTJets]
#TTJets.splitFactor=1000
#from CMGTools.TTHAnalysis.samples.samples_13TeV_private_heplx import *
#selectedComponents = [T2DegStop_300_270]


#from CMGTools.TTHAnalysis.samples.samples_13TeV_private_heplx import *
#selectedComponents = [DYJetsToLL_M50_PU20bx25]#, DYJetsToLLHT100to200_M50_PU20bx25, DYJetsToLLHT200to400_M50_PU20bx25, DYJetsToLLHT400to600_M50_PU20bx25, DYJetsToLLHT600toInf_M50_PU20bx25]

#selectedComponents = [ TT_PU40bx25 ]
#selectedComponents = [ TT_PU4bx50 ]
#selectedComponents = [TTJets]+SingleTop+WJetsToLNuHT+QCDPt
#selectedComponents = [TTJets]

#selectedComponents = [ SingleElectron_Run2015B ]
#selectedComponents = [ SingleMu_Run2015B ]
#selectedComponents = [ SingleMuon_Run2015B ]
selectedComponents = [TTJets]
#eventFlagsAna.processName = 'HLT'
#jetAna.recalibrateJets = False

#for comp in dataSamples:  #dataSamples is defined in samples_13TeV_DATA2015.py
#  comp.isMC = False
#  comp.isData = True

#for comp in selectedComponents:
#  comp.splitFactor = 1
#  comp.fineSplitFactor = 10
  #comp.files = comp.files[:1]


#-------- HOW TO RUN
test = 0 
#print "selectedComponents1 ",selectedComponents
if test==1:
    # test a single component, using a single thread.
    #comp = TTJets
    comp = T2DegStop_300_270
#    comp = SMS_T1tttt_2J_mGl1500_mLSP100
    comp.files = comp.files[:10]
    print "Files:",comp.files
    selectedComponents = [comp]
    comp.splitFactor = 1
elif test==2:
    # test all components (1 thread per component).
    print "selectedComponents2a ",selectedComponents
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.files = comp.files[:1]
    print "selectedComponents2b ",selectedComponents#
elif test=="data":
        #from CMGTools.RootTools.samples.samples_13TeV_Data import *
        #selectedComponents = [ privEGamma2015A ]
    from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
    selectedComponents = [ SingleElectron_Run2015B ]
    #selectedComponents = [ SingleMu_Run2015B ]

    eventFlagsAna.processName = 'HLT'
    jetAna.recalibrateJets = False

    for comp in dataSamples:
      comp.isMC = False
      comp.isData = True

    for comp in selectedComponents:
      comp.splitFactor = 1
      comp.fineSplitFactor = 10
      #comp.files = comp.files[:1]





