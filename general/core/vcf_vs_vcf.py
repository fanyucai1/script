import argparse
import subprocess
def run(vardict,varscan,outdir):
    infile1=open(vardict,"r")#MNV vcf
    infile2=open(varscan,"r")#SNV vcf
    outfile1=open("%s/tmp.vcf"%(outdir),"w")
    outfile2 = open("%s/combine.vcf" % (outdir), "w")
    for line in infile1:
        line = line.strip()
        array = line.split("\t")
        if line.startswith("#CHROM"):
            continue
        if len(array[3]) >= 2 and len(array[3]) == len(array[4]):  # MNV
            tmp1 = list(array[3])
            tmp2 = list(array[4])
            start = array[1]
            end = array[1]
            for j in range(len(tmp1)):
                tmp = array[0] + "_" + str(start) + "_" + str(end) + "_" + tmp1[j] + "_" + tmp2[j]
                dict[tmp] = line
                start = int(array[1]) + 1
                end = int(array[1]) + 1
        else:
            tmp = array[0] + "_" + array[1] + "_" + array[2] + "_" + array[3] + "_" + array[4]
            dict[tmp] = line
    infile1.close()

    for line in infile2:
        line = line.strip()
        array = line.split("\t")
        if line.startswith("#CHROM"):
            continue
        tmp = array[0] + "_" + array[1] + "_" + array[2] + "_" + array[3] + "_" + array[4]
        if tmp in dict:
            outfile1.write("%s\n" % (dict[tmp]))
        else:
            outfile2.write("%s\n"%(line))
    infile2.close()
    outfile1.close()
    outfile2.close()
    subprocess.check_call("cd %s && cat tmp.vcf |sort -u >ovarlap.vcf && rm tmp.vcf" %(outdir),shell=True)
    subprocess.check_call("cd %s && cat ovarlap.vcf >>combine.vcf"%(outdir),shell=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser("vcf1(MNV) and vcf2(MNV) combine and overlap")
    parser.add_argument("-v1","--vcf1",help="vcf file(MNV)",required=True)
    parser.add_argument("-v2", "--vcf2", help="vcf file(MNV)", required=True)
    parser.add_argument("-o","--outdir",help="output directory",required=True)
    args=parser.parse_args()
    run(args.vcf1,args.vcf2,args.outdir)