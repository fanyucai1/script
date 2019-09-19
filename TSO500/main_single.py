import os
import sys
import subprocess
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from multiprocessing import Process
fastp="/software/fastp/fastp"
TSO500="/software/TSO500/1.3.1/TruSight_Oncology_500.sh"
indexfile="/software/TSO500/1.3.1/resources/sampleSheet"
def shell_run(x):
    subprocess.check_call(x, shell=True)
def run(pe1,pe2,index1,outdir,SampleID):
    ###############################生产输出文件夹目录
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if not os.path.exists("%s/%s"%(outdir,SampleID)):
        os.mkdir("%s/%s"%(outdir, SampleID))
    out=outdir+"/"+SampleID
    id,i7_num,i7_seq,i5_num,i5_seq="","","","",""
    #############################根据输入的index1的序列或者ID号来匹配正确的index对
    infile=open(indexfile,"r")
    for line in infile:
        line=line.strip()
        array=line.split("\t")
        if array[1]==index1 or array[2]==index1:
            id=array[0]
            i7_seq=array[1]
            i7_num=array[2]
            i5_seq=array[3]
            i5_num=array[4]
    infile.close()
    #####################################生产SampleSheet
    outfile = open("SampleSheet.csv", "w")
    outfile.write("""[Header]
    IEMFileVersion,4
    Investigator Name,User Name
    Experiment Name,Experiment
    Date,2019/8/1
    Workflow,From GenerateFASTQ
    Application,NextSeq FASTQ Only
    Assay
    Description
    Chemistry,Default

    [Reads]
    151
    151

    [Settings]
    Adapter,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA
    AdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT
    Read1UMILength,7
    Read2UMILength,7
    Read1StartFromCycle,9
    Read2StartFromCycle,9

    [Data]
    Sample_ID,Sample_Name,Sample_Plate,Sample_Well,Index_ID,index,I7_Index_ID,index2,I5_Index_ID\n""")
    outfile.write("%s,,,,%s,%s,%s,%s,%s\n"%(SampleID,id,i7_seq,i7_num,i5_seq,i5_num))
    ###################################使用fastp在fastq序列中添加UMI序列
    cmd = "%s -i %s -I %s -U --umi_loc per_read --umi_len 7 --umi_skip 1 -o %s.umi.1.fq.gz -O %s.umi.2.fq.gz" \
          % (fastp, pe1, pe2,out, out)
    subprocess.check_call(cmd, shell=True)
    ####################################将index序列反向互补，由于fastp添加的UMI是下划线，这里将下划线转化为+
    my_seq = Seq('%s' % (i5_seq), IUPAC.unambiguous_dna)
    string = {}
    string["a"] = "zcat < %s.umi.1.fq.gz|sed s:+%s:+%s:g|sed s:_:+:g|gzip -c >%s_S1_L001_R1_001.fastq.gz && rm %s.umi.1.fq.gz" \
               % (out, my_seq.reverse_complement().tostring(),i5_seq, out, out)
    string["b"] = "zcat < %s.umi.2.fq.gz|sed s:+%s:+%s:g|sed s:_:+:g|gzip -c >%s_S1_L001_R2_001.fastq.gz && rm %s.umi.2.fq.gz" \
               % (out, my_seq.reverse_complement().tostring(), i5_seq, out, out)
    ####################################多线程运行
    p1 = Process(target=shell_run, args=(string["a"],))
    p2 = Process(target=shell_run, args=(string["b"],))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    #####################################