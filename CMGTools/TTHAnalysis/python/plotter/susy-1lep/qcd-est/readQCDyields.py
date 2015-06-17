#!/usr/bin/env python

import shutil
import subprocess
import os
import glob
from multiprocessing import Pool

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

def _getYields(inargs):

    (sample, cardDir, binName, ratDict) = inargs

    if len(inargs) < 1:
        return (binName,[0,0])

    limfName = "Limits_"+sample+"_"+binName
    signfName = "Significance_"+sample+"_"+binName
    cardName = cardDir+"/"+sample+"/QCDyield_"+binName+".card.txt"

    #print "# Starting Bin:", binName

    cardf = open(cardName)

    hasSelected = False
    nSel = 0
    nAnti = 0

    for line in cardf.readlines():

        if 'process' in line and 'QCDsel' in line:
            #if 'sel' in line:
            hasSelected = True

        if 'rate' in line:
            # get yields
            if hasSelected:
                (text,nAnti,nSel) = line.split()
            else:
                (text,nAnti) = line.split()

    #print 'Yields:', nAnti, nSel
    nAnti = float(nAnti)
    nSel = float(nSel)

    # Apply f-ratios for prediction
    if ratDict != {}:
        # filter STX from binname
        stbin = binName[binName.find('ST'):binName.find('ST')+3]

        #print 'Going to apply ratios in ST bin:', stbin

        fRatio = ratDict[stbin][0]
        nPred = nAnti * ratDict[stbin][0]

        #print nAnti, fRatio, nPred , nSel


        return (binName,[nAnti,nSel,nPred])
    else:
        print 'No ratios given'
        return (binName,[nAnti,nSel,0])


# MAIN
if __name__ == "__main__":

    nJobs = 12

    ratDict = {}
    ratDict = readRatios()

    cardDirectory="yields/QCD_yields_3fb_testFull"
    cardDirectory = os.path.abspath(cardDirectory)

    '''
    limitDir = cardDirectory+"/limits_test/"
    if not os.path.isdir(limitDir):
    print 'Creating limit dir', limitDir
    os.mkdir(limitDir)

    print 'Entering out dir', limitDir
    os.chdir(limitDir)
    print
    '''

    QCDdir = 'QCDsel'
    cardPattern = 'QCDyield'

    limitdict = {}
    sigdict = {}


    print 80*'#'
    print "Yields for", QCDdir

    # get card file list
    inDir = cardDirectory+'/'+QCDdir
    cardFnames = glob.glob(inDir+'/'+ cardPattern + '_*.txt')
    cardNames = [os.path.basename(name) for name in cardFnames]
    cardNames = [(name.replace(cardPattern+'_','')).replace('.card.txt','') for name in cardNames]

    #print 'Card list', cardNames
    argTuple = [(QCDdir, cardDirectory,name, ratDict) for name in cardNames]
    #print 'Card list', argTuple

    yieldDict = {}

    # single jobs
    #for args in argTuple:
    #    (val,err) = _getYields(args)
    #    yieldDict[args[0]] = (val,err)

    # multi thread
    pool = Pool(nJobs)
    yieldDict = dict(pool.map(_getYields, argTuple))

    #print yieldDict

    # Print yields
    print "Bin:\t\tNanti\t\tNpredict\tNselect\t\tDifference(%)"

    for bin in yieldDict:

        (nAnti, nSel, nPred) = yieldDict[bin]
        #print "%s:\t%f\t%f\t%f" % ( bin, yieldDict[bin][0], yieldDict[bin][1], yieldDict[bin][2])
        print "%s:\t%f\t%f\t%f\t%f" % ( bin, nAnti, nPred, nSel, abs(nSel-nPred)/(nPred+0.00001)*100)

    '''
    #    limDict  = dict(pool.map(_, jobs)) if options.jobs > 0 else dict([_runIt(j) for j in jobs])
    limDict = dict(pool.map(_getLimits, argTuple))
    #   limDict  = dict(pool.map(_getLimits, cardNames))

    print 80*'#'
    print 'Results:'
    print 'Sample [sigma,r-value]'

    #    for key in limDict:
    #        if limDict[key][0] != -1:
    #            print key, limDict[key]

    # make dict[sigma] = samplename
    sigDict = {}
    for key in limDict:
    if limDict[key][0] != -1:
    sigDict[limDict[key][0]] = key

    sigList = sigDict.keys()
    sigList.sort(reverse = True)

    #    for sigma in sigDict:
    #        print sigma, sigDict[sigma], limDict[sigDict[sigma]]
    for sigma in sigList:
    print sigDict[sigma],'\t', limDict[sigDict[sigma]][0],'\t', limDict[sigDict[sigma]][1]
    '''
