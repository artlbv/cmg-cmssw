from yieldClass import *
from searchBins import *


if __name__ == "__main__":

    pattern = "Yields/wData/jecv7_fixSR/lumi2p3fb/allbins/allSF_noPU/merged/"

    #BinMask LTX_HTX_NBX_NJX for canvas names
    basename = os.path.basename(pattern)
    mask = basename.replace("*","X_")

    ## Create Yield Storage
    yds = YieldStore("lepYields")
    yds.addFromFiles(pattern,("lep","sele"))
    yds.showStats()

    '''
    rcsMB = yds.getSampDict("EWK","Rcs_MB")
    rcsSB = yds.getSampDict("EWK","Rcs_MB")
    kaps = yds.getSampDict("EWK","Kappa")

    print rcsMB.keys()

    '''
    samps = [
        ("EWK","Rcs_MB"),
        ("EWK","Rcs_SB"),
        ("EWK","Kappa"),
        ]
    #print yds.getMixDict(samps)
    #yds.printMixBins(samps)

    ydmix = yds.getMixDict(samps)
    bins = sorted(ydmix.keys())

    for nj in ["NJ68","NJ9i"]:
    #for nj in ["NJ9i"]:
        #for nb in ["NB1","NB2","NB3"]:

        curNJ = None
        curLT = None
        curHT = None
        curNB = None

        for bin in bins:
            if nj in bin:

                nCols = len(samps) + len(bin.split("_"))
                nCol1 = 1

                bLT,bHT,bNB,bNJ = bin.split("_")

                #print bLT, bHT, bNJ
                #print curLT, curHT, curNJ


                if bNJ == curNJ:
                    nCol1 += 1
                    if bLT == curLT:
                        nCol1 += 1
                        if bHT == curHT:
                            nCol1 += 1
                            if bNB == curNB:
                                nCol1 += 1
                if nCol1 == 1:
                    print "\\hline \\hline"
                elif nCol1 < len(bin.split("_")):
                    print "\\cline{%i-%i}" %(nCol1,nCols)

                if bNJ != curNJ:
                    sameNJbins = [b for b in bins if (nj in b)]
                    curNJ = bNJ

                    lab = binsNJ[curNJ][1]

                    if len(sameNJbins) > 1:
                        print "\multirow{%i}{*}{%s} &\t" %(len(sameNJbins), lab),
                    else:
                        print lab, "\t\t&\t",
                else:
                    print "\t\t&\t",
                    #nCol1 -= 1

                if bLT != curLT:
                    sameLTbins = [b for b in bins if (nj in b and bLT in b)]
                    curLT = bLT
                    curHT = None
                    curNB = None

                    lab = binsLT[curLT][1]

                    if len(sameLTbins) > 1:
                        print "\multirow{%i}{*}{%s} &\t" %(len(sameLTbins), lab),
                    else:
                        print lab, "\t\t&\t",
                else:
                    print "\t\t&\t",
                    #nCol1 -= 1

                if bHT != curHT:
                    sameHTbins = [b for b in sameLTbins if (nj in b and bHT in b)]
                    curHT = bHT
                    curNB = None

                    lab = binsHT[curHT][1]

                    if len(sameHTbins) > 1:
                        print "\multirow{%i}{*}{%s} &\t" %(len(sameHTbins), lab),
                    else:
                        print lab, "\t\t&\t",
                else:
                    print "\t\t&\t",
                    #nCol1 -= 1

                if bNB != curNB:
                    sameNBbins = [b for b in sameHTbins if (nj in b and bNB in b)]
                    curNB = bNB

                    lab = binsNB[curNB][1]

                    if len(sameNBbins) > 1:
                        print "\multirow{%i}{*}{%s} &\t" %(len(sameNBbins), lab),
                    else:
                        print lab, "\t\t",
                else:
                    print "\t\t",
                    #nCol1 -= 1


                #print "\t\t\t",

                #binn = bin.replace(nj,"")
                #binn = binn.replace("_"," ")
                #print binn,"\t\t",
                #for yd in ydmix[bin]: print yd.printValue(),"\t",
                prec = "%4.4f"
                for yd in ydmix[bin]: print "& "+prec %(yd.val) +" $\pm$ "+prec %(yd.err) ,"\t",
                #print "\\\\ \\hline"
                print "\\\\"
