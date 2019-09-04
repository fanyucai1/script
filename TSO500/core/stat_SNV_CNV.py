import os
import re
import argparse
import glob
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

root_dir = "/data/TSO500/"
sample_list = "/data/TSO500/samplelist.csv"
outdir = "/data/TSO500/stat/"
annovar="/software/docker_tumor_base/Resource/Annovar/"

def run_1(root_dir,sample_list,outdir):#step1:将SNV和CNV文件结果汇总
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if not os.path.exists("%s/CNV"%(outdir)):
        os.mkdir("%s/CNV"%(outdir))
    if not os.path.exists("%s/SNV"%(outdir)):
        os.mkdir("%s/SNV"%(outdir))
    subprocess.check_call('rm -rf %s/SNV/*'%(outdir),shell=True)
    subprocess.check_call('rm -rf %s/CNV/*'%(outdir),shell=True)
    dict = {}
    infile = open(sample_list, "r")
    num = 0
    counts = 0
    for line in infile:
        line = line.strip()
        array = line.split(",")
        num += 1
        if num == 1:
            """
            for k in range(len(array)):
                if array[k] == "yes_no_illumina":
                    counts = k
            """
        else:
            """
            if array[counts] == "yes":
                dict[array[0]] = 1
            """
            dict[array[0]] = 1
    infile.close()
    SNV_file=[]
    for (root, dirs, files) in os.walk(root_dir):
        for file in files:
            tmp = os.path.join(root, file)
            array = tmp.split("/")
            ############################################################SNV
            if tmp.endswith("annovar.tsv"):
                sample_name=re.sub(r'.annovar.tsv', "", array[-1])
                if sample_name in dict:
                    SNV_file.append(tmp)
            #############################################################CNV
            if tmp.endswith("CopyNumberVariants.vcf"):
                sample_name = re.sub(r'_CopyNumberVariants.vcf', "", array[-1])
                if sample_name in dict:
                    outfile = open("%s/CNV/%s.cnv.tsv" % (outdir, sample_name), "w")
                    infile = open(tmp, "r")
                    i = 0
                    for line in infile:
                        if not line.startswith("#"):
                            line = line.strip()
                            array = line.split("\t")
                            if array[4] == "<DUP>" or array[4] == "<DEL>":
                                i += 1
                                p1 = re.compile(r'END=(\d+)')
                                p2 = re.compile(r'ANT=(\S+)')
                                a = p1.findall(line)
                                b = p2.findall(line)
                                tmp = array[0] + "\t" + array[1] + "\t" + a[0] + "\t" + array[3] + "\t" + array[4] + "\t" + b[0]
                                outfile.write("%s\n" % (tmp))
                    outfile.close()
                    infile.close()
                    if i == 0:
                        subprocess.check_call("rm -rf %s/CNV/%s.cnv.tsv" % (outdir, sample_name), shell=True)
                        print("sample %s not find CNV" % (sample_name))
    for key in SNV_file:
        subprocess.check_call('cp %s %s/SNV/' % (key, outdir), shell=True)
