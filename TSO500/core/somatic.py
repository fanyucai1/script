#Email:fanyucai1@126.com
#2019.5.21
#version:1.0
import os
import argparse
import subprocess
import re

Canonical_transcript_file="/data/Database/knownCanonical/clinvar_canonical_trans.txt"
annovar="/software/docker_tumor_base/Resource/Annovar/"
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene',
          'ExonicFunc.refGene',	'AAChange.refGene',	'cytoBand',	'1000g2015aug_all',	'avsnp150',	'snp138',
          'CLNALLELEID','CLNDN','CLNDISDB',	'CLNREVSTAT','CLNSIG','cosmic88_coding','SIFT_score','SIFT_pred',
          'Polyphen2_HDIV_score','Polyphen2_HDIV_pred','esp6500siv2_all','ExAC_ALL','ExAC_EAS','1000g2015aug_eas',
          '1000g2015aug_sas','1000g2015aug_afr','1000g2015aug_amr','1000g2015aug_eur','InterVar_automated','GT','AAChange.1',
          'Ref_Reads',	'Alt_Reads','Var']
def run_hgvs(var_site):
    p1=re.search(r'[A-Z]fs\*\d+$',var_site)###匹配移码突变
    p2=re.search(r'del([ACGT]+)ins',var_site)###匹配del和ins
    if p1:
        new=re.sub(r'[A-Z]fs\*\d+$',"",var_site)
        new=new+"fs"
    else:
        new=var_site
    if var_site.endswith("X"):####终止密码子X替换*
        new1= re.sub(r'X$', "*", new)
    else:
        new1=new
    if p2:
        new2=re.sub(p2.group(1),"",new1,count=1)
    else:
        new2 = new1
    return new2
def run(dir,outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    #########################get Canonical transcript info
    transcript = {}
    infile = open(Canonical_transcript_file, "r")
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        transcript[array[0]] = []
        for j in range(len(array)):
            if j != 0:
                tmp = array[j].split(".")
                transcript[array[0]].append(tmp[0])
    infile.close()
    ###############################backlist
    hotspot = open("/data/Database/Cancer_hotspots/hotspot.tsv", "r")
    backlist = {}
    for line in hotspot:
        line = line.strip()
        array = line.split("\t")
        backlist[array[0] + "\t" + array[1] + "\t" + array[2] + "\t" + array[3]] = 1
    hotspot.close()
    ######################################get SNV information
    prefix,path,vcf="","",""
    for(root,dirs,files) in os.walk(dir):
        for file in files:
            tmp=os.path.join(root,file)
            if tmp.endswith(".tmb.tsv"):
                prefix=tmp.split("/")[-2]
                path=tmp
            if tmp.endswith("_SmallVariants.genome.vcf"):
                vcf=tmp
    infile=open(path,"r")
    outfile=open("%s/%s.snv.tmp.vcf"%(outdir,prefix),"w")
    outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    num,name,dict=0,[],{}
    for line in infile:
        line=line.strip()
        num+=1
        array=line.split("\t")
        vaf,Depth =0,0
        if num==1:
            for i in range(len(array)):
                name.append(array[i])
        else:
            result=0
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
            tmp = array[0] + "\t" + array[1] + "\t" + array[2] + "\t" + array[3]
            if result==4 or tmp in backlist:
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
                outfile.write("%s\t%s\t.\t%s\t%s\t.\t.\tGT=%s;AD=%s;Var=%s\n"%(array[0],array[1],array[3],array[4],info[0],info[2],info[4]))
    infile.close()
    outfile.close()
    ##########################run annovar
    par = " -protocol refGene,cytoBand,snp138,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,1000g2015aug_eas,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118"
    par += ",1000g2015aug_sas,1000g2015aug_afr,1000g2015aug_amr,1000g2015aug_eur "
    par += " -operation g,r,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f "
    par += " -nastring . -polish "
    subprocess.check_call("cd %s && perl %s/table_annovar.pl %s/%s.snv.tmp.vcf %s/humandb -buildver hg19 -out %s -remove %s -vcfinput " %(outdir,annovar,outdir,prefix,annovar,prefix,par),shell=True)
    #########################output final result
    infile=open("%s/%s.hg19_multianno.txt"%(outdir,prefix),"r")
    outfile=open("%s/%s.annovar.tsv"%(outdir,prefix),"w")
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
        p2=re.compile(r'AD=([0-9.,]+)')
        p3=re.compile(r'GT=([\d.]/[.\d])')
        a=p1.findall(line)
        b=p2.findall(line)
        c=p3.findall(line)
        if line.startswith("Chr"):
            for i in range(len(array)):
                name.append(array[i])
                dict[array[i]] = i
        else:
            Reads=b[0].split(",")
            ##########################format output knownCanonical transcript
            tmp = array[dict['AAChange.refGene']].split(",")
            final_nm = ""
            if array[6] in transcript:
                for i in transcript[array[6]]:
                    if final_nm == "":
                        for k in tmp:
                            if final_nm == "" and re.search(i, k):
                                final_nm = k
                                continue
                            else:
                                pass
                    else:
                        continue
            if final_nm == "":
                final_nm = tmp[0]
            for l in range(len(out_name)):
                if l == 0:
                    outfile.write("%s" % (array[dict[out_name[l]]]))
                elif out_name[l]=="Var":
                    tmp_num = float(a[0]) * 100
                    outfile.write("\t%.2f" % (tmp_num)+"%")
                elif out_name[l] == "AAChange.1":
                    outfile.write("\t%s" % (run_hgvs(final_nm)))
                elif out_name[l] == "Ref_Reads":
                    outfile.write("\t%s"%(Reads[0]))
                elif out_name[l] == "Alt_Reads":
                    outfile.write("\t%s" % (Reads[1]))
                elif out_name[l] == "GT":
                    outfile.write("\t%s"%c[0])
                else:
                    outfile.write("\t%s" % (array[dict[out_name[l]]]))
            outfile.write("\n")
    infile.close()
    outfile.close()
    subprocess.check_call("cd %s && rm -rf %s.hg19_multianno.txt %s.hg19_multianno.vcf %s.snpeff.vcf %s.snv.tmp.vcf %s.avinput snpEff_summary.html snpEff_genes.txt "%(outdir,prefix,prefix,prefix,prefix,prefix),shell=True)

if __name__=="__main__":
    parser = argparse.ArgumentParser("")
    parser.add_argument("-d", "--dir", help="TSO500 analysis directory", required=True)
    parser.add_argument("-o", "--outdir", help="output directory", default=os.getcwd())
    args = parser.parse_args()
    run(args.dir, args.outdir)