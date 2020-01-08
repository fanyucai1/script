#Email:fanyucai1@126.com

import os
import argparse
import subprocess
import re

cmd="cd /software/TSO500/1.3.1/craft_1.0.0.49/resource/ && /software/dotnet/dotnet /software/TSO500/1.3.1/craft_1.0.0.49/Craft.dll " \
    "-baselineFile craft_baseline.txt -manifestFile craft_manifest.txt  -callGender true -genderThreshold 0.05 " \
    "-genomeFolder /software/TSO500/1.3.1/resources/genomes/hg19_hardPAR -geneThresholdFile CnvGeneThresholds.csv"
def run(analysis,outdir,prefix,purity):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    path = analysis + "/Logs_Intermediates/CNV/%s_CopyNumberVariants.vcf" % (prefix)
    bam_dir=analysis+"/Logs_Intermediates/IndelRealignment/"
    out_dir=analysis+"/Logs_Intermediates/CNV/"
    if not os.path.exists(path):
        for(root, dirs, files) in os.walk(bam_dir):
            for file in files:
                tmp=os.path.join(root,file)
                if tmp.endswith(".bam"):
                    sh=cmd+" -bamFiles "+tmp+" -outputFolder "+out_dir
                    subprocess.check_call(sh,shell=True)
    else:
        outfile=open("%s/%s.cnv.tsv" %(outdir,prefix),"w")
        if purity != 0:
            outfile.write("#Chr\tStart\tend\tRef\tType\tGene\tCopy_number\n")
        else:
            outfile.write("#Chr\tStart\tend\tRef\tType\tGene\n")
        i=0
        infile = open(path, "r")
        for line in infile:
            if not line.startswith("#"):
                line = line.strip()
                array = line.split()
                if array[4]=="<DUP>" or array[4]=="<DEL>":
                    i+=1
                    p1=re.compile(r'END=(\d+)')
                    p2=re.compile(r'ANT=(\S+)')
                    a=p1.findall(line)
                    b=p2.findall(line)
                    tmp = array[0] + "\t" + array[1] +"\t"+a[0]+"\t"+array[3]+"\t"+array[4]+"\t"+b[0]
                    print(tmp)
                    if purity != 0:
                        cn = (200 * float(array[-1]) - 2 * (100 - purity)) / purity
                        outfile.write("%s\t%s\n" %(tmp, cn))
                    else:
                        outfile.write("%s\n"%(tmp))
        outfile.close()
        if i==0:
            subprocess.check_call("rm -rf %s/%s.cnv.tsv" %(outdir,prefix),shell=True)
            print("sample %s not find CNV"%(prefix))

if __name__=="__main__":
    parser = argparse.ArgumentParser("Run CNV")
    parser.add_argument("-a", "--analysis", help="analysis directory", required=True)
    parser.add_argument("-o", "--outdir", help="output directory", default=os.getcwd())
    parser.add_argument("-p", "--prefix", help="prefix of output", required=True)
    parser.add_argument("-t", "--purity", help="tumor purity", default=0)
    args = parser.parse_args()
    run(args.analysis,args.outdir,args.prefix,args.purity)
