import subprocess
import re
import sys
import os

annovar="/software/docker_tumor_base/Resource/Annovar/"
snpsift="/software/SnpEff/4.3/snpEff/"
java="/software/java/jdk1.8.0_202/bin/java"
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene',
          'ExonicFunc.refGene',	'AAChange.refGene',	'cytoBand',	'1000g2015aug_all',	'avsnp150',	'snp138',
          'CLNALLELEID','CLNDN','CLNDISDB',	'CLNREVSTAT','CLNSIG','cosmic88_coding','SIFT_score','SIFT_pred',
          'Polyphen2_HDIV_score','Polyphen2_HDIV_pred','esp6500siv2_all','ExAC_ALL','ExAC_EAS','1000g2015aug_eas',
          '1000g2015aug_sas','1000g2015aug_afr','1000g2015aug_amr','1000g2015aug_eur','InterVar_automated','GT','AAChange.1',
          'Ref_Reads',	'Alt_Reads','Var']

def anno(vcf,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    ##########################run snpeff
    cmd = "cd %s && %s -Xmx40g -jar %s/snpEff.jar -v hg19 -canon -hgvs %s >%s.snpeff.anno.vcf" % (outdir,java, snpsift, vcf, prefix)
    subprocess.check_call(cmd, shell=True)
    ##########################run annovar
    par = " -protocol refGene,cytoBand,snp138,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,1000g2015aug_eas,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118"
    par += ",1000g2015aug_sas,1000g2015aug_afr,1000g2015aug_amr,1000g2015aug_eur "
    par += " -operation g,r,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f "
    par += " -nastring . -polish "
    subprocess.check_call("perl %s/table_annovar.pl %s.snpeff.anno.vcf %s/humandb -buildver hg19 -out %s -remove %s -vcfinput " %(annovar,out,annovar,out,par),shell=True)
    subprocess.check_call("rm -rf %s.hg19_multianno.vcf %s.avinput" %(out,out),shell=True)
    ###########################
    infile = open("%s.hg19_multianno.txt" % (out), "r")
    outfile = open("%s.annovar.tsv" % (out), "w")
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
        if line.startswith("Chr"):
            for i in range(len(array)):
                name.append(array[i])
                dict[array[i]] = i
        else:
            p1 = re.compile(r'UMT=([0-9]+)')
            p2 = re.compile(r'VMT=([0-9]+)')
            p3 = re.compile(r'VMF=(\d+\.\d+)')
            p4=re.compile(r'GT=(\d+\/\d+)')
            UMT = p1.findall(line)
            VMT = p2.findall(line)
            VMF = p3.findall(line)
            GT=p4.findall(line)
            ##########################format output knownCanonical transcript
            p = re.compile(r'transcript\|(\S+)\|protein_coding')
            a = p.findall(line)
            tmp = array[dict['AAChange.refGene']].split(",")
            final_nm = tmp[0]
            if a != []:
                b = a[0].split(".")
                for j in range(len(tmp)):
                    if re.search(b[0], tmp[j]):
                        final_nm = tmp[j]
            for l in range(len(out_name)):
                if l == 0:
                    outfile.write("%s" % (array[dict[out_name[l]]]))
                elif out_name[l]=="Var":
                    tmp_num=float(VMF[0])*100
                    outfile.write("\t%.2f" % (tmp_num))
                elif out_name[l]=="Alt_Reads":
                    outfile.write("\t%s" % (VMT[0]))
                elif out_name[l] == "Ref_Reads":
                    outfile.write("\t.")
                elif out_name[l] == "AAChange.1":
                    outfile.write("\t%s" % (final_nm))
                elif out_name[l] == "GT":
                    outfile.write("\t%s" % (GT[0]))
                else:
                    outfile.write("\t%s" % (array[dict[out_name[l]]]))
            outfile.write("\n")
    infile.close()
    outfile.close()
    if os.path.exists("%s.hg19_multianno.txt"%(out)):
        subprocess.check_call("rm -rf %s.hg19_multianno.txt %s/snpEff_genes.txt %s/snpEff_summary.html %s.snpeff.anno.vcf" %(out,outdir,outdir,out),shell=True)
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