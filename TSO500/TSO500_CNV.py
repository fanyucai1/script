#Email:fanyucai1@126.com

import os
import argparse
import subprocess

cmd="cd /software/TSO500/1.3.1/craft_1.0.0.49/resource/ && /software/dotnet/dotnet /software/TSO500/1.3.1/craft_1.0.0.49/Craft.dll " \
    "-baselineFile craft_baseline.txt -manifestFile craft_manifest.txt  -callGender true -genderThreshold 0.05 " \
    "-genomeFolder /software/TSO500/1.3.1/resources/genomes/hg19_hardPAR -geneThresholdFile CnvGeneThresholds.csv"
parser=argparse.ArgumentParser("Run CNV")
parser.add_argument("-a","--analysis",help="analysis directory",required=True)
args=parser.parse_args()

bam_dir=args.analysis+"/Logs_Intermediates/IndelRealignment/"
out_dir=args.analysis+"/Logs_Intermediates/CNV/"


for(root, dirs, files) in os.walk(bam_dir):
    sh=""
    for i in dirs:
        bam_file=bam_dir+i+"/"+i+".bam"
        sh=cmd+" -bamFiles "+bam_file+" -outputFolder "+out_dir
        subprocess.check_call(sh,shell=True)