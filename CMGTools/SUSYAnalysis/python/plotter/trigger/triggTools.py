#!/usr/bin/python

import os
from ROOT import *

import CMS_lumi
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12

gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetPadTopMargin(0.05)
gStyle.SetOptFit()

gStyle.SetLabelFont(62)
gStyle.SetTitleFont(62)

#gStyle.SetPalette(53)
#gStyle.SetCanvasPreferGL(True)

_colorList = [2,4,8,9,7,3,6] + range(10,50)

def varToLabel(var):

    label = var

    if 'pt' in var:
        label = 'p_{T}(lep)'
    elif 'MET' in var:
        label = 'E_{T}^{miss}'
    elif 'T' in var:
        label = var.replace('T','_{T}')

    return label

def getLegend(pos = 'ne'):
    if pos == 'ne':
        leg = TLegend(0.4,0.7,0.9,0.9)
    elif pos == 'log':
        leg = TLegend(0.6,0.8,0.99,0.99)
    elif pos == 'roc':
        leg = TLegend(0.15,0.2,0.7,0.4)
    elif pos == 'fit':
        leg = TLegend(0.15,0.75,0.5,0.9)
    elif pos == '2d':
        leg = TLegend(0.3,0.75,0.85,0.9)

    leg.SetBorderSize(1)
    leg.SetTextFont(62)
    leg.SetTextSize(0.03321678)
    leg.SetLineColor(0)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(1001)

    return leg

def turnon_func(x, par):

    halfpoint = par[0]
    width = max(par[1],1)
    plateau = par[2]

    #offset = par[3]
    #plateau = 1.0
    offset = 0

    pt = TMath.Max(x[0],0.000001)

    arg = 0
    #print pt, halfpoint, width
    arg = (pt - halfpoint) / (width * TMath.Sqrt(2))

    fitval = offset + plateau * 0.5 * (1 + TMath.Erf(arg))
    #fitval = offset + plateau * TMath.Erfc(arg)

    return fitval

def cutsToString(cutList):

    cutstr = ''

    for i, cut in enumerate(cutList):
        cutstr += cut

        if i != len(cutList)-1: cutstr += ' && '

    return cutstr

def saveCanvases(canvList, pdir = '', extraName = '', _batchMode = True):

    ## save canvases to file
    extList = ['.png','.pdf']

    prefix = ''
    if extraName != '':
        suffix = '_' + extraName
    else:
        suffix = ''

    ## wait
    if not _batchMode:
        answ = raw_input("'Enter' to proceed (or 'q' to exit): ")
        if 'q' in answ: exit(0)


    cdir = os.path.dirname(pdir + prefix)
    print 'Canvas dir is', cdir

    if not os.path.exists(cdir):
        os.makedirs(cdir)

    cdir += '/'

    # make output file
    outName = cdir + 'plots_'+ extraName +'.root'
    ofile = TFile(outName,'RECREATE')

    for canv in canvList:
        for ext in extList:
            cname = canv.GetName().replace('Lep_pt','LepPt')
            cname = cdir + cname+ suffix + ext
            canv.SaveAs(cname)
        canv.Write()

    '''
    # empty stores for further use
    del _canvStore[:]
    _histStore.clear()
    _hEffStore.clear()
    del _fitrStore[:]
    '''

    ofile.Close()

    return 1

def renameTrig(trigName):

    trigName = trigName.replace('SingleMu','IsoMu27')
    trigName = trigName.replace('Mu50NoIso','Mu50')
    trigName = trigName.replace('ElNoIso','El105')
    trigName = trigName.replace('SingleEl','El32')
    trigName = trigName.replace('HTMET','HT350MET120')

    return trigName

