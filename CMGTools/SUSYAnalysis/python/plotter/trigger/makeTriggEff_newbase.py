#!/usr/bin/python

import sys

from array import array
from ROOT import *

from triggTools import *

# global storages
_canvStore = []
_histStore = {}
_hEffStore = {}

_fitrStore = []

_colorList = [2,8,4,9,7,3,6] + range(10,50)

def getHistsFromTree(tree, var = 'MET', refTrig = '', cuts = '', testTrig = '', maxEntries = -1, lumi = -1):

    # maximum number of entries to process
    if maxEntries == -1:
        maxEntries = tree.GetEntries()

    # histogram name prefix
    histPrefix = 'h' + var + '_'

    # plot option
    plotOpt = 'e1'

    # histogram list
    histList = []

    # prepend HLT name
    testTrig = ['HLT_'+name.replace('HLT_','') for name in testTrig]

    # names
    if refTrig != '':
        refName = refTrig.replace('HLT_','')
    else:
        refName = 'PreSel'

    ## name replacement
    refName = renameTrig(refName)
    rname = histPrefix + refName

    cname = var + '_' + refName
    ctitle = 'Plots for reference:' + refName

    if cuts != '':
        ctitle += ' cut: ' + cuts

    if refTrig != '':
        cuts += ' && HLT_' + refTrig.replace('HLT_','')
        htitle = refTrig.replace('HLT_','')#'Ref: ' + refTrig
    else:
        htitle = 'Preselection'

    print 'Going to draw', ctitle

    # make canvas
    canv = TCanvas(cname,ctitle,800,800)

    # make hist
    nbins = 50

    varBinSize = False

    if var == 'MET':
        hRef = TH1F(rname,htitle,nbins,0,1000)
    elif var == 'HT':
        hRef = TH1F(rname,htitle,nbins,0,3000)
    elif 'pt' in var:
        #xbins = range(5,25,1) + range(25,70,5) + range(70,150,10) + range (150,225,25)#[10,20,30,40,60,80,100,150,200]
        xbins = range(6,30,2) + range(30,70,5) + range(70,150,10) + range (150,225,25)
        varBinSize = True

        hRef = TH1F(rname,htitle,len(xbins)-1,array('f',xbins))
        #hRef = TH1F(rname,htitle,nbins,0,200)
    elif 'eta' in var:
        hRef = TH1F(rname,htitle,nbins,-2.5,2.5)
    else:
        hRef = TH1F(rname,htitle,nbins,0,1000)

    ## lumi scaling
    if lumi == 0:
        # don't do lumi scaling on MC
        doLumi = False
        CMS_lumi.lumi_13TeV = "MC"
        CMS_lumi.extraText = "Simulation"
        hRef.GetYaxis().SetTitle('MC counts')
    elif lumi > 0:
        # make lumi label for data
        doLumi = False
        CMS_lumi.lumi_13TeV = str(lumi) + " pb^{-1}"
        CMS_lumi.extraText = "Preliminary"
        hRef.GetYaxis().SetTitle('Events')
    elif lumi < 0:
        # do lumi scaling for MC
        doLumi = True
        CMS_lumi.lumi_13TeV = str(lumi) + " fb^{-1}"
        CMS_lumi.extraText = "Simulation"
        hRef.GetYaxis().SetTitle('Events')

    # make reference plot
    if not doLumi:
        tree.Draw(var + '>>' + hRef.GetName(),cuts,plotOpt, maxEntries)
        print '# Drawing', hRef.GetName(), 'with cuts', cuts
    else:
        hRef.Sumw2()

        wt = 1000*lumi/float(maxEntries)
        print '# Weight for %2.2f lumi and maxEntries %10.f is %f' %(lumi, maxEntries,wt)
        weight = str(wt) + ' * Xsec'
        if cuts != '': wcuts = weight + '*(' + cuts + ')'
        else: wcuts = weight
        print '# Drawing', hRef.GetName(), 'with cuts', wcuts

        tree.Draw(var + '>>' + hRef.GetName(),wcuts,plotOpt, maxEntries)
        hRef.SetMaximum(hRef.GetMaximum() * 2)

    print '# Found', hRef.Integral(), 'events'

    hRef.SetLineColor(1)
    # axis set up
    hRef.SetStats(0)
    hRef.GetXaxis().SetTitle(varToLabel(var))
    hRef.GetYaxis().SetTitleOffset(1.2)
    canv.SetLogy()

    gPad.Update()

    _histStore[hRef.GetName()] = hRef
    histList.append(hRef)

    # loop over test triggers:
    for ind, trig in enumerate(testTrig):

        # for OR and AND test triggers
        if '||' in trig:
            tnames = trig.replace('HLT_','').split('||')
            trigName = tnames[0]
            trig = '(' + 'HLT_'+tnames[0].replace('HLT_','')

            for name in tnames[1:]:
                trigName += '_' + name
                trig += '||' + 'HLT_'+name.replace('HLT_','')
            trig += ')'

            print trigName
            print trig
        else:
            trigName = trig.replace('HLT_','')

        trigName = renameTrig(trigName)

        hname = 'h' + var + '_' + trigName

        hTest = hRef.Clone(hname)
        hTest.SetTitle(trigName)

        hTest.SetLineColor(_colorList[ind])

        # cuts

        if cuts != '':
            tcuts = cuts + ' && ' + trig
        else:
            tcuts = trig

        print '# Drawing', hTest.GetName(), 'with cuts', tcuts

        # lumi scale
        if not doLumi:
            tree.Draw(var + '>>' + hTest.GetName(),tcuts,plotOpt+'same', maxEntries)
        else:
            #hTest.Sumw2()
            if tcuts != '': wtcuts = weight + '*(' + tcuts + ')'
            else: wtcuts = weight
            tree.Draw(var + '>>' + hTest.GetName(),wtcuts,plotOpt+'same', maxEntries)

        print '# Found', hTest.Integral(), 'events'

        gPad.Update()

        _histStore[hTest.GetName()] = hTest
        histList.append(hTest)

    # if var bin sizes
    if varBinSize:

        # add /bin in Y axis label
        hRef.GetYaxis().SetTitle(hRef.GetYaxis().GetTitle() + '/bin')


        for hist in histList:
            for bin in range(1,hist.GetNbinsX()+1):
                binC = hist.GetBinContent(bin)
                binW = hist.GetBinWidth(bin)

                binV = binC/binW
                #print binC, binW, binV

                hist.SetBinContent(bin, binV)

    #hRef.SetTitle(ctitle)

    # legend
    leg = canv.BuildLegend()
    leg.SetFillColor(0)
    #leg.SetHeader(ctitle.replace('&&','\n'));

    # plot CMS info
    CMS_lumi.CMS_lumi(canv, 4, iPos)

    gPad.Update()
    _canvStore.append(canv)

    return histList

