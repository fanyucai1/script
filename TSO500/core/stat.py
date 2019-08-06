#Email:fanyucai1@126.com
#2019.5.21
#version:1.0
import os
import argparse
import glob
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def run(samplelist,outdir="/data/TSO500/",dir="/data/TSO500/"):
    #####################################defined 2d dict
    def dict2d(dict, key_a, key_b, val):
        if key_a in dict:
            dict[key_a].update({key_b: val})
        else:
            dict.update({key_a: {key_b: val}})
    ######################################get TMB and MSI information
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
    ########################################get information from samplelist
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
    #############################################################output result
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
    ###############################################################
    df = pd.read_csv("%s/TMB_MSI.tsv"%(outdir), sep="\t", header=0)
    x = df['Total_TMB']
    y = df['Cancer']
    plt.figure(figsize=(18, 10))
    sns.boxplot(x, y, data=df)
    plt.savefig('%s/TMB.png'%(outdir), dpi=300)
    ################################################################

if __name__=="__main__":
    parser = argparse.ArgumentParser("Output TSO stat result.")
    parser.add_argument("-d", "--dir", help="result directory", default="/data/TSO500/")
    parser.add_argument("-s", "--samplelist", required=True)
    parser.add_argument("-o", "--outdir", help="output directory", default="/data/TSO500/")
    args = parser.parse_args()
    run(args.samplelist,args.outdir,args.dir)

