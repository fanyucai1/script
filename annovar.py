import subprocess
import re
import sys

annovar="/software/docker_tumor_base/Resource/Annovar/"
snpsift="/software/SnpEff/4.3/snpEff/"
java="/software/java/jdk1.8.0_202/bin/java"

database = ['1000g2015aug_all','1000g2015aug_eas', 'ExAC_ALL', 'esp6500siv2_all','ExAC_EAS','genome_AF','genome_AF_eas','exome_AF','exome_AF_eas']
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene','ExonicFunc.refGene','AAChange.refGene','cytoBand',
          'avsnp150','ExAC_ALL','ExAC_EAS','esp6500siv2_all','1000g2015aug_all','1000g2015aug_eas','genome_AF','genome_AF_eas','exome_AF','exome_AF_eas',
          'cosmic88_coding','CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG','SIFT_pred','Polyphen2_HDIV_pred', 'Polyphen2_HVAR_pred','MutationTaster_pred','MutationAssessor_pred','FATHMM_pred',
          'CADD_phred','InterVar_automated']

def anno(vcf,out):
    ##########################run snpeff
    cmd = "%s -Xmx40g -jar %s/snpEff.jar -v hg19 -canon -hgvs %s >%s.snpeff.anno.vcf" % (java, snpsift, vcf, out)
    subprocess.check_call(cmd, shell=True)
    ##########################run annovar
    par=" -protocol refGene,cytoBand,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,1000g2015aug_eas,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118 "
    par+=" -operation g,r,f,f,f,f,f,f,f,f,f,f,f "
    par+=" -nastring . -polish "
    subprocess.check_call("perl %s/table_annovar.pl %s.snpeff.anno.vcf %s/humandb -buildver hg19 -out %s -remove %s -vcfinput " %(annovar,out,annovar,out,par),shell=True)
    subprocess.check_call("rm -rf %s.hg19_multianno.vcf %s.avinput" %(out,out),shell=True)
    ###########################
    infile = open("%s.hg19_multianno.txt" % (out), "r")
    outfile = open("%s.final.txt" % (out), "w")
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
            array[dict['AAChange.refGene']] = final_nm
            for l in range(len(out_name)):
                if l == 0:
                    outfile.write("%s" % (array[dict[out_name[l]]]))
                else:
                    outfile.write("\t%s" % (array[dict[out_name[l]]]))
            outfile.write("\n")
    infile.close()
    outfile.close()
    subprocess.check_call("rm -rf %s.hg19_multianno.txt" %(out),shell=True)
    ###########################################################

if __name__=="__main__":
    if len(sys.argv)!=3:
        print ("\nUsage:\npython annovar.py vcffile outdir/outprefix\n")
        print("Copyright:fanyucai\nVersion:1.0")
        sys.exit(-1)
    vcf=sys.argv[1]
    out=sys.argv[2]
    anno(vcf,out)