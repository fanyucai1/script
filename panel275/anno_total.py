#Email:fanyucai1@126.com
#2019.3.26-2019.4.11
import os
import subprocess
import argparse
import re

annovar="/software/docker_tumor_base/Resource/Annovar/"
snpsift="/software/SnpEff/4.3/snpEff/"
java="/software/java/jdk1.8.0_202/bin/java"
cosmic_vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.hg19.vcf"

database = ['1000g2015aug_all','1000g2015aug_eas', 'ExAC_ALL', 'esp6500siv2_all','ExAC_EAS','genome_AF','genome_AF_eas','exome_AF','exome_AF_eas']
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene','ExonicFunc.refGene','AAChange.refGene','cytoBand',
          'avsnp150','ExAC_ALL','ExAC_EAS','esp6500siv2_all','1000g2015aug_all','1000g2015aug_eas','genome_AF','genome_AF_eas','exome_AF','exome_AF_eas',
          'cosmic88_coding','CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG','SIFT_pred','Polyphen2_HDIV_pred', 'Polyphen2_HVAR_pred','MutationTaster_pred','MutationAssessor_pred','FATHMM_pred',
          'CADD_phred','InterVar_automated']
score=['SIFT_pred','Polyphen2_HDIV_pred', 'Polyphen2_HVAR_pred','MutationTaster_pred','MutationAssessor_pred','FATHMM_pred','CADD_phred']
"""
####################
Cheng D T, Mitchell T N, Zehir A, et al. Memorial Sloan Kettering-Integrated Mutation Profiling of Actionable Cancer Targets (MSK-IMPACT): a hybridization capture-based next-generation sequencing clinical assay for solid tumor molecular oncology[J]. The Journal of molecular diagnostics, 2015, 17(3): 251-264.
####################
"""
parser=argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                               description="Run annovar and filter vcf as followed:\n"
                                           "1:Depth>=50\n"
                                           "2:if MAF>0.01,but CNT>50 in COSMIC will retain\n" 
                                           "3:dicard synonymous SNV,intronic,intergenic\n"    
                                           "4:dicard common snp from:dbsnp,1000Genomes,EXAC,ESP,genomAD\n"
                                )
parser.add_argument("-v","--vcf",help="vcf file",type=str,required=True)
parser.add_argument("-m","--maf",type=int,help="default:0.01",default=0.01)
parser.add_argument("-o","--outdir",help="output directoty",default=os.getcwd())
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
args=parser.parse_args()

if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
args.outdir = os.path.abspath(args.outdir)
args.vcf=os.path.abspath(args.vcf)
os.chdir(args.outdir)
out=args.outdir
out+="/"
out+=args.prefix
##########################anno snpeff
cmd="%s -Xmx40g -jar %s/snpEff.jar -v hg19 -canon -hgvs %s >%s.snpeff.anno.vcf" %(java,snpsift,args.vcf,out)
subprocess.check_call(cmd,shell=True)
##########################run annovar
par=" -protocol refGene,cytoBand,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,1000g2015aug_eas,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118 "
par+=" -operation g,r,f,f,f,f,f,f,f,f,f,f,f "
par+=" -nastring . -polish "
subprocess.check_call("cd %s && perl %s/table_annovar.pl %s.snpeff.anno.vcf %s/humandb -buildver hg19 -out %s -remove %s -vcfinput " %(args.outdir,annovar,out,annovar,args.prefix,par),shell=True)
subprocess.check_call("rm -rf %s.hg19_multianno.vcf %s.avinput" %(out,out),shell=True)
###########################################################read cosmic vcf
cnt={}
file1=open(cosmic_vcf,"r")
for line in file1:
    if not line.startswith("#"):
        line=line.strip()
        array=line.split()
        pattern=re.compile(r'CNT=(\d+)')
        a=pattern.findall(line)
        cnt[array[2]]=int(a[0])
file1.close()
#######################################################
infile=open("%s.hg19_multianno.txt" %(out),"r")
outfile=open("%s.annovar.filter.txt" %(out),"w")
for i in range(len(out_name)):
    if i == 0:
        outfile.write("%s" % (out_name[i]))
    else:
        outfile.write("\t%s" % (out_name[i]))
outfile.write("\tUMT\tVMT\tVMF(%)\n")
dict={}
for line in infile:
    line=line.strip()
    array=line.split("\t")
    name=[]
    if line.startswith("Chr"):
        for i in range(len(array)):
            name.append(array[i])
            dict[array[i]] = i
    else:
        p1 = re.compile(r'UMT=([0-9.]+)')
        p2 = re.compile(r'VMT=([0-9.]+)')
        p3=re.compile(r'VMF=([0-9.]+)')
        a = p1.findall(line)
        b = p2.findall(line)
        e=p3.findall(line)
        ##########################format output knownCanonical transcript
        p = re.compile(r'transcript\|(\S+)\|protein_coding')
        c = p.findall(line)
        tmp = array[dict['AAChange.refGene']].split(",")
        final_nm = tmp[0]
        if c!=[]:
            d=c[0].split(".")
            for j in range(len(tmp)):
                if re.search(d[0], tmp[j]):
                    final_nm = tmp[j]
        array[dict['AAChange.refGene']] = final_nm
        string = array[0] + "_" + array[1] + "_" + array[3] + "_" + array[4]
        ################################
        if array[8]=="synonymous SNV" or array[5]=="intronic" or array[5]=="intergenic" or array[5].startswith("UTR"):
            continue
        ####################################frequence
        freq=0
        freq_counts=0
        counts=0
        result = ""
        for i in database:
            if array[dict[i]]== ".":
                pass
            elif array[dict[i]] != "." and float(array[dict[i]])<=args.maf:
                freq += 1
            else:
                freq_counts+=1
        if freq_counts<3:#not common snp
            if array[dict['CLNSIG']].startswith("Pathogenic") or array[dict['CLNSIG']].startswith("Likely_pathogenic") or array[dict['CLNSIG']].startswith("drug_response"):
                result="true"
            elif array[dict['InterVar_automated']].startswith("Pathogenic") or array[dict['InterVar_automated']].startswith("Likely pathogenic"):
                result = "true"
            elif freq >0:#at least 1<MAF
                result = "true"
            elif array[dict['cosmic88_coding']].startswith("ID="):
                pattern = re.compile(r'ID=(\S+);')
                a = pattern.findall(array[dict['cosmic88_coding']])
                cosmic = a[0].split(",")
                for i in cosmic:
                    counts += int(cnt[i])
                if counts > 50:
                    result = "true"
            else:
                pass
        if result=="true":
            for l in range(len(out_name)):
                if l==0:
                    outfile.write("%s" % (array[dict[out_name[l]]]))
                else:
                    outfile.write("\t%s" % (array[dict[out_name[l]]]))
            outfile.write("\t%s\t%s\t%s\n" % (a[0], b[0],float(e[0])*100))
infile.close()
outfile.close()