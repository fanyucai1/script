import subprocess
import re
import os
import xlsxwriter
import argparse

annovar="/software/docker_tumor_base/Resource/Annovar/"
snpsift="/software/SnpEff/4.3/snpEff/"
java="/software/java/jdk1.8.0_202/bin/java"
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene',
          'ExonicFunc.refGene',	'AAChange.refGene',	'cytoBand',	'1000g2015aug_all',	'avsnp150',	'snp138',
          'CLNALLELEID','CLNDN','CLNDISDB',	'CLNREVSTAT','CLNSIG','cosmic88_coding','SIFT_score','SIFT_pred',
          'Polyphen2_HDIV_score','Polyphen2_HDIV_pred','esp6500siv2_all','ExAC_ALL','ExAC_EAS','1000g2015aug_eas',
          '1000g2015aug_sas','1000g2015aug_afr','1000g2015aug_amr','1000g2015aug_eur','InterVar_automated','GT','AAChange.1',
          'Ref_Reads',	'Alt_Reads','Var']
def run(dir,samplelist,vaf,outdir):
    #####################################defined 2d dict
    def dict2d(dict, key_a, key_b, val):
        if key_a in dict:
            dict[key_a].update({key_b: val})
        else:
            dict.update({key_a: {key_b: val}})
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
        if os.path.exists(path):
            infile=open(path,"r")
            outfile=open("%s/%s.snv.tmp.vcf"%(outdir,key),"w")
            outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
            num=0
            name=[]
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
                    end = int(array[1]) + len(array[2]) - 1
                    tmp = array[0] + "\t" + array[1] + "\t" + str(end) + "\t" + array[2] + "\t" + array[3]
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
                        outfile.write("%s\t%s\t.\t%s\t%s\t.\t.\tAF=%s;Depth=%s\n"%(array[0],array[1],array[2],array[3],vaf,Depth))
                    else:
                        pass
            infile.close()
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
            workbook = xlsxwriter.Workbook('%s/%s.annovar.xlsx' % (outdir,key))
            worksheet = workbook.add_worksheet()
            for i in range(len(out_name)):
                worksheet.write(0, i, "%s" % (out_name[i]))
            dict = {}
            line_num = 0
            for line in infile:
                line = line.strip()
                array = line.split("\t")
                name = []
                p1=re.compile(r'AF=([0-9.]+)')
                p2=re.compile(r'Depth=([0-9.]+)')
                a=p1.findall(line)
                b=p2.findall(line)
                if line.startswith("Chr"):
                    for i in range(len(array)):
                        name.append(array[i])
                        dict[array[i]] = i
                else:
                    line_num+=1
                    string = array[0] + "_" + array[1] + "_" + array[3] + "_" + array[4]
                    ##############################format output knownCanonical transcript
                    tmp = array[dict['AAChange.refGene']].split(",")
                    final_nm = tmp[0]
                    for j in range(len(tmp)):
                        if array[1] in nm and re.search(nm[array[1]],tmp[j]):
                            final_nm = tmp[j]
                    for l in range(len(out_name)):
                        if out_name[l]=="Var":
                            tmp_num = float(a[0]) * 100
                            worksheet.write(line_num, l, "%.2f" % (tmp_num))
                        elif out_name[l] == "Canonical_transcript":
                            worksheet.write(line_num, l, "%s" % (final_nm))
                        elif out_name[l] == "Ref_Reads":
                            worksheet.write(line_num, l, ".")
                        elif out_name[l] == "Alt_Reads":
                            worksheet.write(line_num, l, ".")
                        elif out_name[l] == "GT":
                            worksheet.write(line_num, l, ".")
                        else:
                            worksheet.write(line_num, l, "%s" % (array[dict[out_name[l]]]))
                    outfile.write("\n")
            infile.close()
            workbook.close()
            subprocess.check_call("cd %s && rm -rf %s.hg19_multianno.txt %s.hg19_multianno.vcf %s.snpeff.vcf %s.snv.tmp.vcf %s.avinput snpEff_summary.html snpEff_genes.txt "%(args.outdir,key,key,key,key,key),shell=True)

if __name__=="__main__":
    parser = argparse.ArgumentParser("")
    parser.add_argument("-d", "--dir", help="TSO500 analysis directory", required=True)
    parser.add_argument("-s", "--samplelist", required=True)
    parser.add_argument("-v", "--vaf", required=True, default=0, type=float)
    parser.add_argument("-o", "--outdir", help="output directory", default=os.getcwd())
    args = parser.parse_args()
    run(args.dir, args.samplelist, args.vaf, args.outdir)