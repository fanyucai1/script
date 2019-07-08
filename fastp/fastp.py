#Email:fanyucai1@126.com
#2019.1.24

import os
import argparse
import time
import subprocess
import json
fastp="/software/fastp/fastp"
def run(pe1,pe2,prefix,outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    outdir=os.path.abspath(outdir)
    pe1=os.path.abspath(pe1)
    pe2=os.path.abspath(pe2)
    os.chdir(outdir)
    par=" --detect_adapter_for_pe -W 4 -M 15 -l 75 -w 20 -j %s.json -h %s.html " %(prefix,prefix)
    cmd="%s -i %s -I %s -o %s.R1.fq.gz -O %s.R2.fq.gz %s " %(fastp,pe1,pe2,prefix,prefix,par)
    subprocess.check_call(cmd, shell=True)
    json_file= os.path.abspath("%s/%s.json"%(outdir,prefix))
    outfile = open("%s/%s.csv" % (outdir, prefix), "w")
    outfile.write(
        "SampleID\tRaw_reads\tClean_reads\tRaw_bases\tClean_bases\tClean_q20_rate\tClean_q30_rate\tClean_gc_content\n")
    with open("%s" % (json_file), "r") as load_f:
        load_dict = json.load(load_f)
        raw1 = load_dict['summary']['before_filtering']["total_reads"]
        raw2 = load_dict['summary']['before_filtering']['total_bases']
        clean1 = load_dict['summary']['after_filtering']["total_reads"]
        clean2 = load_dict['summary']['after_filtering']['total_bases']
        clean3 = load_dict['summary']['after_filtering']['q20_rate']
        clean4 = load_dict['summary']['after_filtering']['q30_rate']
        clean5 = load_dict['summary']['after_filtering']['gc_content']
    outfile.write(
        "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (args.prefix, raw1, clean1, raw2, clean2, clean3, clean4, clean5))
    outfile.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser("QC using fastp.")
    parser.add_argument("-p1", "--pe1", help="5 reads", required=True)
    parser.add_argument("-p2", "--pe2", help="3 reads", required=True)
    parser.add_argument("-o", "--outdir", help="output directory", default=os.getcwd())
    parser.add_argument("-p", "--prefix", help="prefix of output", default="out.clean")
    args = parser.parse_args()
    run(args.pe1,args.pe2,args.prefix,args.outdir)
