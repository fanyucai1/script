#!/usr/bin/env python3
# Version 1.1
# Author Xiufeng Yang
# Date: 08/18/2017

# Import Required Libraries 
import argparse
import glob
import subprocess
import os
import configparser
import sys

# Read the command line arguments.
parser = argparse.ArgumentParser(description="Generates pollution test  scripts.")
parser.add_argument("-i", "--inputDirectory", help="Input directory with clean data( FASTQ files.)")
parser.add_argument("-l", "--read_length",help="filtering read that its length less than the define length.(default=150)",default="150")
parser.add_argument("-o", "--outputDirectory",help="Output directory for filtered clean data.(default=./clean_data_length_150)",default="./clean_data_length_150")
parser.add_argument("-c", "--configfile", help="The config file.(default:./config_files/config.ini)", default="./config_files/config.ini")
parser.add_argument("-q", "--qsub_queue_server", help="Submit jobs to queue.(default:all) ", choices=["all", "fat", "big"], default="all")
args=parser.parse_args()

# Process the command line arguments.
inputDirectory = os.path.abspath(args.inputDirectory)
outputDirectory = os.path.abspath(args.outputDirectory)
read_length = args.read_length
configfile = args.configfile
qsubquene = args.qsub_queue_server

# Get the software path and Parameter 
config = configparser.ConfigParser()
config.read(configfile,encoding="utf-8")
qsub_pbs = config.get("software", "qsub_pbs")
perl_path = config.get("software", "perl_path")
thread_number = config.get("parameter", "thread_number")
fastp = config.get("software", "fastp")

# Create output directories, if they do not exist yet.
if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

# Store the list of files with the extensions fastq or fastq.gz
files=glob.glob(inputDirectory+ "/*.fq.gz") + glob.glob(inputDirectory+ "/*.fastq.gz")
files.sort()

# Write the script(s)
os.chdir(outputDirectory)

# Cycle through all the samples, 2 by 2.
for i in range(0, len(files), 2):
    fileR1=os.path.basename(files[i])
    fileR2=os.path.basename(files[i+1])
    filename=fileR1.replace(".R1.fq.gz", "").replace(".R1.fastq.gz", "")
    # Create script file
    scriptName = 'a.filtering_by_length'  + '.sh'
    script = open(scriptName, 'a')
    script.write(fastp  + " -A ")
    script.write("-i " + os.path.join(inputDirectory,fileR1) + " ")
    script.write("-o " + os.path.join(outputDirectory,fileR1) + " ")
    script.write("-I " + os.path.join(inputDirectory,fileR2)  +" ")
    script.write("-O " + os.path.join(outputDirectory,fileR2) + " ")    
    script.write("-l " + read_length +"\n")
    script.close()
# exe these script 
scripts = glob.glob("*.sh")
scripts.sort()
for i in range(0, len(scripts), 1):
   command = perl_path+" "+qsub_pbs + " --queue "+qsubquene  +" "+" --maxproc "+ thread_number +" "+ scripts[i]
   subprocess.call(command,shell=True)
