import os
import sys

germline_vcf="/data/Database/germline_somatic/db.germline.vcf"
somatic_vcf="/data/Database/germline_somatic/db.somatic.vcf"
snp_vcf="/data/Database/germline_somatic/db.snp.vcf"


def run(vcf,sample,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    ##################################
    germline, somatic, snp = {}, {}, {}
    infile=open(germline_vcf,"r")
    for line in infile:
        if not line.startswith("#"):
            line = line.strip()
            array = line.split("\t")
            tmp = array[0] + "\t" + array[1] + "\t" + array[3] + "\t" + array[4]
            germline[tmp]=1
    infile.close()
    infile = open(somatic_vcf, "r")
    for line in infile:
        if not line.startswith("#"):
            line = line.strip()
            array = line.split("\t")
            tmp = array[0] + "\t" + array[1] + "\t" + array[3] + "\t" + array[4]
            somatic[tmp] = 1
    infile.close()
    infile = open(snp_vcf, "r")
    for line in infile:
        if not line.startswith("#"):
            line = line.strip()
            array = line.split("\t")
            tmp = array[0] + "\t" + array[1] + "\t" + array[3] + "\t" + array[4]
            snp[tmp] = 1
    infile.close()
    #################################
    infile=open(vcf,"r")
    outfile1=open("%s.somatic.vcf","w")
    outfile2 = open("%s.germline.vcf", "w")
    outfile3 = open("%s.snp.vcf", "w")
    sampleID,format=0,0
    for line in infile:
        line=line.strip()
        if line.startswith("#CHROM"):
            array = line.split("\t")
            for k in range(len(array)):
                if array[k]=="FORMAT":
                    format=k
                if array[k] ==sample:
                    sampleID=k
        if line.startswith("#"):
            outfile1.write("%s\n"%(line))
            outfile2.write("%s\n" % (line))
            outfile3.write("%s\n" % (line))
        else:
            array = line.split("\t")
            tmp = array[0] + "\t" + array[1] + "\t" + array[3] + "\t" + array[4]
            if tmp in somatic:
                outfile1.write("%s\n" % (line))
            elif tmp in germline:
                outfile2.write("%s\n" % (line))
            elif tmp in snp:
                outfile3.write("%s\n" % (line))
            else:
                AF_name=array[format].split(":")
                for i in range(len(AF_name)):
                    if AF_name[i]=="AF" or AF_name[i]=="VAF" or AF_name[i]=="VF":
                        AF=array[sampleID].split(":")[i]
                        if float(AF)>=0.95:
                            outfile2.write("%s\n" % (line))
                        elif float(AF)>=0.40 and float(AF)<=0.60:
                            outfile2.write("%s\n" % (line))
                        else:
                            outfile1.write("%s\n" % (line))
    outfile1.close()
    outfile2.close()
    outfile3.close()

if __name__=="__main__":
    if len(sys.argv)!=5:
        print("usage:python3 %s vcffile sampleID outdir prefix\n"%(sys.argv[0]))
        print("Email:fanyucai1@126.com")
    else:
        vcf=sys.argv[1]
        sample=sys.argv[2]
        outdir=sys.argv[3]
        prefix=sys.argv[4]
        run(vcf, sample, outdir, prefix)