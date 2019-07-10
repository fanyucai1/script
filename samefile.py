import sys
import re
import subprocess
vardict="/data/Project/fanyucai/test/SNV/201911.annovar.tsv"
varscan_indel="/data/Project/fanyucai/test/varscan_SNV/anno/201911.indel.annovar.tsv"
varscan_snp="/data/Project/fanyucai/test/varscan_SNV/anno/201911.snp.annovar.tsv"

outfile=open("varscan_vardict.tsv","w")

dict={}
dict2={}
infile1=open(vardict,"r")
for line in infile1:
    line=line.strip()
    array=line.split("\t")
    if line.startswith("Chr"):
        continue
    if len(array[3])>=2  and len(array[3])==len(array[4]):#MNV
        tmp1=list(array[3])
        tmp2 = list(array[4])
        start=array[1]
        end=array[1]
        for j in range(len(tmp1)):
            tmp=array[0]+"_"+str(start)+"_"+str(end)+"_"+tmp1[j]+"_"+tmp2[j]
            dict[tmp] = line
            print (tmp)
            start = int(array[1])+1
            end = int(array[1])+1
    else:
        tmp = array[0] + "_" + array[1] + "_" + array[2] + "_" + array[3] + "_" + array[4]
        dict[tmp] = line
infile1.close()

infile2=open(varscan_indel,"r")
for line in infile2:
    line = line.strip()
    array = line.split("\t")
    tmp =array[0]+"_"+array[1]+"_"+array[2]+"_"+array[3]+"_"+array[4]
    if tmp in dict:
        outfile.write("%s\n"%(dict[tmp]))
infile2.close()

infile3=open(varscan_snp,"r")
for line in infile3:
    line = line.strip()
    array = line.split("\t")
    tmp =array[0]+"_"+array[1]+"_"+array[2]+"_"+array[3]+"_"+array[4]
    if tmp in dict:
        outfile.write("%s\n"%(dict[tmp]))
infile3.close()
outfile.close()

subprocess.check_call("cat varscan_vardict.tsv|sort -u >varscan_vardict.final.tsv && rm varscan_vardict.tsv",shell=True)