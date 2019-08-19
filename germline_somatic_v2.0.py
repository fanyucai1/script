#Email:fanyucai1@126.com
#2019.6.6

import os
import re
import argparse

cosmic_anno="/data/Database/COSMIC/release_v88/CosmicMutantExport.tsv"
cosmic_vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.vcf"
clinvar_vcf="/data/Database/clinvar/clinvar.vcf"
clinvar_anno="/data/Database/clinvar/variant_summary.txt"
def run(vcf,samplename,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    site={}
    infile=open(vcf,"r")
    outfile1=open("%s.somatic.vcf"%(out),"w")
    outfile2 = open("%s.germline.vcf"%(out), "w")
    outfile3 = open("%s.snp.vcf"%(out), "w")
    outfile4 = open("%s.other.vcf" % (out), "w")
    sample_num,AF_num,AF,=0,0,0
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        if not line.startswith("#"):
            pattern=re.compile(r'chr(\S+)')
            chr=pattern.findall(array[0])
            tmp=chr[0]+"_"+array[1]+"_"+array[3]+"_"+array[4]
            site[tmp]=line

        else:
            for i in range(len(array)):
                if array[i]==samplename:
                    sample_num=i
                if array[i]=="FORMAT":
                    AF_num=i
            outfile1.write("%s\n"%(line))
            outfile2.write("%s\n" % (line))
            outfile3.write("%s\n" % (line))
            outfile4.write("%s\n" % (line))
    infile.close()
    ##################first get info from cosmic###################
    cosmic_id={}
    infile=open(cosmic_vcf,"r")
    for line in infile:
        if not line.startswith("#"):
            line=line.strip()
            array=line.split("\t")
            p1=re.compile(r'SNP')
            p2=re.compile(r'CNT=(\d+)')
            a=p1.findall(array[7])
            b=p2.findall(array[7])
            tmp=array[0]+"_"+array[1]+"_"+array[3]+"_"+array[4]
            if float(b[0]) >= 50 and tmp in site:
                outfile1.write("%s\n" % (site[tmp]))
                del site[tmp]
            elif a!=[] and tmp in site:
                outfile3.write("%s\n" % (site[tmp]))
                del site[tmp]
            else:
                cosmic_id[array[2]] = array[0] + "_" + array[1] + "_" + array[3] + "_" + array[4]
    infile.close()
    infile=open(cosmic_anno,"r")
    id_num=0
    status=0
    num=0
    for line in infile:
        num+=1
        line = line.strip()
        array = line.split("\t")
        if num==1:
            for i in range(len(array)):
                if array[i]=="Mutation ID":
                    id_num=i
                elif array[i]=="Mutation somatic status":
                    status=i
                else:
                    pass
        else:
            if array[id_num] in cosmic_id and cosmic_id[array[id_num]] in site:
                if array[status]=="Confirmed somatic variant":
                    outfile1.write("%s\n"%(site[cosmic_id[array[id_num]]]))
                    del site[cosmic_id[array[id_num]]]
                else:
                    pass
            else:
                pass
    infile.close()
    ##################then get info from clinvar###################
    clinvar_id={}
    infile=open(clinvar_anno,"r")
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        if line.startswith("#"):
            for i in range(len(array)):
                if array[i]=="OriginSimple":
                    status=i
        else:
            clinvar_id[array[0]]=array[status]
    infile.close()
    ###############################################################
    infile=open(clinvar_vcf,"r")
    for line in infile:
        if not line.startswith("#"):
            line=line.strip()
            array=line.split("\t")
            tmp = array[0] + "_" + array[1] + "_" + array[3] + "_" + array[4]
            if tmp in site:
                if array[2] in clinvar_id:
                    if re.search('somatic',clinvar_id[array[2]]):
                        outfile1.write("%s\n" % (site[tmp]))
                        del site[tmp]
                    else:
                        if re.search('germline',clinvar_id[array[2]]):
                            outfile2.write("%s\n" % (site[tmp]))
                            del site[tmp]
    infile.close()
    ###############################################################
    for key in site:
        array=site[key].split("\t")
        info = array[AF_num].split(":")
        for k in range(len(info)):
            if info[k] == "AF" or info[k] == "VF" or info[k] == "VAF":
                AF = k
        info=array[sample_num].split(":")
        if re.search(",",info[AF]):
            outfile4.write("%s\n" % (site[key]))
        elif float(info[AF])>=0.3:
            outfile2.write("%s\n"%(site[key]))
        else:
            print(float(info[AF]))
            outfile1.write("%s\n" % (site[key]))
    outfile1.close()
    outfile2.close()
    outfile3.close()

if __name__=="__main__":
    parser=argparse.ArgumentParser("This scipt will divided vcf into somatic and germline.")
    parser.add_argument("-v","--vcf",help="vcf file",required=True)
    parser.add_argument("-s","--samplename",help="sample name",required=True)
    parser.add_argument("-o","--outdir",help="output directory",required=True)
    parser.add_argument("-p","--prefix",help="prefix of output",required=True)
    args=parser.parse_args()
    run(args.vcf,args.samplename,args.outdir,args.prefix)