#Email:fanyucai1@126.com
#2019.1.4

import subprocess
import os
import argparse
"""
As follow suggest msi score cutoff 11% for tumor only data. (msi high: msi score >= 11%)
Niu B, Ye K, Zhang Q, et al. MSIsensor: microsatellite instability detection using paired tumor-normal sequence data[J]. Bioinformatics, 2013, 30(7): 1015-1016.

"""
msisensor="/data02/software/MSIsensor/msisensor/msisensor"
parser=argparse.ArgumentParser("This script will compute the MSI-score.")
parser.add_argument("-n","--normal",type=str,help="normal bam file")
parser.add_argument("-r","--ref",type="str",help="reference genome fasta",required=True)
parser.add_argument("-t","--tumor",type=str,help="tumor bam file",required=True)
parser.add_argument("-o","--outdir",type=str,help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",type=str,help="prefix of output",defualt="MSI")
parser.add_argument("-e","--bed",type=str,help="bed file,optional")
parser.add_argument("-c","--coverage",type=str,help="coverage threshold for msi analysis, WXS: 20; WGS: 15",result=True)
parser.add_argument("-f","--fdr",type=str,help="FDR threshold for somatic sites detection, default=0.05",default=0.05)
result=parser.parse_args()

result.ref=os.path.abspath(result.ref)
result.tumor=os.path.abspath(result.tumor)
if result.outdir:
    result.outdir = os.path.abspath(result.outdir)
    subprocess.check_call("mkdir -p %s" %(result.outdir),shell=True)
subprocess.check_call("%s scan %s -o %s/microsatellites.list"%(msisensor,result.ref,result.outdir),shell=True)
par=""
if result.normal:
    result.normal=os.path.abspath(result.normal)
    par+=" -n %s " %(result.normal)
if result.bed:
    result.bed=os.path.abspath(result.bed)
    par+=" -e %s " %(result.bed)
par+=" -f %s -t %s -o %s/%s -c %s " %(result.fdr,result.tumor,result.outdir,result.prefix,result.coverage)
subprocess.check_call("%s msi -d %s/microsatellites.list %s " %(msisensor,result.outdir,par),shell=True)