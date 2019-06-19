#Email:fanyucai1@126.com
#2019.5.21
#version:1.0
import os
import argparse
import subprocess
import re

snpeff="/software/SnpEff/4.3/snpEff/"
java="/software/java/jdk1.8.0_202/bin/java"
annovar="/software/docker_tumor_base/Resource/Annovar/"
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene',
          'ExonicFunc.refGene',	'AAChange.refGene',	'cytoBand',	'1000g2015aug_all',	'avsnp150',	'snp138',
          'CLNALLELEID','CLNDN','CLNDISDB',	'CLNREVSTAT','CLNSIG','cosmic88_coding','SIFT_score','SIFT_pred',
          'Polyphen2_HDIV_score','Polyphen2_HDIV_pred','esp6500siv2_all','ExAC_ALL','ExAC_EAS','1000g2015aug_eas',
          '1000g2015aug_sas','1000g2015aug_afr','1000g2015aug_amr','1000g2015aug_eur','InterVar_automated','GT','AAChange.1',
          'Ref_Reads',	'Alt_Reads','Var']
def run(dir,samplelist,vaf,outdir):
    #####################################get sample ID
    sample_ID=[]
    infile = open(samplelist, "r")
    for line in infile:
        line=line.strip()
        array=re.split('[\t,]',line)
        sample_ID.append(array[0])
    infile.close()
    ######################################get SNV information
    for key in sample_ID:
        path=dir+"/Logs_Intermediates/Tmb/%s/%s.tmb.tsv"%(key,key)
        vcf=dir+"/Logs_Intermediates/SmallVariantFilter/%s/%s_SmallVariants.genome.vcf"%(key,key)
        if os.path.exists(path):
            infile=open(path,"r")
            outfile=open("%s/%s.snv.tmp.vcf"%(outdir,key),"w")
            outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
            num=0
            name=[]
            dict={}
            for line in infile:
                line=line.strip()
                num+=1
                array=line.split("\t")
                vaf =0
                Depth = 0
                if num==1:
                    for i in range(len(array)):
                        name.append(array[i])
                else:
                    result=0
                    tmp = array[0] + "\t" + array[1] + "\t" + array[2] + "\t" + array[3]
                    for i in range(len(name)):
                        if name[i]=="VAF" and float(array[i])>= vaf:
                            result+=1
                            vaf=array[i]
                        if name[i]=="Depth":
                            Depth=array[i]
                        if name[i]=="CodingVariant" and array[i]=="True":
                            result+=1
                        if name[i]=="Nonsynonymous" and array[i]=="True":
                            result +=1
                        if name[i]=="SomaticStatus" and array[i]=="Somatic":
                            result +=1
                    if result==4:
                        dict[tmp]=1
            infile.close()
            infile=open(vcf,"r")
            for line in infile:
                line=line.strip()
                if not line.startswith("#"):
                    array=line.split("\t")
                    tmp=array[0] + "\t" + array[1] + "\t" + array[3] + "\t" + array[4]
                    if tmp in dict:
                        info=array[-1].split(":")
                        outfile.write("%s\t%s\t.\t%s\t%s\t.\t.\tGT=%s;Alt_Reads=%s;Var=%s\n"%(array[0],array[1],array[3],array[4],info[0],info[2],info[4]))
            outfile.close()
            ############################anno snpeff
            cmd="%s -Xmx40g -jar %s/snpEff.jar -v hg19 -canon -hgvs %s/%s.snv.tmp.vcf >%s/%s.snpeff.vcf" %(java,snpeff,outdir,key,outdir,key)
            subprocess.check_call(cmd,shell=True)
            ############################get knownCanonical transcript
            nm = {}
            file1 = open("%s/%s.snpeff.vcf" % (outdir,key), "r")
            for line in file1:
                if not line.startswith("#"):
                    line = line.strip()
                    p1 = re.compile(r'transcript\|(\S+)\|')
                    a = p1.findall(line)
                    array = line.split("\t")
                    if a != []:
                        b = a[0].split(".")
                        end = int(array[1]) + len(array[3]) - 1
                        nm[array[1]] = b[0]
                        print(b[0])
            file1.close()
            ##########################run annovar
            par = " -protocol refGene,cytoBand,snp138,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,1000g2015aug_eas,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118"
            par += ",1000g2015aug_sas,1000g2015aug_afr,1000g2015aug_amr,1000g2015aug_eur "
            par += " -operation g,r,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f "
            par += " -nastring . -polish "
            subprocess.check_call("cd %s && perl %s/table_annovar.pl %s.snpeff.vcf %s/humandb -buildver hg19 -out %s -remove %s -vcfinput " %(args.outdir,annovar,key,annovar,key,par),shell=True)
            #########################output final result
            infile=open("%s/%s.hg19_multianno.txt"%(outdir,key),"r")
            outfile=open("%s/%s.annovar.tsv"%(outdir,key),"w")
            for i in range(len(out_name)):
                if i == 0:
                    outfile.write("%s" % (out_name[i]))
                else:
                    outfile.write("\t%s" % (out_name[i]))
            outfile.write("\n")
            dict = {}
            for line in infile:
                line = line.strip()
                array = line.split("\t")
                name = []
                p1=re.compile(r'Var=([0-9.]+)')
                p2=re.compile(r'Alt_Reads=([0-9.]+)')
                p3=re.compile(r'GT=(\d/\d)')
                a=p1.findall(line)
                b=p2.findall(line)
                c=p3.findall(line)
                if line.startswith("Chr"):
                    for i in range(len(array)):
                        name.append(array[i])
                        dict[array[i]] = i
                else:
                    ##############################format output knownCanonical transcript
                    tmp = array[dict['AAChange.refGene']].split(",")
                    final_nm = tmp[0]
                    for j in range(len(tmp)):
                        if array[1] in nm and re.search(nm[array[1]],tmp[j]):
                            final_nm = tmp[j]
                    for l in range(len(out_name)):
                        if l == 0:
                            outfile.write("%s" % (array[dict[out_name[l]]]))
                        elif out_name[l]=="Var":
                            tmp_num = float(a[0]) * 100
                            outfile.write("\t%.2f" % (tmp_num))
                        elif out_name[l] == "AAChange.1":
                            outfile.write("\t%s" % (final_nm))
                        elif out_name[l] == "Alt_Reads":
                            outfile.write("\t%s" % (b[0]))
                        elif out_name[l] == "Ref_Reads":
                            outfile.write("\t.")
                        elif out_name[l] == "GT":
                            outfile.write("\t%s"%c[0])
                        else:
                            outfile.write("\t%s" % (array[dict[out_name[l]]]))
                    outfile.write("\n")
            infile.close()
            outfile.close()
            subprocess.check_call("cd %s && rm -rf %s.hg19_multianno.txt %s.hg19_multianno.vcf %s.snpeff.vcf %s.snv.tmp.vcf %s.avinput snpEff_summary.html snpEff_genes.txt "%(args.outdir,key,key,key,key,key),shell=True)

if __name__=="__main__":
    parser = argparse.ArgumentParser("")
    parser.add_argument("-d", "--dir", help="TSO500 analysis directory", required=True)
    parser.add_argument("-s", "--samplelist", required=True)
    parser.add_argument("-v", "--vaf", default=0, type=float)
    parser.add_argument("-o", "--outdir", help="output directory", default=os.getcwd())
    args = parser.parse_args()
    run(args.dir, args.samplelist, args.vaf, args.outdir)