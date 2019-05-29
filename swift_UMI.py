#Email:fanyucai1@126.com
#2019.3.1

import os
import argparse
import subprocess

fgbio="/software/fgbio/fgbio-0.8.0.jar"
java="/software/java/jdk1.8.0_202/bin/java"
picard="/software/picard/picard.jar"
bwa="/software/bwa/bwa-0.7.17/bwa"
ref="/data/Database/hg19/ucsc.hg19.fasta"
samtools="/software/samtools/samtools-1.9/bin/samtools"

"""
MacConaill L E, Burns R T, Nag A, et al. Unique, dual-indexed sequencing adapters with UMIs effectively eliminate index cross-talk and significantly improve sensitivity of massively parallel sequencing[J]. BMC genomics, 2018, 19(1): 30.
https://sfvideo.blob.core.windows.net/sitefinity/docs/default-source/user-guide-manual/analysis-guideline-variant-calling-data-with-umis.pdf?sfvrsn=d0aa3207_24
"""
parser=argparse.ArgumentParser("")
parser.add_argument("-p1","--pe1",required=True,help="5 reads")
parser.add_argument("-p2","--pe2",required=True,help="3 reads")
parser.add_argument("-t","--thread",type=int,default=20,help="Number of threads to use[20]")
parser.add_argument("-f","--fastq",required=True,help="fastq file only contains umi")
parser.add_argument("-o","--outdir",default=os.getcwd(),help="output directory")
parser.add_argument("-p","--prefix",required=True,help="prefix of output")
args=parser.parse_args()

if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
args.fastq=os.path.abspath(args.fastq)

out=args.outdir
out+=args.prefix
cmd="%s mem -t %s -R \'@RG\\tID:%s\\tSM:%s\\tLB:lib:\\tPL:Illumina\' %s %s %s |" %(bwa,args.thread,args.prefix,args.prefix,ref,args.pe1,args.pe2)
cmd+="%s view -@ %s -o %s.bam" %(samtools,args.thread,out)
subprocess.check_call(cmd,shell=True)
cmd="%s sort -@ %s %s.bam -o %s.sort.bam" %(samtools,args.thread,out,out)
subprocess.check_call(cmd,shell=True)
cmd="%s index %s.sort.bam" %(samtools,out)
subprocess.check_call(cmd,shell=True)

if os.path.exists("%s.sort.bam" %(out)):
    subprocess.check_call("rm -rf %s.bam*" %(out),shell=True)

cmd="%s -Xmx100G -jar %s AnnotateBamWithUmis -i %s.sort.bam -f %s -o %s.umi.bam" %(java,fgbio,out,args.fastq,out)
subprocess.check_call(cmd,shell=True)

cmd="%s -Xmx100G -jar %s MarkDuplicates I=%s.umi.bam O=%s.umi.dup.bam BARCODE_TAG=RX M=%s.marked_dup_metrics.txt" %(java,picard,out,out,out)
subprocess.check_call(cmd,shell=True)

cmd="%s -Xmx100G -jar %s RevertSam I=%s.umi.dup.bam O=%s.sanitised.bam SANITIZE=true REMOVE_DUPLICATE_INFORMATION=false REMOVE_ALIGNMENT_INFORMATION=false" \
    %(java,picard,out,out)
subprocess.check_call(cmd,shell=True)

#Fgbio SetMateInformation
cmd="%s -Xmx100G -jar %s SetMateInformation -i %s.sanitised.bam -o %s.fix.bam" %(java,fgbio,out,out)
subprocess.check_call(cmd,shell=True)

#Fgbio GroupReadsByUmi
cmd="%s -Xmx100G -jar %s GroupReadsByUmi -i %s.fix.bam -o %s.group.bam -s adjacency -m 20" \
    %(java,fgbio,out,out)
subprocess.check_call(cmd,shell=True)

#Fgbio CallMolecularConsensusReads
cmd="%s -Xmx50G -jar %s CallMolecularConsensusReads -i %s.group.bam -o %s.consensus.unmap.bam --min-reads 1 --error-rate-post-umi 30" \
    %(java,fgbio,out,out)
subprocess.check_call(cmd,shell=True)

#Filter consensus reads
cmd="%s -Xmx50G -jar %s FilterConsensusReads -i %s.consensus.unmap.bam -o %s.consensus.filtered.unmap.bam -r %s --reverse-per-base-tags=true --min-reads=3 -E 0.05 -N 40 -e 0.1 -n 0.1" \
    %(java,fgbio,out,out,ref)
subprocess.check_call(cmd,shell=True)

#BamToBfq
cmd="%s -Xmx200G -jar %s SamToFastq I=%s.consensus.filtered.unmap.bam FASTQ=%s.1.fq SECOND_END_FASTQ=%s.2.fq" \
    %(java,picard,out,out,out)
subprocess.check_call(cmd,shell=True)