def plotEff(histList, var = 'HT', doFit = False):


    ## histList: [hReference, hTest1, hTest2,...]

    # hist prefix
    histPrefix = 'h' + var + '_'

    # reference hist should be first
    hRef = histList[0]
    hRefEff = hRef.Clone(hRef.GetName()+'Eff')
    # set reference eff to 1
    hRefEff.Divide(hRef)

    hRefEff.GetYaxis().SetTitle("Efficiency")

    if not doFit:
        cname = hRef.GetName().replace('h'+var,var) + '_Eff_'
    else:
        cname = hRef.GetName().replace('h'+var,var) + '_EffFit'

    ctitle = 'Eff for reference:' + hRefEff.GetName()

    ## make canvas
    canv = TCanvas(cname,ctitle,800,800)
    ## style

    ## legend
    leg = getLegend('fit')

    # set reference eff to 1
    for bin in range(1,hRefEff.GetNbinsX()+1):
        hRefEff.SetBinContent(bin,1)
        hRefEff.SetBinError(bin,0)

    hRefEff.Draw()
    #leg.AddEntry(0,'Reference: ' + hRefEff.GetName(),'')
    leg.SetHeader('Reference: ' + hRef.GetName().replace('h'+var+'_',''))
    #leg.AddEntry(hRefEff,hRefEff.GetTitle(),'lp')

    plotOpt = 'same'

    gPad.Update()

    # loop over test
    #for ind,hname in enumerate(nameList):
    for ind,hist in enumerate(histList[1:]):

        #hist = _histStore[hname]
        hname = hist.GetName()

        # filter out hists
        #if histPrefix not in hname: continue
        #if 'Ref' in hname: continue

        htitle = hname.replace(histPrefix,'')
        hname = hname.replace('h','hEff')

        print 'Drawing', hname, 'from', hRef.GetName()

        ## Divide
        hEff = hist.Clone(hname)
        hEff.Divide(hRef)

        ## TEfficiency
        tEff = TEfficiency(hist,hRef)
        tEff.SetName(hname);#+';'+var+';Efficiency')
        tEff.SetTitle(htitle)

        # style
        tEff.SetLineColor(hist.GetLineColor())
        tEff.SetFillColor(0)
        tEff.SetMarkerStyle(20)
        tEff.SetMarkerColor(hist.GetLineColor())

        tEff.Draw(plotOpt)
        leg.AddEntry(tEff,tEff.GetTitle(),'lp')

        if 'same' not in plotOpt: plotOpt += 'same'

        gPad.Update()

        #SetOwnership(tEff,0)

        if doFit and hEff.GetEntries() > 0:
            ## Fitting turn on curve
            print 'Fitting...'

            xmin = hEff.GetXaxis().GetXmin()
            xmax = hEff.GetXaxis().GetXmax()

            fturn = TF1("turnon",turnon_func,xmin,xmax,3)
            fturn.SetParNames('halfpoint','width','plateau')
            fturn.SetParLimits(0,0,10000)
            fturn.SetParLimits(1,0.1,10000)
            fturn.SetParLimits(2,0,1)

            fturn.SetLineColor(hEff.GetLineColor())

            ## get painted graph and fit with turn-on
            gEff = tEff.GetPaintedGraph()
            #gEff = hEff

            ## get estimate of parameters
            expPlateau = min(hEff.GetMaximum(),0.99)
            expHalfP = hEff.GetBinCenter(hEff.FindFirstBinAbove(0.5))
            expWidth = expHalfP/2

            #fturn.SetParameters(300,100,1)
            fturn.SetParameters(expHalfP,expWidth,expPlateau)

            ## do fit
            fitr = gEff.Fit(fturn,'S Q EX0')#EX0

            SetOwnership(gEff,0)

            halfpoint = fitr.Value(0)
            width = fitr.Value(1)
            plateau = fitr.Value(2)

            print 'Expected values: halfpoint = %5.2f, width = %5.2f, plateau = %5.2f' % (expHalfP, expWidth, expPlateau)
            print 'Fit result: halfpoint = %5.2f, width = %5.2f, plateau = %5.2f' % (halfpoint, width, plateau)
            print 80*'#'

            gStyle.SetOptFit()
            #gStyle.SetOption("Show Fit Parameters")
            gPad.Update()

            _fitrStore.append((hname,halfpoint, width, plateau))

        _hEffStore[hname] = tEff

    # remove refEff
    #gPad.GetListOfPrimitives().Remove(hRef)

    # legend
    #leg = canv.BuildLegend()
    #leg.SetFillColor(0)
    leg.Draw()
    SetOwnership( leg, 0 )

    # axis set up
    hRefEff.SetStats(0)
    #hRef.GetXaxis().SetTitle(var)
    hRefEff.GetYaxis().SetRangeUser(0,1.5)
    #canv.SetLogy()

    #leg.GetListOfPrimitives().Remove(hRefEff)

    ## CMS lumi
    CMS_lumi.CMS_lumi(canv, 4, iPos)

    gPad.Update()

    _hEffStore[hRefEff.GetName] = hRefEff
    _canvStore.append(canv)

    return 1

