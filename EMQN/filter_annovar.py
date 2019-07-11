
import re
import sys
import os
database = ['1000g2015aug_all','1000g2015aug_eas', 'ExAC_ALL', 'esp6500siv2_all','ExAC_EAS']
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene',
          'ExonicFunc.refGene',	'AAChange.refGene',	'cytoBand',	'1000g2015aug_all',	'avsnp150',	'snp138',
          'CLNALLELEID','CLNDN','CLNDISDB',	'CLNREVSTAT','CLNSIG','cosmic88_coding','SIFT_score','SIFT_pred',
          'Polyphen2_HDIV_score','Polyphen2_HDIV_pred','esp6500siv2_all','ExAC_ALL','ExAC_EAS','1000g2015aug_eas',
          '1000g2015aug_sas','1000g2015aug_afr','1000g2015aug_amr','1000g2015aug_eur','InterVar_automated','GT','AAChange.1',
          'Ref_Reads',	'Alt_Reads','Var']
cosmic_vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.hg19.vcf"
maf=0.01
def run(maf,annovar,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    ###########################################read cosmic
    cnt={}
    file1 = open(cosmic_vcf, "r")
    for line in file1:
        if not line.startswith("#"):
            line = line.strip()
            array = line.split()
            pattern = re.compile(r'CNT=(\d+)')
            a = pattern.findall(line)
            cnt[array[2]] = int(a[0])
    file1.close()
    ##############################################
    infile = open(annovar, "r")
    outfile = open("%s.annovar.filter.tsv" % (out), "w")
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
            freq = 0
            freq_counts = 0
            counts = 0
            result = ""
            for i in database:
                if array[dict[i]] == ".":
                    pass
                elif array[dict[i]] != "." and float(array[dict[i]]) <= float(maf):
                    freq += 1
                else:
                    freq_counts += 1
            if array[dict['CLNSIG']].startswith("Pathogenic") or array[dict['CLNSIG']].startswith(
                    "Likely_pathogenic") or array[dict['CLNSIG']].startswith("drug_response"):
                result = "true"
            elif array[dict['InterVar_automated']].startswith("Pathogenic") or array[
                dict['InterVar_automated']].startswith("Likely pathogenic"):
                result = "true"
            elif array[dict['cosmic88_coding']].startswith("ID="):
                pattern = re.compile(r'ID=(\S+);')
                a = pattern.findall(array[dict['cosmic88_coding']])
                cosmic = a[0].split(",")
                for i in cosmic:
                    counts += int(cnt[i])
                if counts >=50:
                    result = "true"
            elif freq_counts>=1 or array[8]=="synonymous SNV" or array[5]=="intronic" or array[5]=="intergenic" or array[5].startswith("UTR"):
                    continue
            else:
                result = "true"
            if result == "true":
                for l in range(len(out_name)):
                    if l == 0:
                        outfile.write("%s" % (array[dict[out_name[l]]]))
                    else:
                        outfile.write("\t%s" % (array[dict[out_name[l]]]))
                outfile.write("\n")
    infile.close()
    outfile.close()

if __name__=="__main__":
    if len(sys.argv)!=5:
        print("Usage:\npython3 %s maf annovarfile outdir prefix"%(sys.argv[0]))
        print("Copyright:fanyucai")
        print("Version:1.0")
    else:
        run(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])