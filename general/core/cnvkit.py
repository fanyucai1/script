#Email:fanyucai1@126.com
#2019.7.11

import subprocess
import argparse
import glob
#http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refFlat.txt.gz
def run(tumor,normal,bed,outdir,anno,access,python3,cnvkit,ref):
    cmd="%s %s batch %s --normal %s --targets %s --fasta %s --output-reference my_reference.cnn --output-dir %s --annotate %s --access %s" %(python3,cnvkit,tumor,normal,bed,ref,outdir,anno,access)
    subprocess.check_call(cmd,shell=True)
    cns=glob.glob("%s/*.cns")
    infile=open(cns[0],"r")
    outfile=open("%s/cnv.final.tsv","w")
    outfile.write("#Chr\tStart\tend\tgene\tlog2\ttype\tCopy\n")
    for line in infile:
        if not line.startswith("chromosome"):
            line=line.strip()
            array=line.split("\t")
            copy = 2 ** float(array[4]) * 2
            if float(array[4])>=0.585:#https://cnvkit.readthedocs.io/en/stable/calling.html
                type="gain"
                tmp = array[0] + "\t" + array[1] + "\t" + array[2] + "\t" + array[3] + "\t" + array[4] + "\t" + type + "\t" + str(copy)
                outfile.write("%s\n" % (tmp))
            if float(array[4]) <=-1:
                type="loss"
                tmp=array[0]+"\t"+array[1]+"\t"+array[2]+"\t"+array[3]+"\t"+array[4]+"\t"+type+"\t"+str(copy)
                outfile.write("%s\n"%(tmp))
    outfile.close()

if __name__=="__main__":
    parser=argparse.ArgumentParser("cnvkit run cnv.")
    parser.add_argument("-tumor",help="tumor bam",required=True)
    parser.add_argument("-normal",help="normal bam",required=True)
    parser.add_argument("-bed",help="bed file",required=True)
    parser.add_argument("-outdir",help="output directory",required=True)
    parser.add_argument("-anno",help="anno file",default="/software/CNVkit/cnvkit-master/data/refFlat.txt")
    parser.add_argument("-access",help="access file",default="/software/CNVkit/cnvkit-master/data/access-5k-mappable.hg19.bed")
    parser.add_argument("-python3",help="python3 bin",default="/software/python3/Python-v3.7.0/bin/python3")
    parser.add_argument("-cnvkit",help="cnvkit bin",default="/software/python3/Python-v3.7.0/bin/cnvkit.py")
    parser.add_argument("-ref",help="reference fasta",default="/data/Database/hg19/ucsc.hg19.fasta")
    args=parser.parse_args()
    run(args.tumor, args.normal, args.bed, args.outdir, args.anno, args.access, args.python3, args.cnvkit, args.ref)