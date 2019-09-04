import os
import sys

root_dir="/data/TSO500"
outdir="/data/TSO500/snv_vcf"
def run(root_dir,outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    #####################################get sample ID
    sample_ID=["TS19355NF","TS19067NF","TS19348NF","TS19353NF"]
    ######################################get SNV information
    for (root,dirs,files) in os.walk(root_dir):
        for file in files:
            tmp=os.path.join(root,file)
            array=tmp.split("/")
            samplename=array[-2]
            if samplename in sample_ID:
                dict={}
                outfile = open("%s/%s.snv.tmp.vcf" % (outdir, samplename), "w")
                if tmp.endswith("tmb.tsv"):
                    path=tmp
                    infile = open(path, "r")
                    outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
                    num = 0
                    dict = {}
                    for line in infile:
                        line = line.strip()
                        num += 1
                        array = line.split("\t")
                        tmp = array[0] + "\t" + array[1] + "\t" + array[2] + "\t" + array[3]
                        dict[tmp] = 1
                    infile.close()
                if tmp.endswith("SmallVariants.genome.vcf"):
                    vcf=tmp
                    infile=open(vcf,"r")
                    for line in infile:
                        line=line.strip()
                        if not line.startswith("#"):
                            array=line.split("\t")
                            tmp=array[0] + "\t" + array[1] + "\t" + array[3] + "\t" + array[4]
                            if tmp in dict:
                                info=array[-1].split(":")
                                outfile.write("%s\t%s\t.\t%s\t%s\t.\t.\tGT=%s;AD=%s;Var=%s\n"%(array[0],array[1],array[3],array[4],info[0],info[2],info[4]))
                    infile.close()
                outfile.close()
if __name__=="__main__":
    run(root_dir,outdir)