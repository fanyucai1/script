#Email:fanyucai1@126.com
#2019.1.31

import os
import argparse
import json

parser=argparse.ArgumentParser("Parse the fastp json file.")
parser.add_argument("-j","--json",help="serveral json files,split by space",nargs="+",required=True)
parser.add_argument("-n","--name",help="sample name,split by space",nargs="+",required=True)
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",help="prefix of output",default="QC.stat")
args=parser.parse_args()

if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
args.outdir=os.path.abspath(args.outdir)
for i in range(len(args.json)):
    args.json[i]=os.path.abspath(args.json[i])
outfile=open("%s/%s.csv" %(args.outdir,args.prefix),"w")
outfile.write("SampleID\tRaw_reads\tClean_reads\tRaw_bases\tClean_bases\tClean_q20_rate\tClean_q30_rate\tClean_gc_content\n")
for i in range(len(args.json)):
    with open("%s" % (args.json[i]), "r") as load_f:
        load_dict = json.load(load_f)
        raw1 = load_dict['summary']['before_filtering']["total_reads"]
        raw2 = load_dict['summary']['before_filtering']['total_bases']
        clean1 = load_dict['summary']['after_filtering']["total_reads"]
        clean2 = load_dict['summary']['after_filtering']['total_bases']
        clean3 = load_dict['summary']['after_filtering']['q20_rate']
        clean4 = load_dict['summary']['after_filtering']['q30_rate']
        clean5 = load_dict['summary']['after_filtering']['gc_content']
    outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %(args.name[i],raw1,clean1,raw2,clean2,clean3,clean4,clean5))
outfile.close()
