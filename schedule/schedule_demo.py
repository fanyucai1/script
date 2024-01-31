import schedule
import time
import re,subprocess
import os
import argparse

script_dir=os.path.dirname(os.path.abspath(__file__))#当前脚本路径

def run_task():
   cmd="dragen -V"

def check_samplesheet(file):
    infile=open(file,'r')
    lane=0
    for line in infile:
        line=line.strip()
        if re.search('^Lane',line):
            lane=1
    infile.close()
    return lane

def bcl2fastq(samplesheet,bcl_dir,out_dir):
    cmd=""
    if check_samplesheet(samplesheet)==1:
        cmd="dragen --bcl-conversion-only true --bcl-input-directory %s --output-directory %s --force --sample-sheet %s"%(bcl_dir,out_dir,samplesheet)
    else:
        cmd="dragen --bcl-conversion-only true --bcl-input-directory %s --output-directory %s --force --sample-sheet %s --no-lane-splitting true"%(bcl_dir,out_dir,samplesheet)
    subprocess.check_call(cmd,shell=True)

def dragen_wes():
    pass

def dragen_wgs():
    pass

schedule.every(10).minutes.do(run_task())

while True:
    schedule.run_pending()
    time.sleep(1)