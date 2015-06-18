#!/usr/bin/env python

import shutil
import subprocess
import os
import glob
from multiprocessing import Pool
from ROOT import *

def readRatios(fname = "f_ratios_NJ34_Nb0.txt"):

    ratioDict = {}

    rfile = open(fname)

    for line in rfile.readlines():

        if 'ST' in line:
            (name,ratio,err) = line.split()

            # filter STX
            stbin = name[name.find('ST'):name.find('ST')+3]

            ratioDict[stbin] = (float(ratio),float(err))

    print 'Read ratios from', fname
    for bin in ratioDict:
        print "%s:\t%f +/- %f" %(bin, ratioDict[bin][0], ratioDict[bin][1])

    return ratioDict

def applyRatio(binname, nAnti):
    # scale yield with ratio and get correct yield

    return (nPred, nPredErr)

def _getYieldsFromInput(inargs):

    (sample, cardDir, binName, ratDict) = inargs

    if len(inargs) < 1:
        return (binName,[0,0])

    cardName = cardDir+"/common/QCDyield_"+binName+".input.root"

    #print "# Starting Bin:", binName

    cardf = TFile(cardName,"READ")

    # get anti-selected histo
    hAnti = cardf.Get("x_QCDanti")
    nAnti = hAnti.Integral()
    nAntiErr = hAnti.GetBinError(1)

    # get selected histo
    hSel = cardf.Get("x_QCDsel")
    nSel = hSel.Integral()
    nSelErr = hSel.GetBinError(1)

    nPred = 0
    nPredErr = 0

    # Apply f-ratios for prediction
    if ratDict != {} and nAnti != 0:
        # filter STX from binname
        stbin = binName[binName.find('ST'):binName.find('ST')+3]

        #print 'Going to apply ratios in ST bin:', stbin

        fRatio = ratDict[stbin][0]
        fRatioErr = ratDict[stbin][1]

        nPred = nAnti * fRatio

        nPredErr = nPred * sqrt(nAntiErr/nAnti*nAntiErr/nAnti +  fRatioErr/fRatio*fRatioErr/fRatio)
        #print nAnti, fRatio, nPred , nSel

        return (binName,[nAnti, nAntiErr,nSel, nSelErr, nPred, nPredErr])
    else:
        #print 'No ratios given'
        return (binName,[nAnti, nAntiErr,nSel, nSelErr, nPred, nPredErr])

# MAIN
if __name__ == "__main__":

    nJobs = 12

    ratDict = {}
    ratDict = readRatios()

    cardDirectory="yields/QCD_yields_3fb_AllBins"
    cardDirectory = os.path.abspath(cardDirectory)

    QCDdir = 'common'
    cardPattern = 'QCDyield'

    limitdict = {}
    sigdict = {}


    #print 80*'#'
    #print "Yields for", QCDdir

    # get card file list
    inDir = cardDirectory+'/'+QCDdir
    cardFnames = glob.glob(inDir+'/'+ cardPattern + '_*.root')
    cardNames = [os.path.basename(name) for name in cardFnames]
    cardNames = [(name.replace(cardPattern+'_','')).replace('.input.root','') for name in cardNames]

    #print 'Card list', cardNames
    argTuple = [(QCDdir, cardDirectory,name, ratDict) for name in cardNames]
    #print 'Card list', argTuple

    yieldDict = {}

    # single jobs
    #for args in argTuple:
    #    _getYieldsFromInput(args)
    #    yieldDict[args[0]] = (val,err)

    # multi thread
    pool = Pool(nJobs)
    yieldDict = dict(pool.map(_getYieldsFromInput, argTuple))

    ykeys = sorted(yieldDict.keys())

    #print 'KEYS', sorted(ykeys)

    # Print yields
    print 80*'#'
    print "Yields with zero difference"
    print "Bin:\t\tNanti\t\t\t\t\tNpredict\t\t\t\tNselect\t\t\t\t\tDifference(%)"

    for bin in ykeys:#yieldDict:

        (nAnti, nAntiErr,nSel, nSelErr, nPred, nPredErr) = yieldDict[bin]

        if nSel != 0:
            diff = abs(nSel-nPred)/(nSel)*100
        else:
            diff = 0

        if diff == 0:
            print "%s:\t%f\t+/-\t%f\t%f\t+/-\t%f\t%f\t+/-\t%f\t%f" % ( bin, nAnti, nAntiErr, nPred, nPredErr, nSel, nSelErr, diff)

    print 80*'#'
    print "Yields with non-zero difference"
    print "Bin:\t\tNanti\t\t\t\t\tNpredict\t\t\t\tNselect\t\t\t\t\tDifference(%)"
    for bin in ykeys:#yieldDict:

        (nAnti, nAntiErr,nSel, nSelErr, nPred, nPredErr) = yieldDict[bin]

        if nSel != 0:
            diff = abs(nSel-nPred)/(nSel)*100
        else:
            diff = 0

        if diff != 0:
            print "%s:\t%f\t+/-\t%f\t%f\t+/-\t%f\t%f\t+/-\t%f\t%f" % ( bin, nAnti, nAntiErr, nPred, nPredErr, nSel, nSelErr, diff)
