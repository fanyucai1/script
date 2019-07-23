import os
import argparse
import subprocess

fgbio="/software/fgbio/fgbio-0.8.0.jar"
java="/software/java/jdk1.8.0_202/bin/java"
picard="/software/picard/picard.jar"
bwa="/software/bwa/bwa-0.7.17/bwa"
ref="/data/Database/hg19/ucsc.hg19.fasta"
samtools="/software/samtools/samtools-1.9/bin/samtools"
env="export PATH=/software/java/jdk1.8.0_202/bin:/software/R/R-v3.5.2/bin/:"
env+="/software/vardict/1.5.7/VarDictJava-1.5.7/bin:/software/perl/perl-v5.28.1/bin/:$PATH"

parser=argparse.ArgumentParser("")
parser.add_argument("-p1","--pe1",required=True,help="5 reads")
parser.add_argument("-p2","--pe2",required=True,help="3 reads")
parser.add_argument("-o","--outdir",default=os.getcwd(),help="output directory")
parser.add_argument("-r","--read",help="read length",required=True,type=int)
parser.add_argument("-b","--bed",help="bed file",required=True)
parser.add_argument("-v","--vaf",help="VAF",required=True,type=float,choices=[0.002,0.001,0.005],default=0.002)
parser.add_argument("-p","--prefix",required=True,help="prefix of output")
args=parser.parse_args()

if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)

out=args.outdir+"/"+args.prefix
len=args.read-5
##########fastq2bam#####################

cmd="%s -Xmx50g -jar %s FastqToSam F1=%s F2=%s O=%s.unmapped.bam SM=%s RG=%s LB=%s PL=illumina" %(java,picard,args.pe1,args.pe2,out,args.prefix,args.prefix,args.prefix)
subprocess.check_call(cmd,shell=True)

##########ExtractUmisFromBam##############

cmd="%s -Xmx50g -jar %s ExtractUmisFromBam -i %s.unmapped.bam -o %s.umi.unmapped.bam -r 3M2S%sT 3M2S%sT --molecular-index-tags ZA ZB -s RX"\
    %(java,fgbio,out,out,len,len)
subprocess.check_call(cmd,shell=True)

##########align reads######################

cmd="%s -Xmx50g -jar %s SamToFastq I=%s.umi.unmapped.bam INTERLEAVE=true F=%s.fq"%(java,picard,out,out)
subprocess.check_call(cmd,shell=True)
cmd="%s mem -p -t 10 %s %s.fq >%s.mapped.bam"%(bwa,ref,out,out)
subprocess.check_call(cmd,shell=True)
cmd="%s -Xmx50g -jar %s MergeBamAlignment UNMAPPED=%s.umi.unmapped.bam ALIGNED=%s.mapped.bam O=%s.merge.bam R=%s SO=coordinate MAX_GAPS=-1 ORIENTATIONS=FR VALIDATION_STRINGENCY=SILENT " \
    "ALIGNER_PROPER_PAIR_FLAGS=true CREATE_INDEX=true" %(java,picard,out,out,out,ref)
subprocess.check_call(cmd,shell=True)

########GroupReadsByUmi####################

cmd="%s -Xmx50g -jar %s GroupReadsByUmi -i %s.merge.bam  -o %s.group.bam -s Paired -m 20" \
    %(java,fgbio,out,out)
subprocess.check_call(cmd,shell=True)

#######Combine each set of reads to generate consensus reads##########################

cmd="%s -Djava.io.tmpdir=/data/tmp -Xmx50g -jar %s CallDuplexConsensusReads -i %s.group.bam -o %s.consensus.unmapped.bam -1 45 -2 30 -m 30" \
    %(java,fgbio,out,out)
subprocess.check_call(cmd,shell=True)

##############Produce variant calls from consensus reads#################################

cmd="%s -Xmx50g -jar %s SamToFastq I=%s.consensus.unmapped.bam F=%s.consensus.fq INTERLEAVE=true"%(java,picard,out,out)
subprocess.check_call(cmd,shell=True)
cmd="%s mem -p -t 10 %s %s.consensus.fq >%s.realign.bam"%(bwa,ref,out,out)
subprocess.check_call(cmd,shell=True)
cmd="%s -Xmx50g -jar %s MergeBamAlignment UNMAPPED=%s.consensus.unmapped.bam ALIGNED=%s.realign.bam O=%s.consensus.bam R=%s SO=coordinate MAX_GAPS=-1 ORIENTATIONS=FR VALIDATION_STRINGENCY=SILENT " \
    "ALIGNER_PROPER_PAIR_FLAGS=true CREATE_INDEX=true" %(java,picard,out,out,out,ref)
subprocess.check_call(cmd,shell=True)

#######Filter consensus reads#############################################################

cmd="%s -Djava.io.tmpdir=/data/tmp -Xmx50g -jar %s FilterConsensusReads -i %s.consensus.bam -o %s.consensus.filter.bam -r %s -M 6 3 3 " \
    "-N 50 -E 0.05 -e 0.1 -n 0.05"%(java,fgbio,out,out,ref)
subprocess.check_call(cmd,shell=True)

########Clip##############################################################################

cmd="%s -Djava.io.tmpdir=/data/tmp -Xmx50g -jar %s ClipBam -i %s.consensus.filter.bam -o %s.consensus.filter.clipped.bam -r %s -s false --clip-overlapping-reads=true"\
    %(java,fgbio,out,out,ref)
subprocess.check_call(cmd,shell=True)

#############vardict##########################################################################

cmd="%s && VarDict  -U -th 10 -q 20 -Q 20 -G %s -f %s -N %s -b %s.consensus.mapped.clipped.bam -z -c 1 -S 2 -E 3 -g 4 %s | teststrandbias.R | var2vcf_valid.pl -d 50 -N %s -E -f %s >%s.vardict.vcf" \
        %(env,ref,args.vaf,args.prefix,out,args.bed,args.prefix,args.vaf,out)
subprocess.check_call(cmd,shell=True)

