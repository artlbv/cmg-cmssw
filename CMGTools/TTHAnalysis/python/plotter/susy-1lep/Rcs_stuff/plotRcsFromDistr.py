#!/usr/bin/python

import sys
import os
#sys.argv.append( '-b' )

from ROOT import *
from array import array

_histListSR = []
_histListCR = []
_histListRcs = []

_canvStore = []
_histStore = []

def getHistsFromFile(tfile, flag = 'SR'):

    if 'SR' in tfile.GetName():
        flag = 'SR'
    elif 'CR' in tfile.GetName():
        flag = 'CR'

    print '# Getting hist from', flag

    for key in tfile.GetListOfKeys():
        hist = key.ReadObj()

        if 'TH1' in str(type(hist)):
            ## skip inclusive ST
            if 'ST_background' == hist.GetName(): continue
            if 'background' in hist.GetName():
                hname = hist.GetName()

                hname += '_'+flag

                if flag == 'SR':
                    _histListSR.append(hist.Clone(hname))
                elif flag == 'CR':
                    _histListCR.append(hist.Clone(hname))
    return 1

def getRcsPlots():

    for indx,histSR in enumerate(_histListSR):

        hname = (histSR.GetName()).replace('SR','Rcs')

        histRcs = histSR.Clone(hname)
        histRcs.Divide(_histListCR[indx])

        _histListRcs.append(histRcs)

    return 1

def setColors(histList):

    #    colorList = [3,2,ROOT.kGreen-2,1]
    colorList = [1,2,3,4]

    for ind,hist in enumerate(histList):
        hist.SetLineColor(colorList[ind])
        hist.SetMarkerColor(colorList[ind])

def custHists():
    ## loop over all saved hists
    for hist in _histListCR+_histListSR:

        hname = hist.GetName()
        ## common settings
        hist.SetStats(0)
        hist.SetFillColor(0)
        hist.SetLineWidth(2)
        hist.SetMarkerStyle(0)

        ## rebin
        #hist.Rebin(2)

        htitle = ''
        ## NJ bins
        if 'NJ45'in hname:
            htitle = 'Nj = 4-5, '
        elif 'NJ6'in hname:
            htitle = 'Nj #geq 6, '

        ## HT bins
        if 'HT500750'in hname:
            htitle += '500 < HT < 750'
        elif 'HT7501250'in hname:
            htitle += '750 < HT < 1250'
        elif 'HT1250'in hname:
            htitle += 'HT > 1250'
        elif 'HT500'in hname:
            htitle += 'HT > 500'

        hist.SetTitle(htitle)

        print hname, htitle

        setColors(_histListSR)
        setColors(_histListCR)

    return 1

def plotHists(flag = 'CR', doNorm = False, plotOpt = 'histe1'):

    if flag == 'CR':
        histList = _histListCR
    elif flag == 'SR':
        histList = _histListSR
    elif flag == 'Rcs':
        histList = _histListRcs
        plotOpt += 'e1'

    # define Canvas (plot) name
    cname = 'canvST_'+ flag

    if doNorm == True:
        cname += 'Norm'

    canv = TCanvas(cname,'L_{T} in different Nj and HT bins for '+ flag,800,800)

    ## clone hists for this plot
    histCloneList = []

    #for hist in histList:
    #histCloneList.append(hist.Clone(hist.GetName()+cname))

    #histList = histCloneList

    for ind,hist in enumerate(histList):

        #_histStore.append(hist)
        #print 'Hist name', hist.GetName()

        if doNorm:
            hist.DrawNormalized(plotOpt)
        else:
            hist.Draw(plotOpt)

        if 'same' not in plotOpt: plotOpt += 'same'

    leg = canv.BuildLegend()
    leg.SetFillColor(0)

    # set proper title
    first =  canv.GetListOfPrimitives()[0]
    first.SetTitle(canv.GetTitle())

    # Set ST/LT range
    first.GetXaxis().SetRangeUser(250,1000)

    # axis label
    first.GetXaxis().SetLabelSize(0.04)
    first.GetYaxis().SetLabelSize(0.04)

    # axis titles
    first.GetXaxis().SetTitleSize(0.05)

    first.GetYaxis().SetTitleSize(0.04)
    first.GetYaxis().SetTitleOffset(1.0)

    # Y axis mod
    if flag != 'Rcs':
        canv.SetLogy()

        if doNorm:
            first.GetYaxis().SetTitle("a.u.")
            first.GetYaxis().SetRangeUser(0.001,0.2)
    else:
        first.GetYaxis().SetTitle("R_{CS}")
        first.GetYaxis().SetRangeUser(0,1)

    _canvStore.append(canv)
    return canv

if __name__ == "__main__":

    if len(sys.argv) > 2:
        SRfileName = sys.argv[1]
        CRfileName = sys.argv[2]
        print '#SRfileName is', SRfileName
        print '#CRfileName is', CRfileName
    else:
        print '#No file names given'
        exit(0)

    srfile  = TFile(SRfileName, "READ")
    crfile  = TFile(CRfileName, "READ")

    if len(sys.argv) > 3:
        outName = sys.argv[3]
    else:
        print '#No out file name is given'
        outName = (os.path.basename(SRfileName)).replace('.root','_rcs.root')
        print '#> Out file name is', outName

    outfile = TFile(outName, "RECREATE")

    if not srfile:
        print "Couldn't open the file"
        exit(0)

    # get hists from files
    getHistsFromFile(srfile)
    getHistsFromFile(crfile)

    # customise hists
    custHists()

    # make rcs plots
    getRcsPlots()

    canvCRnorm = plotHists('CR',True)
    canvSRnorm = plotHists('SR',True)
    canvRcs = plotHists('Rcs')

    ## wait
    answ = raw_input("Enter 'q' to exit: ")

    canvCR = plotHists('CR')
    canvSR = plotHists('SR')

    ## save canvases to file
    for canv in _canvStore:
        pdir = 'plots/'
        canv.SaveAs(pdir+canv.GetName()+'.pdf')
        canv.Write()

    srfile.Close()
    crfile.Close()
    outfile.Close()
