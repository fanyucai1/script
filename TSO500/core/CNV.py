#Email:fanyucai1@126.com

import os
import argparse
import subprocess
import re

cmd="cd /software/TSO500/1.3.1/craft_1.0.0.49/resource/ && /software/dotnet/dotnet /software/TSO500/1.3.1/craft_1.0.0.49/Craft.dll " \
    "-baselineFile craft_baseline.txt -manifestFile craft_manifest.txt  -callGender true -genderThreshold 0.05 " \
    "-genomeFolder /software/TSO500/1.3.1/resources/genomes/hg19_hardPAR -geneThresholdFile CnvGeneThresholds.csv"
def run(analysis,samplelist,outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    bam_dir=analysis+"/Logs_Intermediates/IndelRealignment/"
    out_dir=analysis+"/Logs_Intermediates/CNV/"
    for(root, dirs, files) in os.walk(bam_dir):
        sh=""
        for i in dirs:
            bam_file=bam_dir+i+"/"+i+".bam"
            sh=cmd+" -bamFiles "+bam_file+" -outputFolder "+out_dir
            subprocess.check_call(sh,shell=True)
    infile=open(samplelist,"r")
    sample=[]
    for line in infile:
        line=line.strip()
        array=re.split('[\t,]',line)
        sample.append(array[0])
    infile.close()
    for id in sample:
        path=analysis+"/Logs_Intermediates/CNV/%s_CopyNumberVariants.vcf" %(id)
        if os.path.exists(path):
            infile=open(path,"r")
            outfile=open("%s/%s.cnv.tsv" %(outdir,id),"w")
            outfile.write("#Chr\tStart\tend\tRef\tType\tGene\n")
            i=0
            print(path)
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
                        outfile.write("%s\n"%(tmp))
            outfile.close()
            if i==0:
                subprocess.check_call("rm -rf %s/%s.cnv.tsv" %(outdir,id),shell=True)
                print("sample %s not find CNV"%(id))
if __name__=="__main__":
    parser = argparse.ArgumentParser("Run CNV")
    parser.add_argument("-a", "--analysis", help="analysis directory", required=True)
    parser.add_argument("-o", "--outdir", help="output directory", default=os.getcwd())
    parser.add_argument("-s", "--samplelist", help="sample list", required=True)
    args = parser.parse_args()
    run(args.analysis,args.samplelist,args.outdir)
