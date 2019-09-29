import os
import sys
import subprocess
import re
sub=os.path.abspath(__file__)
dir_name=os.path.dirname(sub)
sys.path.append(dir_name)
import core


pattern=re.compile(r'uid=(\d+)')
cmd=os.popen('id')
tmp=cmd.read().strip()
uid=pattern.findall(tmp)
TSO500_cmd="/software/TSO500/1.3.1/TruSight_Oncology_500.sh --user=%s --remove --resourcesFolder=/software/TSO500/1.3.1/resources "%(uid[0])
genefuse="/software/GeneFuse/genefuse"
ref="/data/Database/hg19/ucsc.hg19.fasta"
fusion="/software/GeneFuse/genes/cancer.hg19.csv"
def run(SampleSheet,samplelist,BCLdir,genelist,outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
        os.mkdir("%s/analysis"%(outdir))
        os.mkdir("%s/CNV" % (outdir))
        os.mkdir("%s/SNV" % (outdir))
        os.mkdir("%s/genefuse" % (outdir))
    subprocess.check_call("cp %s %s"%(SampleSheet,BCLdir),shell=True)
    cmd=" %s --analysisFolder %s/analysis/ --runFolder %s "%(TSO500_cmd,outdir,BCLdir)
    subprocess.check_call(cmd,shell=True)
    core.somatic.run("%s/analysis" % (outdir), samplelist, 0, "%s/SNV" % (outdir), genelist)  ###注释SNV
    core.CNV.run("%s/analysis" % (outdir), samplelist, "%s/CNV" % (outdir), genelist)###注释CNV
    #####################基因融合分析
    if not os.path.exists("%s/gene_fuse" % (outdir)):
        os.mkdir("%s/gene_fuse" % (outdir))
    infile=open(SampleSheet,"r")
    num=0
    for line in infile:
        line=line.strip()
        array=line.split(",")
        if line.startswith("Sample_ID"):
            num=1
        if num==1:
            cmd="cat %s/analysis/Logs_Intermediates/FastqGeneration/%s/%s*R1* >%s/gene_fuse/%s.R1.fq"\
              %(outdir,array[0],array[0],outdir,array[0])
            subprocess.check_call(cmd,shell=True)
            cmd = "cat %s/analysis/Logs_Intermediates/FastqGeneration/%s/%s*R2* >%s/gene_fuse/%s.R2.fq" \
                  % (outdir, array[0], array[0], outdir, array[0])
            subprocess.check_call(cmd, shell=True)
            cmd = "%s --read1 %s/gene_fuse/%s.R1.fq --read2 %s/gene_fuse/%s.R2.fq --ref %s --fusion %s --thread 10 --unique 3 >%s/%s.txt"\
                  % (genefuse, outdir, array[0], outdir, array[0], ref, fusion, outdir,array[0])
            subprocess.check_call(cmd, shell=True)
            core.gene_fuse_stat.run("%s/%s.txt" % (outdir,array[0]), "%s/gene_fuse/" % (outdir),array[0])
    infile.close()
    core.twilio_run.run("TSO500")

if __name__=="__main__":
    if len(sys.argv)!=6:
        print("python3 %s SampleSheet.csv samplelist.csv BCLdir genelist outdir"%(sys.argv[0]))
        print("\n\nEmail:fanyucai1@126.com")
    else:
        SampleSheet, samplelist, BCLdir, genelist, outdir=\
            sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]
        run(SampleSheet, samplelist, BCLdir, genelist, outdir)