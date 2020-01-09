import os
import sys
import subprocess
sub=os.path.abspath(__file__)
dir_name=os.path.dirname(sub)
sys.path.append(dir_name)
import core

docker_name="docker-oncology.dockerhub.illumina.com/zodiac/tst170localapp:1.0.1.0 -fastq"
indexfile="/software/TSO500/1.3.1/resources/sampleSheet/sampleIndexPairsLookup.txt"
def run(fq1,fq2,outdir,prefix,index):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if not os.path.exists("%s/fastq"%(outdir)):
        os.mkdir("%s/fastq"%(outdir))
    cmd = "cp %s %s/fastq/%s_S1_L001_R1_001.fastq.gz" % (fq1, outdir, prefix)
    subprocess.check_call(cmd, shell=True)
    cmd = "cp %s %s/fastq/%s_S1_L001_R2_001.fastq.gz" % (fq2, outdir, prefix)
    subprocess.check_call(cmd, shell=True)
    id, i7_num, i7_seq, i5_num, i5_seq = "", "", "", "", ""
    #############################根据输入的index1的序列或者ID号来匹配正确的index对
    infile = open(indexfile, "r")
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        if array[0] == index or array[1] == index or array[2] == index or array[3] == index or array[4] == index:
            id = array[0]
            i7_seq = array[1]
            i7_num = array[2]
            i5_seq = array[3]
            i5_num = array[4]
    infile.close()
    #####################################生产SampleSheet
    outfile = open("%s/fastq/SampleSheet.csv" % (outdir), "w")
    outfile.write("""
[Header],,,,,,,,								
IEMFileVersion,4,,,,,,,
Investigator Name,User Name,,,,,,,							
Experiment Name,Experiment,,,,,,,							
Workflow,TruSight Tumor 170,,,,,,,							
Application,TruSight Tumor 170,,,,,,,							
Assay,TruSight Tumor 170,,,,,,,								
Description,,,,,,,,							
Chemistry,Default,,,,,,,
[Manifests],,,,,,,,								
PoolRNA,MixRNA_Manifest.txt
[Reads],,,,,,,,							
151,,,,,,,,								
151,,,,,,,,
[Settings],,,,,,,,								
Adapter,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA,,,,,,,								
AdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT,,,,,,,
[Data],,,,,,,,								
Sample_ID,Sample_Name,Sample_Plate,Sample_Well,Index_ID,index,I7_Index_ID,index2,I5_Index_ID,Manifest
""")
    outfile.write("%s,,,,%s,%s,%s,%s,%s,PoolRNA\n"%(prefix,id,i7_seq,i7_num,i5_seq,i5_num))
    outfile.close()
    cmd="docker run -t -v /etc/localtime:/etc/localtime:Z -v %s/fastq/:/data:Z -v /software/TST170/version_1.0/genomes:/genomes -v %s:/analysis %s"\
        %(outdir,outdir,docker_name)
    print(cmd)
    subprocess.check_call(cmd,shell=True)
    core.copy_RNA.copy_RNA(outdir)

if __name__=="__main__":
    if len(sys.argv)!=6:
        print("usage:python3 %s sample.1.fq sample.2.fq outdir prefix indexID\n"%(sys.argv[0]))
        print("Email:fanyucai1@126.com\n")
    else:
        fq1=sys.argv[1]
        fq2=sys.argv[2]
        outdir=sys.argv[3]
        prefix=sys.argv[4]
        index=sys.argv[5]
        run(fq1, fq2, outdir, prefix,index)