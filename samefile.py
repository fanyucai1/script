import sys

vardict="/data/Project/fanyucai/test/SNV/201911.somatic.filter.annovar.somatic"
varscan_indel="/data/Project/fanyucai/test/varscan_SNV/anno/201911.indel.filter.filter.annovar.somatic"
varscan_snp="/data/Project/fanyucai/test/varscan_SNV/anno/201911.snp.filter.filter.annovar.somatic"

outfile=open("varscan_vardict.tsv","w")

dict={}
infile1=open(vardict,"r")
for line in infile1:
    line=line.strip()
    array=line.split("\t")
    if len(array[3])>=2  and len(array[3])==len(array[4]):#MNV
        tmp1=array[3].split()
        tmp2=array[4].split()
        for j in range(len(tmp1)):
            tmp=array[0]+"_"+array[1]+"_"+array[2]+"_"+tmp1[j]+"_"+tmp2[j]
            dict[tmp] = line
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