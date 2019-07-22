import os
import sys
import subprocess
import json
fastp="/software/fastp/fastp"
speedseq="export PATH=/software/speedseq/speedseq/bin:$PATH"
ref="/data/Database/hg19/ucsc.hg19.fasta"
java="/software/java/jdk1.8.0_202/bin/java"
picard="/software/picard/picard.jar"

def run(pe1,pe2,readlength,outdir,prefix):
    out=outdir+"/"+prefix
    cmd='%s --in1 %s --in2 %s -w 10 -U --umi_loc=per_read --umi_len 3 --umi_skip 2 --out1 %s.clean.1.fq --out2 %s.clean.2.fq -l %s -j %s.json -h %s.html'\
        %(fastp,pe1,pe2,out,out,readlength-10,out,out)
    subprocess.check_call(cmd,shell=True)
    json_file = os.path.abspath("%s.json" % (out))
    outfile = open("%s.csv" % (out), "w")
    outfile.write(
        "SampleID\tRaw_reads\tClean_reads\tRaw_bases\tClean_bases\tClean_q20_rate\tClean_q30_rate\tClean_gc_content\n")
    with open("%s" % (json_file), "r") as load_f:
        load_dict = json.load(load_f)
        raw1 = load_dict['summary']['before_filtering']["total_reads"]
        raw2 = load_dict['summary']['before_filtering']['total_bases']
        clean1 = load_dict['summary']['after_filtering']["total_reads"]
        clean2 = load_dict['summary']['after_filtering']['total_bases']
        clean3 = load_dict['summary']['after_filtering']['q20_rate']
        clean4 = load_dict['summary']['after_filtering']['q30_rate']
        clean5 = load_dict['summary']['after_filtering']['gc_content']
    outfile.write(
        "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (prefix, raw1, clean1, raw2, clean2, clean3, clean4, clean5))
    outfile.close()
    subprocess.check_call(
        "cd %s && %s && speedseq align -t 20 -o %s -R \"@RG\\tID:%s\\tSM:%s\\tLB:lib:\\tPL:Illumina\" %s %s.clean.1.fq %s.clean.2.fq"
        % (outdir, speedseq, prefix, prefix, prefix, ref, prefix, prefix), shell=True)
    cmd = "%s -Xmx100G -jar %s MarkDuplicates I=%s.bam O=%s.umi.dup.bam BARCODE_TAG=RX M=%s.marked_dup_metrics.txt REMOVE_DUPLICATES=true" % (java, picard, out, out, out)
    subprocess.check_call(cmd, shell=True)

if __name__=="__main__":
    if len(sys.argv)!=6:
        print("python3 %s pe1.fq(.gz) pe2.fq.(gz) 101 outdir prefix"%(sys.argv[0]))
        print("Email:fanyucai1@126.com")
    else:
        pe1=sys.argv[1]
        pe2=sys.argv[2]
        readlength=sys.argv[3]
        outdir=sys.argv[4]
        prefix=sys.argv[5]
        run(pe1, pe2, readlength, outdir, prefix)