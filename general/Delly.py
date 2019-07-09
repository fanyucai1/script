import os
import argparse
import subprocess
delly="/software/Delly/delly_v0.8.1_linux_x86_64bit"
hg19="/software/Delly/delly_v0.8.1_linux_x86_64bit/delly-master/excludeTemplates/human.hg19.excl.tsv"
ref="/data/Database/hg19/ucsc.hg19.fasta"
bcftools="/software/Bcftools/bcftools-1.4/bcftools"
def run(tumor,normal,prefix,outdir):
    out=outdir+"/"+prefix
    cmd="%s call -x %s -o %s.bcf -g %s %s %s"%(delly,hg19,out,ref,tumor,normal)
    subprocess.check_call(cmd,shell=True)
    cmd='%s view %s.bcf > %s_delly_sv.vcf'%(bcftools,out,out)
    subprocess.check_call(cmd,shell=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser("")
    parser.add_argument("-t","--tumor",help="tumor bam",required=True)
    parser.add_argument("-n","--normal",help="normal bam",required=True)
    parser.add_argument("-p","--prefix",help="output prefix",required=True)
    parser.add_argument("-o","--outdir",help="output directory",required=True)
    args=parser.parse_args()
    run(args.tumor,args.normal,args.prefix,args.outdir)