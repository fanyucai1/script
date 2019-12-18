import os
import sys
import subprocess
sub=os.path.abspath(__file__)
dir_name=os.path.dirname(sub)
sys.path.append(dir_name)
import core

docker_name="docker-oncology.dockerhub.illumina.com/zodiac/tst170localapp:1.0.1.0 -fastq"

def run(fq1,fq2,samplesheet,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if not os.path.exists("%s/fastq"%(outdir)):
        os.mkdir("%s/fastq"%(outdir))
    cmd = "cp %s %s/fastq/%s._S1_L001_R1_001.fastq.gz" % (fq1, outdir, prefix)
    subprocess.check_call(cmd, shell=True)
    cmd = "cp %s %s/fastq/%s._S1_L001_R2_001.fastq.gz" % (fq2, outdir, prefix)
    subprocess.check_call(cmd, shell=True)

    if not os.path.exists("%s/fastq/SampleSheet.csv"%(outdir)):
        cmd="cp %s %s/fastq/SampleSheet.csv"%(samplesheet,outdir)
        subprocess.check_call(cmd,shell=True)
    cmd="docker run -t -v /etc/localtime:/etc/localtime:Z -v %s/fastq/:/data:Z -v /software/TST170/version_1.0/genomes:/genomes -v %s:/analysis %s"\
        %(outdir,outdir,docker_name)
    subprocess.check_call(cmd,shell=True)
    core.twilio_run.run("TST170_%s" % (prefix))

if __name__=="__main__":
    if len(sys.argv)!=6:
        print("usage:python3 %s sample.1.fq sample.2.fq samplesheet.csv outdir prefix\n"%(sys.argv[0]))
        print("Email:fanyucai1@126.com\n")
    else:
        fq1=sys.argv[1]
        fq2=sys.argv[2]
        samplesheet=sys.argv[3]
        outdir=sys.argv[4]
        prefix=sys.argv[5]
        run(fq1, fq2, samplesheet, outdir, prefix)