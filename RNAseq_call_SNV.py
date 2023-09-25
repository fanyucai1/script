#Email:fanyucai1@126.com
#2019.1.29

import os
import subprocess
import argparse
import time

GATK="/data/fyc_software/GATK/gatk-4.0.12.0/gatk"
java="export PATH=/data/fyc_software/java/jdk1.8.0_201/bin:$PATH"
ref="/data/fyc_data/hg19/ucsc.hg19.fasta"
dbsnp="/data/fyc_data/hg19/dbsnp_138.hg19.vcf.gz"
mils="/data/fyc_data/hg19/Mills_and_1000G_gold_standard.indels.hg19.sites.vcf.gz"

parser=argparse.ArgumentParser("RNAseq call SNV.(URL:https://github.com/gatk-workflows/gatk3-4-rnaseq-germline-snps-indels/blob/master/rna-germline-variant-calling.wdl)")
parser.add_argument("-s","--sam",help="sam file from STAR mapper",type=str,required=True)
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
parser.add_argument("-n","--name",help="sample name",required=True)
args=parser.parse_args()
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
args.outdir=os.path.abspath(args.outdir)
args.sam=os.path.abspath(args.sam)
os.chdir(args.outdir)
java+=" && cd %s" %(args.outdir)
start=time.time()
###############################################(Assigns all the reads in a file to a single new read-group)
cmd="%s && %s --java-options \"-Xmx10G -Djava.io.tmpdir=./\" AddOrReplaceReadGroups -I %s -O %s.sort.bam -SM %s -PU %s -ID %s -LB library1 -PL illumina -SO coordinate" \
    %(java,GATK,args.sam,args.name,args.name,args.name,args.name)
subprocess.check_call(cmd,shell=True)
###############################################locates and tags duplicate reads in a BAM or SAM file
cmd="%s && %s --java-options \"-Xmx10G -Djava.io.tmpdir=./\" MarkDuplicates -I %s.sort.bam -O %s.dump.bam -M %s.txt" \
    %(java,GATK,args.name,args.name,args.name)
subprocess.check_call(cmd,shell=True)
###############################################Generates a BAM index ".bai" file
cmd="%s && %s --java-options \"-Xmx10G -Djava.io.tmpdir=./\" BuildBamIndex -I %s.dump.bam" %(java,GATK,args.name)
subprocess.check_call(cmd,shell=True)
###############################################Splits reads that contain Ns in their cigar string
cmd="%s && %s --java-options \"-Xmx10G -Djava.io.tmpdir=./\" SplitNCigarReads -R %s -I %s.dump.bam -O %s.SplitNCigarReads.bam" %(java,GATK,ref,args.name,args.name)
subprocess.check_call(cmd,shell=True)
###############################################BaseRecalibrator
cmd="%s && %s --java-options \"-Xmx10G -Djava.io.tmpdir=./\" BaseRecalibrator -R %s --known-sites %s --known-sites %s -I %s.SplitNCigarReads.bam -O %s.recal_data.table" \
    %(java,GATK,ref,dbsnp,mils,args.name,args.name)
subprocess.check_call(cmd,shell=True)
###############################################ApplyBQSR
cmd="%s && %s --java-options \"-Xmx10G -Djava.io.tmpdir=./\" ApplyBQSR -R %s -I %s.SplitNCigarReads.bam --bqsr-recal-file %s.recal_data.table -O %s.recal.bam" \
    %(java,GATK,ref,args.name,args.name,args.name)
subprocess.check_call(cmd,shell=True)
###############################################call snv
cmd="%s && %s --java-options \"-Xmx10G -Djava.io.tmpdir=./\" HaplotypeCaller -R %s -I %s.recal.bam -O %s.raw.vcf --dont-use-soft-clipped-bases true" \
    %(java,GATK,ref,args.name,args.name)
subprocess.check_call(cmd,shell=True)
###############################################filter
cmd="%s && %s --java-options \"-Xmx10G -Djava.io.tmpdir=./\" VariantFiltration -R %s -V %s.raw.vcf -cluster 3 -window 35 -filter-name \"FS\" -filter \"FS > 30.0\" -filter-name \"QD\" -filter \"QD < 2.0\" -O %s.filter.vcf" \
    %(java,GATK,ref,args.name,args.name)
subprocess.check_call(cmd,shell=True)
end=time.time()
print("Elapse time is %g seconds" %(end-start))