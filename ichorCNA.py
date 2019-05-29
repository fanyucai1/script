#Email:fanyucai1@126.com
#2019.3.23

import os
import argparse
import subprocess
R="/software/R/R-v3.5.2/bin/"
HMMcopy="/software/hmmcopy_utils/hmmcopy_utils-master/bin/"
ichorCNA="/software/ichorCNA/ichorCNA-master"

parser=argparse.ArgumentParser("Use ichorCNA to evaluate the prognostic role of cfDNA tumor fraction")
parser.add_argument("--bam",help="bam files",required=True)
parser.add_argument("--bin",help="bin size(kb)",required=True,choices=[10,50,500,1000])
parser.add_argument("--prefix",help="prefix of output",required=True)
parser.add_argument("--outdir",help="output diretory",required=True)
args=parser.parse_args()
bin=args.bin*1000
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
out=args.outdir
out+=args.prefix
args.bam=os.path.abspath(args.bam)
######################Generate Read Count File
cmd="%s/readCounter  --window %s --quality 20 --chromosome \"1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,X,Y\" %s >%s.wig" \
    %(HMMcopy,bin,args.bam,out)
subprocess.check_call(cmd,shell=True)
#######################run ichorCNA
par="--gcWig %s/inst/extdata/gc_hg19_%skb.wig " %(ichorCNA,args.bin)
par+="--mapWig %s/inst/extdata/map_hg19_%skb.wig " %(ichorCNA,args.bin)
par+="--centromere %s/inst/extdata/GRCh37.p13_centromere_UCSC-gapTable.txt "%(ichorCNA)
####################Low tumor content samples (early stage disease)https://github.com/broadinstitute/ichorCNA/wiki/Parameter-tuning-and-settings#low-tumor-content-samples-early-stage-disease
par+="--ploidy \"c(2)\" "
par+="--normal \"c(0.95, 0.99, 0.995, 0.999)\" "
par+="--chrs \"c(1:22)\" --chrTrain \"c(1:22)\" "
par+="--estimateScPrevalence FALSE --scStates \"c()\" "
par+="--maxCN 4 "
if args.bin==1000:
    par+="--normalPanel %s/inst/extdata/HD_ULP_PoN_1Mb_median_normAutosome_mapScoreFiltered_median.rds"
if args.bin==500:
    par+="--normalPanel %s/inst/extdata/HD_ULP_PoN_500kb_median_normAutosome_mapScoreFiltered_median.rds"
cmd="%s/Rscript %s/scripts/runIchorCNA.R --id %s --WIG %s.wig %s --outDir %s" \
    %(R,ichorCNA,args.prefix,out,par,args.outdir)
subprocess.check_call(cmd,shell=True)