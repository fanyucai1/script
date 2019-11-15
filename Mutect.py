import os
import sys
import configparser
import argparse
import subprocess

class Myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
    def optionxform(self, optionstr):
        return optionstr
def run(tumor_bam,tumor_name,normal_bam,bed,outdir,configfile,pon):
    config = Myconf()
    config.read(configfile)
    java = config.get('software', 'java')
    gatk4 = config.get('software', 'gatk4.1.3')
    hg19_ref = config.get('database', 'hg19_ref')
    germline_resource=config.get('database','germline-resource')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+tumor_name
    par=" --create-output-bam-index true --min-base-quality-score 20 --native-pair-hmm-threads 8 "
    par+=" -R %s -bamout %s.bam --germline-resource %s "%(hg19_ref,out,germline_resource)
    if pon!="0":
        par+=" -pon %s "%(pon)
    if normal_bam!="0":
        par+=" -I %s "%(normal_bam)
    if bed!="0":
        cmd="%s -Xmx40G -jar %s BedToIntervalList -I %s -O %s.interval_list -SD %s"%(java,gatk4,bed,out,hg19_ref)
        subprocess.check_call(cmd,shell=True)
        par+=" -L %s.interval_list "%(out)
    cmd="%s -Xmx40G -jar %s Mutect2 -I %s -tumor %s %s -O %s.vcf.gz"%(java,gatk4,tumor_bam,tumor_name,par,out)
    subprocess.check_call(cmd,shell=True)
    cmd="%s -Xmx40G -jar %s FilterMutectCalls -R %s -V %s -O %s.filtered.vcf.gz"%(java,gatk4,hg19_ref,out,out)
    subprocess.check_call(cmd,shell=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser("Run GATK Mutect")
    parser.add_argument("--tbam",help="tumor bam file",required=True)
    parser.add_argument("--tname",help="tumor sample name",required=True)
    parser.add_argument("--nbam", help="normal bam file", default="0")
    parser.add_argument("-b","--bed",help="target region bed file",default="0")
    parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
    parser.add_argument("-c","--config",help="config file",required=True)
    parser.add_argument("-v", "--pon", help="panel-of-normals vcf file",default="0")
    args=parser.parse_args()
    run(args.tbam, args.tname,args.nbam, args.bed, args.outdir, args.configfile,args.pon)