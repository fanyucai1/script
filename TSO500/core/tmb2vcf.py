import os
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
            path=os.path.join(root,file)
            array=path.split("/")
            if path.endswith("tmb.tsv"):
                samplename=array[-2]
                if samplename in sample_ID:
                    infile = open(path, "r")
                    num = 0
                    dict = {}
                    f1, f2, f3, f4= 0, 0, 0, 0
                    for line in infile:
                        line = line.strip()
                        array = line.split("\t")
                        num += 1
                        if num==1:
                            for k in range(len(array)):
                                if array[k] == "GermlineFilterDatabase":
                                    f1 = k
                                if array[k] == "SomaticStatus":
                                    f2 = k
                                if array[k] == "CodingVariant":
                                    f3 = k
                                if array[k] == "GermlineFilterProxi":
                                    f4 = k
                        else:
                            if array[f1] == "False" and array[f2] == "Somatic" and array[f3] == "True" and array[f4] == "False":
                                tmp = array[0] + "\t" + array[1] + "\t" + array[2] + "\t" + array[3]
                                dict[tmp] = 1
                    infile.close()
                    outfile = open("%s/%s.snv.tmp.vcf" % (outdir, samplename), "w")
                    outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
                    for (root, dirs, files) in os.walk(root_dir):
                        for file in files:
                            vcf = os.path.join(root, file)
                            if vcf.endswith("%s_SmallVariants.genome.vcf"%(samplename)):
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