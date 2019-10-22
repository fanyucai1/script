import os
import sys
import subprocess
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from multiprocessing import Process
fastp="/software/fastp/fastp"
TSO500="/software/TSO500/1.3.1/TruSight_Oncology_500.sh"
resources="/software/TSO500/1.3.1/resources"
samplesheet="/data/TSO500/SampleSheet.csv"
samplelist="/data/TSO500/samplelist.csv"

def shell_run(x):
    subprocess.check_call(x, shell=True)
def run(pe1,pe2,index2,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if not os.path.exists("%s/%s"%(outdir,prefix)):
        os.mkdir("%s/%s"%(outdir,prefix))
    out=outdir+"/"+prefix+"/"+prefix
    cmd="%s -i %s -I %s -U --umi_loc per_read --umi_len 7 --umi_skip 1 -o %s.umi.1.fq.gz -O %s.umi.2.fq.gz"\
        %(fastp,pe1,pe2,out,out)
    subprocess.check_call(cmd,shell=True)
    my_seq = Seq('%s'%(index2), IUPAC.unambiguous_dna)
    string = {}
    string["a"]="zcat < %s.umi.1.fq.gz|sed s:%s:%s:g|sed s:_:+:g|gzip -c >%s_S1_L001_R1_001.fastq.gz && rm %s.umi.1.fq.gz" \
         %(out,index2,my_seq.reverse_complement().tostring(),out,out)
    string["b"] = "zcat < %s.umi.2.fq.gz|sed s:%s:%s:g|sed s:_:+:g|gzip -c >%s_S1_L001_R2_001.fastq.gz && rm %s.umi.2.fq.gz"\
           %(out,index2,my_seq.reverse_complement().tostring(),out,out)
    p1=Process(target=shell_run,args=(string["a"],))
    p2 = Process(target=shell_run, args=(string["b"],))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__=="__main__":
    if len(sys.argv)!=6:
        print("python3 %s pe1.fastq pe2.fastq index2 outdir prefix"%(sys.argv[0]))
        print("\nEmail:fanyucai1@126.com")
    else:
        pe1=sys.argv[1]
        pe2=sys.argv[2]
        index2=sys.argv[3]
        outdir=sys.argv[4]
        prefix=sys.argv[5]
        run(pe1,pe2,index2,outdir,prefix)