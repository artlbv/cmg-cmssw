#!/usr/bin/env python
import sys
from ROOT import *

## ROOT STYLE
#gStyle.SetCanvasPreferGL(1)

gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadRightMargin(0.075)
gStyle.SetPadBottomMargin(0.075)
gStyle.SetLegendBorderSize(0)

## CMS LUMI
import CMS_lumi

CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_13TeV = str(2.3) + " fb^{-1}"

iPos = 0#11
if( iPos==0 ): CMS_lumi.relPosX = 0.15



## GLOBAL
colorDict = {'TTJets': kBlue-4,'TTdiLep':kBlue-7,'TTsemiLep':kBlue-2,'WJets':kGreen-2,
             'QCD':kCyan-6,'SingleT':kViolet+5,'DY':kRed-6,'TTV':kOrange-3,'data':1,'background':2,'EWK':3,
             "T1tttt_120": kYellow-6, "T1tttt_150": kMagenta}
#{'TTJets': "t#bar{t}",'TTdiLep': "t#bar{t}#rightarrowl#bar{l}",'TTsemiLep':"t#bar{t}#rightarrowl/#bar{l}",
sampLabs = {'TTJets': "t#bar{t}",'TTdiLep': "t#bar{t} ll + jets",'TTsemiLep':"t#bar{t} l + jets",
            'WJets':"W + jets", 'QCD': "QCD", 'SingleT': "t/#bar{t}",'DY':"DY + jets",'TTV':"t#bar{t}V",'data':"data",
             "T1tttt_120": "T1tttt (1200,800)", "T1tttt_150": "T1tttt (1500,100)"}

_batchMode = False
_alpha = 0.75

def getSampColor(name):

    if "TT_" in name: name = name.replace("TT_","TTJets_")

    for samp in sorted(colorDict.keys()):
        if samp == name:
            return colorDict[samp]

    for samp in sorted(colorDict.keys()):
        if samp in name:
            return colorDict[samp]

    else: return 1

def getSampLabel(name):

    if "TT_" in name: name = name.replace("TT_","TTJets_")

    for samp in sorted(sampLabs.keys()):
        if samp == name:
            return sampLabs[samp]

    for samp in sorted(sampLabs.keys()):
        if samp in name:
            return sampLabs[samp]

    else:
        print name
        return name

def readCF(fname):

    #cfdict = {}

    with open(fname,"r") as fcf:
        lines = fcf.readlines()

        # first line: get number of columns
        if "CUT" in lines[0]:
            lines[0] = lines[0].replace("ALL ","ALL")
            names = lines[0].split()
            print names
        else:
            print "No names found in first line!"
            print lines[0]
            return 0

        cfdict = {name:[] for name in names}
        #print cfdict

        # loop over content
        for line in lines[2:]:
            line = line.replace("entry point","Trigger__Like")

            cols = line.split()

            if line[0] == "#": continue

            if len(cols) != len(names):
                print len(cols), len(names)
                print "Mismatch of columns in", line
                return 0

            for i,col in enumerate(cols):

                name = names[i]
                #print name, col

                if "CUT" in name:
                    cfdict[name].append(col)
                else:
                    cfdict[name].append(float(col))

        #print cfdict
        return cfdict

    return 0

def makeHists(cfdict):

    histList = []
    hdict = {}

    if "CUT" in cfdict: labels = cfdict["CUT"]
    else: return 0

    nbins = len(labels)

    for name in cfdict:
        if "CUT" in name: continue

        conts = cfdict[name]

        hname = name
        #htitle = "Cut Flow for"+ hname
        htitle = getSampLabel(name)
        #print htitle

        hist = TH1F(hname,htitle,nbins,0,nbins)
        #print hname, htitle
        #hist = TH1F("b","h",nbins,-0.5,nbins+0.5)

        for ibin,label in enumerate(labels):

            label = label.replace("__"," ")
            label = label.replace("\,"," ")
            label = label.replace("#geq"," #geq ")
            #print label

            hist.GetXaxis().SetBinLabel(ibin+1,label)
            hist.SetBinContent(ibin+1,conts[ibin])
            hist.SetBinError(ibin+1,0)

            # style
            col = getSampColor(name)
            hist.SetLineColor(col)
            hist.SetMarkerColor(col)
            #hist.SetFillColor(col)
            if _batchMode == False: hist.SetFillColor(col)
            else: hist.SetFillColorAlpha(col,_alpha)
            #hist.SetFillStyle(3002)
            hist.SetFillStyle(1001)

        #hist.Draw("hist")
        #raw_input("continue...")

        histList.append(hist)
        hdict[name] = hist

    return hdict#histList

def getStack(histList):

    stack = THStack("stack","stack")

    for i,hist in enumerate(histList):
        stack.Add(hist)

    return stack

