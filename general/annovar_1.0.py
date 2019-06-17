import subprocess
import re
import sys
import os
import xlsxwriter

annovar="/software/docker_tumor_base/Resource/Annovar/"
snpsift="/software/SnpEff/4.3/snpEff/"
java="/software/java/jdk1.8.0_202/bin/java"

database = ['1000g2015aug_all','1000g2015aug_eas', 'ExAC_ALL', 'esp6500siv2_all','ExAC_EAS','genome_AF','genome_AF_eas','exome_AF','exome_AF_eas']
#out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene','ExonicFunc.refGene','AAChange.refGene','cytoBand',
#          'avsnp150','snp138','ExAC_ALL','ExAC_EAS','esp6500siv2_all','1000g2015aug_all','1000g2015aug_eas','genome_AF','genome_AF_eas','exome_AF','exome_AF_eas',
#          'cosmic88_coding','CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG','InterVar_automated','Canonical_transcript','Total_Depth','Alt_Depth','VAF','GT','SIFT_pred','Polyphen2_HDIV_pred', 'Polyphen2_HVAR_pred','MutationTaster_pred','MutationAssessor_pred','FATHMM_pred','CADD_phred']
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene',
          'ExonicFunc.refGene',	'AAChange.refGene',	'cytoBand',	'1000g2015aug_all',	'avsnp150',	'snp138',
          'CLNALLELEID','CLNDN','CLNDISDB',	'CLNREVSTAT','CLNSIG','cosmic88_coding','SIFT_score','SIFT_pred'
          'Polyphen2_HDIV_score','Polyphen2_HDIV_pred','esp6500siv2_all','ExAC_ALL','ExAC_EAS','1000g2015aug_eas',
          '1000g2015aug_sas','1000g2015aug_afr','1000g2015aug_amr','1000g2015aug_eur','InterVar_automated','GT','AAChange.1',
          'Ref_Reads',	'Alt_Reads','Var']
def anno(vcf,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    ##########################run snpeff
    cmd = "%s -Xmx40g -jar %s/snpEff.jar -v hg19 -canon -hgvs %s >%s.snpeff.anno.vcf" % (java, snpsift, vcf, out)
    subprocess.check_call(cmd, shell=True)
    ##########################run annovar
    par=" -protocol refGene,cytoBand,snp138,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,1000g2015aug_eas,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118"
    par+=",1000g2015aug_sas,1000g2015aug_afr,1000g2015aug_amr,1000g2015aug_eur "
    par+=" -operation g,r,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f "
    par+=" -nastring . -polish "
    subprocess.check_call("perl %s/table_annovar.pl %s.snpeff.anno.vcf %s/humandb -buildver hg19 -out %s -remove %s -vcfinput " %(annovar,out,annovar,out,par),shell=True)
    subprocess.check_call("rm -rf %s.hg19_multianno.vcf %s.avinput" %(out,out),shell=True)
    ###########################
    infile = open("%s.hg19_multianno.txt" % (out), "r")
    workbook = xlsxwriter.Workbook('%s.annovar.xlsx'%(out))
    worksheet = workbook.add_worksheet()
    for i in range(len(out_name)):
        worksheet.write(0, i, "%s" % (out_name[i]))
    dict = {}
    line_num=0
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        name = []
        if line.startswith("Chr"):
            for i in range(len(array)):
                name.append(array[i])
                dict[array[i]] = i
        else:
            line_num+=1
            ##########################format output knownCanonical transcript
            p = re.compile(r'transcript\|(\S+)\|protein_coding')
            a = p.findall(line)
            tmp = array[dict['AAChange.refGene']].split(",")
            Canonical_transcript = tmp[0]
            if a != []:
                b = a[0].split(".")
                for j in range(len(tmp)):
                    if re.search(b[0], tmp[j]):
                        Canonical_transcript = tmp[j]
            for l in range(len(out_name)):
                if out_name[l]=="Var" or out_name[l]=="Ref_Reads" or out_name[l]=="Alt_Reads" or out_name[l]=="GT":
                    worksheet.write(line_num, l, ".")
                elif out_name[1]=="AAChange.1":
                    worksheet.write(line_num, l, "%s"%(Canonical_transcript))
                else:
                    worksheet.write(line_num, l, "%s" % (array[dict[out_name[l]]]))
    infile.close()
    workbook.close()
    subprocess.check_call("rm -rf %s.hg19_multianno.txt %s/snpEff_summary.html %s/snpEff_genes.txt %s.snpeff.anno.vcf" %(out,outdir,outdir,out),shell=True)
    ###########################################################

if __name__=="__main__":
    if len(sys.argv)!=4:
        print ("\nUsage:\npython annovar.py vcffile outdir outprefix\n")
        print("Copyright:fanyucai\nVersion:1.0")
        sys.exit(-1)
    vcf=sys.argv[1]
    outdir=sys.argv[2]
    prefix=sys.argv[3]
    anno(vcf,outdir,prefix)
