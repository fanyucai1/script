import sys

vardict="/data/Project/fanyucai/test/SNV/201911.somatic.filter.annovar.somatic"
varscan_indel="/data/Project/fanyucai/test/varscan_SNV/anno/201911.indel.filter.filter.annovar.somatic"
varscan_snp="/data/Project/fanyucai/test/varscan_SNV/anno/201911.snp.filter.filter.annovar.somatic"

outfile=open("varscan_vardict.tsv","w")

dict={}
infile1=open(vardict,"r")
for line in infile1:
    line=line.strip()
    dict[line]=1
infile1.close()

infile2=open(varscan_indel,"r")
for line in infile2:
    line = line.strip()
    if line in dict:
        outfile.write("%s\n"%(line))
infile2.close()

infile3=open(varscan_snp,"r")
for line in infile3:
    line = line.strip()
    if line in dict:
        outfile.write("%s\n"%(line))
infile3.close()

outfile.close()