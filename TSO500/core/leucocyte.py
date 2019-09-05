import os
import subprocess
root_dir = "/data/TSO500/"
sample_list = "/data/TSO500/samplelist.csv"
outdir = "/data/TSO500/stat/"
annovar="/software/docker_tumor_base/Resource/Annovar/"
def run(root_dir,sample_list,outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    #####################################get sample ID
    infile=open(sample_list,"r")
    sample_ID,num,remark={},0,0
    for line in infile:
        line=line.strip()
        array=line.split(",")
        num+=1
        if num==1:
            for k in range(len(array)):
                if array[k] == "Remarks":
                    remark=k
        else:
            if array[remark] == "N":
                if array[0].startswith("BP") or array[0].startswith("MP"):
                        print(array[0])
                        sample_ID[array[0]]=1
    ######################################get SNV information
    dict,vaf={},{}
    for (root,dirs,files) in os.walk(root_dir):
        for file in files:
            path=os.path.join(root,file)
            array=path.split("/")
            if path.endswith("tmb.tsv"):
                samplename=array[-2]
                if samplename in sample_ID:
                    infile = open(path, "r")
                    num = 0
                    f1, f2, f3, f4,f5= 0, 0, 0, 0,0
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
                                if array[k] == "VAF":
                                    f5=k
                        else:
                            if array[f1] == "False" and array[f2] == "Somatic" and array[f3] == "True" and array[f4] == "False":
                                tmp = array[0] + "\t" + array[1] + "\t" + array[2] + "\t" + array[3]
                                if tmp in dict:
                                    dict[tmp] += 1
                                else:
                                    dict[tmp]=1
                                if tmp in vaf:
                                    vaf[tmp]+=";%s"%(array[f5])
                                else:
                                    vaf[tmp]="%s"%(array[f5])
                    infile.close()
    outfile=open("%s/leucocyte_false_somatic.vcf"%(outdir),"w")
    outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    for key in dict:
        array=key.split("\t")
        outfile.write("%s\t%s\t.\t%s\t%s\t.\t.\tcounts=%s,VAF=%s\n" % (array[0], array[1], array[2], array[3],dict[key],vaf[key]))
    outfile.close()
    par = " -protocol refGene,cytoBand,snp138,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,1000g2015aug_eas,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305"
    par += " -operation g,r,f,f,f,f,f,f,f,f,f,f "
    par += " -nastring . -polish "
    subprocess.check_call("perl %s/table_annovar.pl %s/leucocyte_false_somatic.vcf %s/humandb -buildver hg19 -out %s/leucocyte_false_somatic -remove %s -vcfinput " % (annovar, outdir, annovar, outdir, par), shell=True)
if __name__=="__main__":
    run(root_dir,sample_list,outdir)