def doLegend(pos = "TM",nEntr = None):

    if pos == "TM":
        #leg = TLegend(0.3,0.5,0.45,0.85)
        leg = TLegend(0.15,0.7,0.9,0.9)
    elif pos == "Long":
        leg = TLegend(0.15,0.7,0.9,0.9)
    elif pos == "TRC":
        leg = TLegend(0.6,0.6,0.9,0.9)
    elif pos == "TR":
        leg = TLegend(0.5,0.6,0.9,0.9)
    elif pos == "TL":
        leg = TLegend(0.2,0.75,0.4,0.9)

    leg.SetBorderSize(1)
    #leg.SetTextFont(62)
    leg.SetTextFont(42)
    leg.SetTextSize(0.03321678)
    leg.SetLineColor(0)
    leg.SetLineStyle(0)
    leg.SetLineWidth(0)

    if _batchMode == False: leg.SetFillColor(0)
    else: leg.SetFillColorAlpha(0,_alpha)

    leg.SetFillStyle(1001)
    #leg.SetFillStyle(0)

    return leg


if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        fname = sys.argv[1]
        print '# fname is', fname
    else:
        fname = "cf_test.txt"
    #fname = "mycf.txt"

    cfd = readCF(fname)
    print cfd.keys()

    hdict = makeHists(cfd)
    #print hdict

    #samps = ['T1tttt_150', 'TTsemiLep', 'DY','TTdiLep', 'TTV', 'SingleT', 'T1tttt_120', 'WJets', 'T5tttt_1.2', 'T5tttt_1.5', 'QCD']
    #samps = ['T1tttt_150', 'TTsemiLep', 'DY', 'TTdiLep', 'TTV', 'SingleT', 'T1tttt_120', 'WJets', 'QCD']
    #samps = ['DY','TTV','QCD','SingleT','WJets','TTdiLep','TTsemiLep']
    #samps = ['DY','TTV','SingleT','WJets','TTdiLep','TTsemiLep','QCD']
    samps = ['TTV','DY','SingleT','QCD','WJets','TTdiLep','TTsemiLep',"TTJets"]

    # make hist list
    hlist = []
    #for samp in samps[::-1]:
    for samp in samps:
        if samp in hdict: hlist.append(hdict[samp])

    # make sig hist list
    sigs = ["T1tttt_120","T1tttt_150"]
    shlist = []
    for samp in sigs:
        if samp in hdict: shlist.append(hdict[samp])

    print hlist
    print shlist

    canv = TCanvas("CutFlow","CutFlow",800,800)
    canv.SetLogy()
    canv.SetTicks()

    plotOpt = "hist"

    #ymax = max([h.GetMaximum() for h in hlist])
    #ymin = min([h.GetMinimum() for h in hlist])
    ymax = sum([h.GetMaximum() for h in hlist])
    ymin = min([h.GetMinimum() for h in hlist+shlist])

    print ymax, ymin

    hdummy = hlist[0]
    hdummy.Draw()
    #hdummy.GetYaxis().SetRangeUser(0.5*ymin,5*ymax)
    hdummy.GetYaxis().SetRangeUser(5,100000000)

    stack = getStack(hlist)
    stack.Draw("same")

    #hdata = hdict["DATA"]
    #hdata.SetFillStyle(0)
    #hdata.Draw("same")

    for hsig in shlist:
        hsig.Scale(10)
        hsig.SetLineWidth(3)
        hsig.SetFillStyle(0)
        hsig.SetFillColor(0)
        hsig.Draw("histsame")

    '''
    for i,hist in enumerate(hlist):

        if i == 0:
            hist.Draw()
            hist.GetYaxis().SetRangeUser(0.8*ymin,1.3*ymax)
        else:
            hist.Draw(plotOpt+"same")
    '''

    '''
    leg = doLegend()
    leg.SetNColumns(4)

    for h in shlist:
        leg.AddEntry(h,h.GetTitle(),"l")

    for h in hlist:
        leg.AddEntry(h,h.GetTitle(),"f")

    leg.Draw()
    '''
    mcleg = doLegend("TR")
    mcleg.SetNColumns(2)
    for h in hlist[::-1]:
        mcleg.AddEntry(h,h.GetTitle(),"f")
    mcleg.Draw()

    sigleg = doLegend("TL")
    for h in shlist:
        sigleg.AddEntry(h,h.GetTitle(),"l")
    sigleg.Draw()


    gPad.RedrawAxis()
    CMS_lumi.CMS_lumi(canv, 4, iPos)

    canv.SaveAs("plots_"+fname.replace(".txt",".root"))
    canv.SaveAs("plots_"+fname.replace(".txt",".pdf"))

    if _batchMode == False:
        raw_input("continue...")