##############################################################step2:stat TMB and MSI
def run_2(dir,samplelist,outdir):
    #defined 2d dict
    def dict2d(dict, key_a, key_b, val):
        if key_a in dict:
            dict[key_a].update({key_b: val})
        else:
            dict.update({key_a: {key_b: val}})
    #get TMB and MSI information
    dict={}
    sample_ID=[]
    for (root,dirs,files) in os.walk(dir):
        for dir in dirs:
            path=root+"/"+dir+"/analysis/Results/"
            if os.path.exists(path):
                tmbfile=glob.glob("%s/*_BiomarkerReport.txt"%(path))
                for file in tmbfile:
                    basename=os.path.basename(file)
                    sample = basename.split("_BiomarkerReport.txt")
                    sample_ID.append(sample[0])
                    infile = open(file, "r")
                    for line in infile:
                        line = line.strip()
                        array = line.split("\t")
                        if array[0].startswith("Total TMB"):
                            dict2d(dict,sample[0],"Total_TMB",array[1])
                        if array[0].startswith("Nonsynonymous TMB"):
                            dict2d(dict, sample[0], "Nonsynonymous_TMB", array[1])
                        if array[0].startswith("Coding Region Size in Megabases"):
                            dict2d(dict, sample[0], "Coding_Region_Size_in_Megabases", array[1])
                        if array[0].startswith("Number of Passing Eligible Variants"):
                            dict2d(dict, sample[0], "Number_of_Passing_Eligible_Variants", array[1])
                        if array[0].startswith("Number of Passing Eligible Nonsynonymous Variants"):
                            dict2d(dict, sample[0], "Number_of_Passing_Eligible_Nonsynonymous_Variants", array[1])
                        if array[0].startswith("Usable MSI Sites"):
                            dict[sample[0]]["Usable_MSI_Sites"] = array[1]
                            dict2d(dict, sample[0], "Usable_MSI_Sites", array[1])
                        if array[0].startswith("Total Microsatellite Sites Unstable"):
                            dict2d(dict, sample[0], "Total_Microsatellite_Sites_Unstable", array[1])
                        if array[0].startswith("Percent Unstable Sites"):
                            dict2d(dict, sample[0], "Percent_Unstable_Site", array[1])
                    infile.close()
            else:
                continue
    #get information from samplelist
    dict2={}
    infile = open(samplelist, "r")
    num=0
    name=[]
    Batch={}
    rate={}
    for line in infile:
        line=line.strip()
        array=line.split(",")
        num+=1
        if num==1:
            for i in range(len(array)):
                name.append(array[i])
        else:
            for i in range(len(array)):
                if name[i]=="Batch":
                    Batch[array[0]]=array[i]
                if name[i]=="rate":
                    rate[array[0]]=array[i]
                dict2d(dict2,array[0],name[i],array[i])
    infile.close()
    #output result
    outfile=open("%s/TMB_MSI.tsv"%(outdir),"w")
    outfile.write("Batch\trate\tSample_ID\tCancer\tTotal_TMB\tNonsynonymous_TMB\tCoding_Region_Size_in_Megabases\t"
                  "Number_of_Passing_Eligible_Variants"
                  "\tNumber_of_Passing_Eligible_Nonsynonymous_Variants\t"
                  "Usable_MSI_Sites\tTotal_Microsatellite_Sites_Unstable\tPercent_Unstable_Site\n")
    for i in Batch:
        if i not in dict2:
            pass
        else:
            if i in sample_ID:
                outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %(Batch[i],rate[i],i,dict2[i]["Cancer"],dict[i]["Total_TMB"],dict[i]["Nonsynonymous_TMB"],dict[i]["Coding_Region_Size_in_Megabases"],dict[i]["Number_of_Passing_Eligible_Variants"],dict[i]["Number_of_Passing_Eligible_Nonsynonymous_Variants"],dict[i]["Usable_MSI_Sites"],dict[i]["Total_Microsatellite_Sites_Unstable"],dict[i]["Percent_Unstable_Site"]))
    outfile.close()
    #plot
    df = pd.read_csv("%s/TMB_MSI.tsv"%(outdir), sep="\t", header=0)
    x = df['Total_TMB']
    y = df['Cancer']
    plt.figure(figsize=(18, 10))
    sns.boxplot(x, y, data=df)
    plt.savefig('%s/TMB.png'%(outdir), dpi=300)
