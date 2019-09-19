import os
import sys
import subprocess
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from multiprocessing import Process
sub=os.path.abspath(__file__)
dir_name=os.path.dirname(sub)
sys.path.append(dir_name)
import core
import argparse
import re
pattern=re.compile(r'uid=(\d+)')
cmd=os.popen('id')
tmp=cmd.read().strip()
uid=pattern.findall(tmp)
TSO500_cmd="/software/TSO500/1.3.1/TruSight_Oncology_500.sh --user=%s --remove --resourcesFolder=/software/TSO500/1.3.1/resources "%(uid[0])
fastp="/software/fastp/fastp"
indexfile="/software/TSO500/1.3.1/resources/sampleSheet"
genefuse="/software/GeneFuse/genefuse"
ref="/data/Database/hg19/ucsc.hg19.fasta"
fusion="/software/GeneFuse/genes/cancer.hg19.csv"
def shell_run(x):
    subprocess.check_call(x, shell=True)
def run(pe1,pe2,index,genelist,outdir,SampleID,samplelist=""):
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
        if array[0]==index or array[1]==index or array[2]==index or array[3]==index or array[4]==index:
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
    ####################################如果samplelist为空生成临时的samplelist
    if samplelist=="1":
        samplelist=open("%s/sample.list","w")
        samplelist.write("Sample_ID,rate,UP,Original_ID,Batch,Time,Cancer,Years,Library_type,Hospital,Remarks,DNA_RNA,Tumor_content,yes_no_illumina,Integrity Score,Pairs\n")
        samplelist.write("%s\n"%(SampleID))
    ####################################运行docker程序
    if not os.path.exists("%s/analysis"%(outdir)):
        os.mkdir("%s/analysis"%(outdir))
        subprocess.check_call("%s --analysisFolder %s/analysis/ --fastqFolder %s"%(TSO500_cmd,outdir,outdir),shell=True)
        core.somatic("%s/analysis" % (outdir), samplelist, 0, "%s/SNV" % (outdir), genelist)###注释SNV
        core.CNV("%s/analysis" % (outdir),samplelist,"%s/CNV"%(outdir))####注释CNV
        #####################基因融合分析
        if not os.path.exists("%s/gene_fuse"%(outdir)):
            os.mkdir("%s/gene_fuse"%(outdir))
            cmd = "%s --read1 %s_S1_L001_R1_001.fastq.gz --read2 %s_S1_L001_R2_001.fastq.gz --ref %s --html %s.html --json %s.json --fusion %s --thread 10 --unique 3 >%s.txt" \
                   % (genefuse, out, out, ref,out,out, fusion, out)
            subprocess.check_call(cmd,shell=True)
            core.gene_fuse_stat("%s.txt"%(out),outdir,SampleID)
    else:
        print("Analysis directory!!!!!!!!")

if __name__=="__main__":
    parser=argparse.ArgumentParser("")
    parser.add_argument("-p1","--pe1",help="5 read fastq(.gz) ",required=True)
    parser.add_argument("-p2","--pe2",help="3 read fastq(.gz)",required=True)
    parser.add_argument("-o","--outdir",help="output directory",required=True)
    parser.add_argument("-s","--sample",help="sample name",required=True)
    parser.add_argument("-g","--genelist",help="sub gene list",required=True)
    parser.add_argument("-i","--index",help="index seq or indexID",required=True)
    parser.add_argument("--l","--samplelist",help="sample list",default="1")
    args=parser.parse_args()
    run(args.pe1, args.pe2, args.index, args.genelist, args.outdir, args.sample, args.samplelist)