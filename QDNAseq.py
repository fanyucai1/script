#Email:fanyucai1@126.com
#2019.3.20

import argparse
import os
import subprocess
import math

qsub="/home/fanyucai/bin/qsub_sge.pl"
#download from:http://genome.ucsc.edu/cgi-bin/hgFileUi?db=hg19&g=wgEncodeMapability
bigWigFile="/software/QDNAseq/wgEncodeCrgMapabilityAlign50mer.bigWig"
bigWigAverageOverBed="/software/ucsc-tools/bigWigAverageOverBed"
backlist=[]
backlist[0]="/software/QDNAseq/wgEncodeDacMapabilityConsensusExcludable.bed"
backlist[1]="/software/QDNAseq/wgEncodeDukeMapabilityRegionsExcludable.bed"
bin_file="/software/QDNAseq"
R="/software/R/R-v3.5.2/bin"

parser=argparse.ArgumentParser("")
parser.add_argument("--bam_dir",help="directory contains bam file",required=True)
parser.add_argument("--bin",help="bin size",required=True,choices=[1,5,10,15,30,50,100,500,1000])
parser.add_argument("-o","--outdir",help="output directory",required=True)
args=parser.parse_args()

for i in range(len(args.bam)):
    args.bam[i]=os.path.abspath(args.bam[i])
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
#########################################Generating bin annotations
shell=open("%s/QDNAseq.Rscript" %(args.outdir),"w")
shell.write("#!%s/Rscript" %(R))
shell.write("library(QDNAseq)")
shell.write("library(Biobase)")
shell.write("library(BSgenome.Hsapiens.UCSC.hg19)")
shell.write("bins <- getBinAnnotations(binSize=%s,path=\'%s\',genome=\"hg19\")" %(args.bin,bin_file))
shell.write("readCounts=binReadCounts(bins, path=\'%s\')" %(args.bam_dir))
shell.write("readCountsFiltered=applyFilters(readCounts,residual=TRUE, blacklist=TRUE)")
#Calculating GC content and mappability
shell.write("readCountsFiltered= estimateCorrection(readCountsFiltered)")
#apply the correction for GC content and mappability
shell.write("copyNumbers = correctBins(readCountsFiltered)")
#median normalization
shell.write("copyNumbersNormalized = normalizeBins(copyNumbers)")
shell.write("copyNumbersSmooth =smoothOutlierBins(copyNumbersNormalized)")
shell.write("exportBins(copyNumbersSmooth, file=\"$%/counts.txt\")" %(args.outdir))
shell.close()
#########################################
subprocess.check_call("%s/Rscript %s/QDNAseq.Rscript" %(R),shell=True)
#########################################
infile=open("%s/counts.txt" %(args.outdir),"r")
outfile=open("%s/counts_log2.txt")
outfile.write("chromosome\tstart\tend\tusebin")
i=-1;
for line in infile:
    line = line.strip()
    list = line.split("\t")
    i+=1
    if i==1:
        outfile.write("%s\t%s\t%s\tusebin" % (list[1],list[2],list[3]))
        for i in range(4,len(list)):
            outfile.write("\t%s" %(list[i]))
        outfile.write("\n")
    else:
        outfile.write("%s\t%s\t%s\tTRUE" % (list[1], list[2], list[3]))
        for i in range(4,len(list)):
            outfile.write("\t%s" %(list[i]))
        outfile.write("\n")
infile.close()
outfile.close()
