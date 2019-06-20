import os
import sys
import argparse
sub=os.path.abspath(__file__)
dir_name=os.path.dirname(sub)
sys.path.append(dir_name)
import core
import shutil
parser=argparse.ArgumentParser("Copy the TSO500.")
parser.add_argument("-a","--analysis",help="analysis directory",required=True)
parser.add_argument("-s","--samplelist",help="sample list",required=True)
parser.add_argument("-o","--outdir",help="output directory",required=True)
args=parser.parse_args()

###########################
args.analysis=os.path.abspath(args.analysis)
args.outdir=os.path.abspath(args.outdir)
args.samplelist=os.path.abspath(args.samplelist)
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
if not os.path.exists("%s/SNV"%(args.outdir)):
    os.mkdir("%s/SNV"%(args.outdir))
if not os.path.exists("%s/CNV"%(args.outdir)):
    os.mkdir("%s/CNV"%(args.outdir))
if not os.path.exists("%s/fusion"%(args.outdir)):
    os.mkdir("%s/fusion"%(args.outdir))
if not os.path.exists("%s/TMB_MSI"%(args.outdir)):
    os.mkdir("%s/TMB_MSI" % (args.outdir))
##########################run CNV
#core.CNV.run(args.analysis,args.samplelist,"%s/CNV"%(args.outdir))
##########################run somatic
#core.somatic.run(args.analysis,args.samplelist,0,"%s/SNV"%(args.outdir))
##########################TMB and MSI
shutil.copy("%s/Results/*BiomarkerReport.txt"%(args.analysis),"%s/TMB_MSI"%(args.outdir))
##########################run stat
core.stat.run(args.samplelist)