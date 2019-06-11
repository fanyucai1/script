import sys
import re
import subprocess
import os
samtools="/software/samtools/samtools-1.9/bin/samtools flagstat"
def run(outdir,prefix):
    if not os.path.exists("%s/result/"%(outdir)):
        os.mkdir("%s/result/"%(outdir))
    infile1=open("%s/%s.umi_depths.summary.txt","r")
    outfile2=open("%s/result/%s.qc.tsv","w")
    num=0
    dict={}
    for line in infile1:
        num+=1
        line=line.strip()
        array=line.split("\t")
        if array[1]=="mean read depth":
            dict["read_depth"] = array[0]
        if array[1]=="mean UMI depth":
            dict["UMI_depth"] = array[0]
        if num==1:
            pattern=re.compile(r'(\d+)')
            a=pattern.findall(line)
            dict["Target_bases"]=a[0]
    infile1.close()
    cmd="%s %s/%s.align.bam >%s/%s.align.stat.tsv"%(samtools,outdir,prefix,outdir,prefix)
    subprocess.check_call(cmd,shell=True)
    infile1=open("%s/%s.align.stat.tsv","r")
    num=0
    for line in infile1:
        line=line.strip()
        num+=1
        array=line.split("\t")
        if num==1:
           dict['Total_reads']=array[0]
        elif num==9:
            pattern=re.compile(r'(\d+)')
            a=pattern.findall(array[0])
            dict["mapping_reads"]=a[0]
            pattern = re.compile(r'\((\d+.\d+)%')
            a = pattern.findall(line)
            dict["mapping_Ratio"]=a[0]
        else:
            pass
    infile1.close()
    outfile2.write("Total_reads\tmapping_reads\tmapping_Ratio(%)\tread_depth\tUMI_depth\n")
    outfile2.write("%s\t%s\t%s\t%s\t%s\n"
                   %(dict["Total_reads"],dict["mapping_reads"],dict["mapping_Ratio"],
                     dict["read_depth"],dict["UMI_depth"]))
    outfile2.close()

if __name__=="__main__":
    if len(sys.argv)!=3:
        print("python3 stat_qc.py outdir prefix\n")
        print("Email:fanyucai1@126.com")
        sys.exit(-1)
    outdir=sys.argv[1]
    prefix=sys.argv[2]
    run(outdir,prefix)