def makeEffPlots(tree, lumi = -1, maxEntries = -1, doFit = False, varList = [], refTrig = '', testTrig = [], cuts = ''):

    # lumi dir
    if lumi == 0:
        # unscaled MC counts
        lumiDir = 'MC/LumiMC/'
    elif lumi < 0:
        # scaled MC
        lumiDir = 'MC/Lumi'+str(lumi).replace('.','p')+'fb/'
    elif lumi > 0:
        # data
        lumiDir = 'Data/Lumi'+str(lumi).replace('.','p')+'pb/'

    # make suffix from testTrigNames
    suffix = 'test'
    for trig in testTrig:
        suffix +=  '_' + trig.replace('||','OR')

    # final output dir:
    lumiDir = 'plots/2d/' + lumiDir

    print '## Going to save plots to', lumiDir

    for var in varList:

        histList = getHistsFromTree(tree,var,refTrig, cuts, testTrig, maxEntries, lumi)
        plotEff(histList, var, doFit)
        saveCanvases(_canvStore, lumiDir,suffix, _batchMode)

        # empty stores for further use
        del _canvStore[:]
        _histStore.clear()
        _hEffStore.clear()
        del _fitrStore[:]

    return 1

if __name__ == "__main__":

    ## remove '-b' option
    _batchMode = False

    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        fileName = sys.argv[1]
        print '#fileName is', fileName
    else:
        print '#No file names given'
        exit(0)

    tfile  = TFile(fileName, "READ")

    if not tfile:
        print "Couldn't open the file"
        exit(0)

    ## Get tree from file
    # for friend trees
    tree = tfile.Get('sf/t')
    # for cmg trees
    #tree = tfile.Get('tree')

    nentries = tree.GetEntries()
    print 'Entries in tree:', nentries

    ## SETTINGS
    # max entries to process
    maxEntries = -1#100000
    # do efficiency fit
    doFit = True
    # luminosity: 0 takes MC counts, >0 is data, <0 is for MC scaling
    lumi = 0

    '''
    #############
    # LT: Muon
    #############

    varList = ['LT']
    cuts = 'nMu == 1 && Lep_pt > 25 && HT > 500'
    refTrig = ''
    #testTrig = ['Mu50NoIso','MuHT400MET70','Mu50NoIso||MuHT400MET70']
    testTrig = ['Mu50NoIso||MuHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    #############
    # LT: Electron
    #############

    varList = ['LT']
    cuts = 'nEl == 1 && Lep_pt > 25 && HT > 500'
    refTrig = ''
    #testTrig = ['ElNoIso','EleHT400MET70','ElNoIso||EleHT400MET70']
    testTrig = ['ElNoIso||EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    #############
    # Lepton legs
    #############

    ## muons
    varList = ['Lep_pt']
    cuts = 'nMu == 1 && Lep_pt > 5 && HT > 500 && MET > 200'
    refTrig = ''
    testTrig = ['Mu50NoIso','MuHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['Lep_pt']
    cuts = 'nMu == 1 && Lep_pt > 5 && HT > 500 && MET > 200'
    refTrig = 'HTMET'
    testTrig = ['Mu50NoIso','MuHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    ## electrons
    varList = ['Lep_pt']
    cuts = 'nEl == 1 && Lep_pt > 5 && HT > 500 && MET > 200'
    refTrig = ''
    testTrig = ['ElNoIso','EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['Lep_pt']
    cuts = 'nEl == 1 && Lep_pt > 5 && HT > 500 && MET > 200'
    refTrig = 'HTMET'
    testTrig = ['ElNoIso','EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    ###############
    # Hadronic legs: Muon
    ###############

    varList = ['HT']
    cuts = 'nMu == 1 && Lep_pt > 55 && MET > 200'
    refTrig = ''
    testTrig = ['SingleMu','Mu50NoIso', 'MuHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, False, varList, refTrig, testTrig, cuts)

    varList = ['HT']
    cuts = 'nMu == 1 && Lep_pt > 25 && MET > 200'
    refTrig = ''
    testTrig = ['MuHT400MET70']#,'MuHT600']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['MET']
    cuts = 'nMu == 1 && Lep_pt > 25 && HT  > 500'
    refTrig = ''
    testTrig = ['MuHT400MET70']#,'MuHT600']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['HT']
    cuts = 'nMu == 1 && Lep_pt > 25 && MET > 200'
    refTrig = 'SingleMu'
    #testTrig = ['SingleMu','Mu50NoIso','HLT_MuHT400MET70']
    testTrig = ['MuHT400MET70']#,'MuHT600']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['MET']
    cuts = 'nMu == 1 && Lep_pt > 25 && HT  > 500'
    refTrig = 'SingleMu'
    testTrig = ['MuHT400MET70']#,'MuHT600']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    ###############
    # Hadronic legs: Electron
    ###############

    varList = ['HT']
    cuts = 'nEl == 1 && Lep_pt > 120 && MET > 200'
    refTrig = ''
    testTrig = ['SingleEl','ElNoIso', 'EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, False, varList, refTrig, testTrig, cuts)

    varList = ['HT']
    cuts = 'nEl == 1 && Lep_pt > 25 && MET > 200'
    refTrig = ''
    testTrig = ['EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['MET']
    cuts = 'nEl == 1 && Lep_pt > 25 && HT  > 500'
    refTrig = ''
    testTrig = ['EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    refTrig = 'SingleEl'
    testTrig = ['EleHT400MET70']

    varList = ['HT']
    cuts = 'nEl == 1 && Lep_pt > 25 && MET > 200'
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['MET']
    cuts = 'nEl == 1 && Lep_pt > 25 && HT  > 500'
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    '''

    ###################
    ###################
    # DATA
    ###################
    ###################

    doFit = True

    if 'SingleEl' in fileName:
        ## Electrons
        lumi = 43.1 # SingleEl RunB

        refTrig = 'IsoEle32'
        testTrig = ['EleHT350MET70']

        varList = ['MET']
        cuts = 'nEl >= 1 && Lep_pt > 25 && HT  > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        varList = ['HT']
        cuts = 'nEl >= 1 && Lep_pt > 25 && MET  > 200'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    elif 'SingleMu' in fileName:
        ## Muons
        lumi = 38.8 # SingleMu RunB

        refTrig = 'IsoMu27'
        testTrig = ['MuHT350MET70']

        varList = ['MET']
        cuts = 'nMu >= 1 && Lep_pt > 25 && HT  > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        varList = ['HT']
        cuts = 'nMu >= 1 && Lep_pt > 25 && MET  > 200'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
    else:
        print 'Nothing to draw for this file!'

    tfile.Close()
    #outfile.Close()
