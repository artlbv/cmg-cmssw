#!/usr/bin/env python
from CMGTools.TTHAnalysis.treeReAnalyzer import *
from glob import glob
import os.path, re

MODULES = []

from CMGTools.SUSYAnalysis.tools.eventVars_1l_base import EventVars1L_base
MODULES.append( ('1l_Basics', EventVars1L_base()) )
# triggers
from CMGTools.SUSYAnalysis.tools.eventVars_1l_triggers import EventVars1L_triggers
MODULES.append( ('1l_Triggers', EventVars1L_triggers()) )
## DATA only
# for Filters
from CMGTools.SUSYAnalysis.tools.eventVars_1l_filters import EventVars1L_filters
MODULES.append( ('1l_Filters', EventVars1L_filters()) )
### MC only
# for pileup
from CMGTools.SUSYAnalysis.tools.eventVars_1l_pileup import EventVars1L_pileup
MODULES.append( ('1l_Pileup', EventVars1L_pileup()) )
# for signal masses
from CMGTools.SUSYAnalysis.tools.eventVars_1l_signal import EventVars1L_signal
MODULES.append( ('1l_Signal', EventVars1L_signal()) )
# for LeptonSF
from CMGTools.SUSYAnalysis.tools.eventVars_1l_leptonSF import EventVars1L_leptonSF
MODULES.append( ('1l_LeptonSF', EventVars1L_leptonSF()) )
# for BtagSF
from CMGTools.SUSYAnalysis.tools.eventVars_1l_btagSF import EventVars1L_btagSF
MODULES.append( ('1l_LeptonSF', EventVars1L_btagSF()) )
# Top pt reweighting
from CMGTools.SUSYAnalysis.tools.eventVars_1l_WeightsForSystematics import EventVars1LWeightsForSystematics
MODULES.append( ('1l_SysWeights', EventVars1LWeightsForSystematics()) )

'''
from CMGTools.SUSYAnalysis.tools.eventVars_1l_bkgDilep import EventVars1L_bkgDilep
MODULES.append( ('1l_bkgDilep', EventVars1L_bkgDilep()) )
from CMGTools.SUSYAnalysis.tools.eventVars_1l_top import EventVars1L_Top
MODULES.append( ('1l_TopVars', EventVars1L_Top()) )
#from CMGTools.SUSYAnalysis.tools.eventVars_1l_extra import EventVars1L_extra
#MODULES.append( ('1l_Extra', EventVars1L_extra()) )
from CMGTools.SUSYAnalysis.tools.resolvedTopTagVars_1l import resolvedTopTagVars1l
MODULES.append( ('1l_resolvedTopTagVars', resolvedTopTagVars1l()) )

from CMGTools.SUSYAnalysis.tools.eventVars_1l_genLevel import EventVars1LGenLevel
MODULES.append( ('1l_BasicsGen', EventVars1LGenLevel()) )
'''

class VariableProducer(Module):
    def __init__(self,name,booker,modules):
        Module.__init__(self,name,booker)
        self._modules = modules
    def beginJob(self):
        self.t = PyTree(self.book("TTree","t","t"))
        self.branches = {}
        for name,mod in self._modules:
            for B in mod.listBranches():
                # don't add the same branch twice
                if B in self.branches:
                    print "Will not add branch %s twice" % (B,)
                    continue
                self.branches[B] = True
                if type(B) == tuple:
                    if len(B) == 2:
                        self.t.branch(B[0],B[1])
                    elif len(B) == 4:
                        self.t.branch(B[0],B[1],n=B[2],lenVar=B[3])
                else:
                    self.t.branch(B ,"F")
    def analyze(self,event):
        keyvals = {}
        for name,mod in self._modules:
            #keyvals = mod(event)
            keyvals.update(mod(event, keyvals))
        for B,V in keyvals.iteritems():
            setattr(self.t, B, V)
            setattr(event,  B, V)
        self.t.fill()

import os, itertools