##############################################################step3:normal false soamtic
def run_3(root_dir,samplelist,outdir):
    dict = {}
    infile = open(samplelist, "r")
    counts = 0
    name = 0
    for line in infile:
        counts += 1
        line = line.strip()
        array = line.split(",")
        if counts == 1:
            for k in range(len(array)):
                if array[k] == "Remarks":
                    name = k
        else:
            if array[name] == "N":
                dict[array[0]] = 0
    infile.close()
    outfile = open("%s/normal_false_somatic.tsv" % (outdir), "w")
    outfile.write("SampleID\tIllumina\tOur\tVAF40\tVAF30\tVAF20\tVAF10\tVAF5\n")
    for (root, dirs, files) in os.walk(root_dir):
        for file in files:
            tmp = os.path.join(root, file)
            sample = tmp.split("/")
            id = sample[-1].split(".")
            if tmp.endswith(".tmb.tsv") and id[0] in dict:
                Illumina, num, VAF5, VAF10, VAF20, VAF30, VAF40 = 0, 0, 0, 0, 0, 0, 0
                row = 0
                infile = open(tmp, "r")
                f1, f2, f3, f4, f5, f6 = 0, 0, 0, 0, 0, 0
                for line in infile:
                    line = line.strip()
                    array = line.split("\t")
                    row += 1
                    if row == 1:
                        for k in range(len(array)):
                            if array[k] == "GermlineFilterDatabase":
                                f1 = k
                            if array[k] == "SomaticStatus":
                                f2 = k
                            if array[k] == "CodingVariant":
                                f3 = k
                            if array[k] == "GermlineFilterProxi":
                                f4 = k
                            if array[k] == "Nonsynonymous":
                                f5 = k
                            if array[k] == "VAF":
                                f6 = k
                    else:
                        tmp=array[0]+"\t"+array[1]+"\t"+array[1]+"\t"+array[2]+"\t"+array[3]
                        if array[f1] == "False" and array[f2] == "Somatic" and array[f3] == "True" and array[f4] == "False":
                            Illumina += 1
                            if array[f5] == "True":
                                num += 1
                                if float(array[f6]) <= 0.05:
                                    VAF5 += 1
                                if float(array[f6]) <= 0.1:
                                    VAF10 += 1
                                if float(array[f6]) <= 0.2:
                                    VAF20 += 1
                                if float(array[f6]) <= 0.3:
                                    VAF30 += 1
                                if float(array[f6]) <= 0.4:
                                    VAF40 += 1
                infile.close()
                outfile.write(
                    "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (id[0], Illumina, num, VAF40, VAF30, VAF20, VAF10, VAF5))
    outfile.close()
####################################################normal tmb convert vcf and anno
def run_4(root_dir,sample_list,outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    #####################################get sample ID
    infile=open(sample_list,"r")
    sample_ID,num,remark,content={},0,0,0
    for line in infile:
        line=line.strip()
        array=line.split(",")
        num+=1
        if num==1:
            for k in range(len(array)):
                if array[k] == "Remarks":
                    remark=k
                if array[k] == "Tumor_content":
                    content=k
        else:
            if array[remark] == "N":
                if array[content]=="." or array[content]=="%0":
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
                    print(samplename)
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
    outfile=open("%s/all_false_somatic.vcf"%(outdir),"w")
    outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    for key in dict:
        array=key.split("\t")
        outfile.write("%s\t%s\t.\t%s\t%s\t.\t.\tcounts=%s,VAF=%s\n" % (array[0], array[1], array[2], array[3],dict[key],vaf[key]))
    outfile.close()
    par = " -protocol refGene,cytoBand,snp138,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305"
    par += " -operation g,r,f,f,f,f,f,f,f,f,f "
    par += " -nastring . -polish "
    subprocess.check_call("perl %s/table_annovar.pl %s/all_false_somatic.vcf %s/humandb -buildver hg19 -out %s/all_false_somatic -remove %s -vcfinput " % (annovar, outdir, annovar, outdir, par), shell=True)


if __name__=="__main__":
    #run_1(root_dir,sample_list,outdir)
    print("done1")
    #run_2(root_dir,sample_list,outdir)
    print("done2")
    #run_3(root_dir,sample_list,outdir)
    print("done3")
    run_4(root_dir,sample_list,outdir)
    print("done4")