from optparse import OptionParser
parser = OptionParser(usage="%prog [options] <TREE_DIR> <OUT>")
parser.add_option("-m", "--modules", dest="modules",  type="string", default=[], action="append", help="Run these modules");
parser.add_option("-d", "--dataset", dest="datasets",  type="string", default=[], action="append", help="Process only this dataset (or dataset if specified multiple times)");
parser.add_option("-D", "--dm", "--dataset-match", dest="datasetMatches",  type="string", default=[], action="append", help="Process only this dataset (or dataset if specified multiple times): REGEXP");
parser.add_option("-c", "--chunk",   dest="chunks",    type="int",    default=[], action="append", help="Process only these chunks (works only if a single dataset is selected with -d)");
parser.add_option("-N", "--events",  dest="chunkSize", type="int",    default=500000, help="Default chunk size when splitting trees");
parser.add_option("-j", "--jobs",    dest="jobs",      type="int",    default=1, help="Use N threads");
parser.add_option("-p", "--pretend", dest="pretend",   action="store_true", default=False, help="Don't run anything");
parser.add_option("-T", "--tree-dir",   dest="treeDir",     type="string", default="sf", help="Directory of the friend tree in the file (default: 'sf')");
parser.add_option("-q", "--queue",   dest="queue",     type="string", default=False, help="Run jobs on lxbatch instead of locally");
parser.add_option("-b", "--naf",     dest="naf",     action="store_true", default=None, help="Run jobs on nafbatch instead of locally");
parser.add_option("-t", "--tree",    dest="tree",      default='treeProducerSusySingleLepton', help="Pattern for tree name");
parser.add_option("-V", "--vector",  dest="vectorTree", action="store_true", default=True, help="Input tree is a vector");
parser.add_option("-F", "--add-friend",    dest="friendTrees",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename). Can use {name}, {cname} patterns in the treename")
parser.add_option("--FMC", "--add-friend-mc",    dest="friendTreesMC",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to MC only. Can use {name}, {cname} patterns in the treename")
parser.add_option("--FD", "--add-friend-data",    dest="friendTreesData",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to data trees only. Can use {name}, {cname} patterns in the treename")
parser.add_option("-L", "--list-modules",  dest="listModules", action="store_true", default=False, help="just list the configured modules");
parser.add_option("-n", "--new",  dest="newOnly", action="store_true", default=False, help="Make only missing trees");
(options, args) = parser.parse_args()

if options.listModules:
    print "List of modules"
    for (n,x) in MODULES:
        print "   '%s': %s" % (n,x)
    exit()

if len(args) != 2 or not os.path.isdir(args[0]):
    print "Usage: program <TREE_DIR> <OUT>"
    exit()
if len(options.chunks) != 0 and len(options.datasets) != 1:
    print "must specify a single dataset with -d if using -c to select chunks"
    exit()

if not os.path.isdir(args[1]): os.makedirs(args[1])

jobs = []
frpref = "evVarFriend_"
#frpref = ""

for D in glob(args[0]+"/*"):
    treename = options.tree
    fname    = "%s/%s/%s_tree.root" % (D,options.tree,options.tree)
    if (not os.path.exists(fname)) and os.path.exists("%s/%s/tree.root" % (D,options.tree)):
        treename = "tree"
        fname    = "%s/%s/tree.root" % (D,options.tree)
    if os.path.exists(fname):
        short = os.path.basename(D)
        if options.datasets != []:
            if short not in options.datasets: continue
        if options.datasetMatches != []:
            found = False
            for dm in  options.datasetMatches:
                if re.match(dm,short): found = True
            if not found: continue
        data = ("DoubleMu" in short or "MuEG" in short or "DoubleElectron" in short or "SingleMu" in short or "SingleEl" in short)
        f = ROOT.TFile.Open(fname);
        t = f.Get(treename)
        entries = t.GetEntries()
        f.Close()
        if options.newOnly:
            fout = "%s/" % (args[1]) + frpref + "%s.root"%(short)
            if os.path.exists(fout):
                #f = ROOT.TFile.Open(fname);
                #t = f.Get(treename)
                f = ROOT.TFile.Open(fout);
                t = f.Get(options.treeDir+'/t')
                if t.GetEntries() != entries:
                    print "Component %s has to be remade, mismatching number of entries (%d vs %d)" % (short, entries, t.GetEntries())
                    f.Close()
                else:
                    print "Component %s exists already and has matching number of entries (%d)" % (short, entries)
                    continue
        chunk = options.chunkSize
        if entries < chunk:
            print "  ",os.path.basename(D),("  DATA" if data else "  MC")," single chunk"
            jobs.append((short,fname,"%s/"  % (args[1]) + frpref + "%s.root" %(short),data,xrange(entries),-1))
        else:
            nchunk = int(ceil(entries/float(chunk)))
            print "  ",os.path.basename(D),("  DATA" if data else "  MC")," %d chunks" % nchunk
            for i in xrange(nchunk):
                if options.chunks != []:
                    if i not in options.chunks: continue
                r = xrange(int(i*chunk),min(int((i+1)*chunk),entries))
                jobs.append((short,fname,"%s/"% (args[1]) + frpref + "%s.chunk%05d.root" %(short,i),data,r,i))
print "\n"

if len(jobs) != 0:
    print "I have %d tasks to process" % len(jobs)
else:
    print "Found 0 jobs! Exiting"
    exit()

if options.queue:
    import os, sys
    basecmd = "bsub -q {queue} {dir}/lxbatch_runner.sh {dir} {cmssw} python {self} -N {chunkSize} -T '{tdir}' -t {tree} {data} {output}".format(
        queue = options.queue, dir = os.getcwd(), cmssw = os.environ['CMSSW_BASE'],
        self=sys.argv[0], chunkSize=options.chunkSize, tdir=options.treeDir, tree=options.tree, data=args[0], output=args[1]
        )
    if options.vectorTree: basecmd += " --vector "
    friendPost =  "".join(["  -F  %s %s " % (fn,ft) for fn,ft in options.friendTrees])
    friendPost += "".join([" --FM %s %s " % (fn,ft) for fn,ft in options.friendTreesMC])
    friendPost += "".join([" --FD %s %s " % (fn,ft) for fn,ft in options.friendTreesData])
    friendPost += "".join(["  -m  '%s'  " % m for m in options.modules])
    for (name,fin,fout,data,range,chunk) in jobs:
        if chunk != -1:
            print "{base} -d {data} -c {chunk} {post}".format(base=basecmd, data=name, chunk=chunk, post=friendPost)
        else:
            print "{base} -d {data} {post}".format(base=basecmd, data=name, chunk=chunk, post=friendPost)

    exit()

if options.naf:
    import os, sys
    import subprocess

    outdir = args[1]

    # check for number of jobs
    if len(jobs) > 5000:
        answ = raw_input("Do you really want to submit %i jobs? [y/n] " %len(jobs) )
        if 'y' not in answ: exit()

    # make unique name for jobslist
    import time
    itime = int(time.time())
    jobListName = outdir+'/jobList_%i.txt' %(itime)
    jobList = open(jobListName,'w')
    print 'Filling %s with job commands' % (jobListName)

    basecmd = "python {self} -N {chunkSize} -T '{tdir}' -t {tree} {data} {output}".format(
        njobs=1, self=sys.argv[0], chunkSize=options.chunkSize, tdir=options.treeDir, tree=options.tree, data=args[0], output=args[1]
        )
    if options.vectorTree: basecmd += " --vector "
    friendPost =  "".join(["  -F  %s %s " % (fn,ft) for fn,ft in options.friendTrees])
    friendPost += "".join([" --FM %s %s " % (fn,ft) for fn,ft in options.friendTreesMC])
    friendPost += "".join([" --FD %s %s " % (fn,ft) for fn,ft in options.friendTreesData])
    friendPost += "".join(["  -m  '%s'  " % m for m in options.modules])

    for (name,fin,fout,data,range,chunk) in jobs:
        if chunk != -1:
            #print "{base} -d {data} -c {chunk} {post}".format(base=basecmd, data=name, chunk=chunk, post=friendPost)
            jobList.write("{base} -d {data} -c {chunk} {post}".format(base=basecmd, data=name, chunk=chunk, post=friendPost)+'\n')
        else:
            #print "{base} -d {data} {post}".format(base=basecmd, data=name, chunk=chunk, post=friendPost)
            jobList.write("{base} -d {data} {post}".format(base=basecmd, data=name, chunk=chunk, post=friendPost)+'\n')

    # check log dir
    logdir = 'logs'
    if not os.path.exists(logdir): os.system("mkdir -p "+logdir)

    # submit job array on list
    subCmd = 'qsub -t 1-%s -o logs nafbatch_runner.sh %s' %(len(jobs),jobListName)
    print 'Going to submit', len(jobs), 'jobs with', subCmd
    args=subCmd.split()

    #subprocess.Popen(args)
    subprocess.call(args) #will run immediately

    jobList.close()
    exit()

def getSampName(name, tname):
    if "/tree.root" in name:
        samp = name.replace("/"+tname+"/tree.root","")
        samp = os.path.basename(samp)
        return samp
    else: return name

maintimer = ROOT.TStopwatch()
def _runIt(myargs):
    (name,fin,fout,data,range,chunk) = myargs
    timer = ROOT.TStopwatch()
    fb = ROOT.TFile(fin)
    tb = fb.Get(options.tree)
    if not tb: tb = fb.Get("tree") # new trees
    if options.vectorTree:
        tb.vectorTree = True
    else:
        tb.vectorTree = False
    friends = options.friendTrees[:]
    friends += (options.friendTreesData if data else options.friendTreesMC)
    friends_ = [] # to make sure pyroot does not delete them
    for tf_tree,tf_file in friends:
        tf = tb.AddFriend(tf_tree, tf_file.format(name=name, cname=name)),
        friends_.append(tf) # to make sure pyroot does not delete them
    nev = tb.GetEntries()
    if options.pretend:
        print "==== pretending to run %s (%d entries, %s) ====" % (name, nev, fout)
        return (name,(nev,0))
    print "==== %s starting (%d entries) ====" % (name, nev)
    booker = Booker(fout)
    modulesToRun = MODULES
    '''
    # remove filter module for MC
    if not data:
        print modulesToRun
        print "removing filters module"
        modulesToRun.remove( ('1l_Filters', EventVars1L_filters()) )
    '''
    # Save sample name in module
    for m,v in MODULES:
        v.sample = getSampName(fin,options.tree)

    if options.modules != []:
        toRun = {}
        for m,v in MODULES:
            for pat in options.modules:
                if re.match(pat,m):
                    toRun[m] = True
        modulesToRun = [ (m,v) for (m,v) in MODULES if m in toRun ]
    el = EventLoop([ VariableProducer(options.treeDir,booker,modulesToRun), ])
    el.loop([tb], eventRange=range)
    booker.done()
    fb.Close()
    time = timer.RealTime()
    print "=== %s done (%d entries, %.0f s, %.0f e/s) ====" % ( name, nev, time,(nev/time) )
    return (name,(nev,time))

if options.jobs > 0:
    from multiprocessing import Pool
    pool = Pool(options.jobs)
    ret  = dict(pool.map(_runIt, jobs)) if options.jobs > 0 else dict([_runIt(j) for j in jobs])
else:
    ret = dict(map(_runIt, jobs))
fulltime = maintimer.RealTime()
totev   = sum([ev   for (ev,time) in ret.itervalues()])
tottime = sum([time for (ev,time) in ret.itervalues()])
print "Done %d tasks in %.1f min (%d entries, %.1f min)" % (len(jobs),fulltime/60.,totev,tottime/60.)
