import re
import sys

database = ['1000g2015aug_all','1000g2015aug_eas', 'ExAC_ALL', 'esp6500siv2_all','ExAC_EAS','genome_AF','genome_AF_eas','exome_AF','exome_AF_eas']
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene','ExonicFunc.refGene','AAChange.refGene','cytoBand',
          'avsnp150','ExAC_ALL','ExAC_EAS','esp6500siv2_all','1000g2015aug_all','1000g2015aug_eas','genome_AF','genome_AF_eas','exome_AF','exome_AF_eas',
          'cosmic88_coding','CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG','SIFT_pred','Polyphen2_HDIV_pred', 'Polyphen2_HVAR_pred','MutationTaster_pred','MutationAssessor_pred','FATHMM_pred',
          'CADD_phred','InterVar_automated','UMT','VMT','VMF',"GT"]
cosmic_vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.hg19.vcf"
maf=0.01
##############################################
def germline(maf,annovar,out):
    infile = open(annovar, "r")
    outfile = open("%s.filter.annovar.germline" % (out), "w")
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
            if array[8]=="synonymous SNV" or array[5]=="intronic" or array[5]=="intergenic" or array[5].startswith("UTR"):
                continue
            freq = 0
            freq_counts = 0
            result = ""
            for i in database:
                if array[dict[i]] == ".":
                    pass
                elif array[dict[i]] != "." and float(array[dict[i]]) <= float(maf):
                    freq += 1
                else:
                    freq_counts += 1
            if freq_counts < 3:  # not common snp
                if array[dict['CLNSIG']].startswith("Pathogenic") or array[dict['CLNSIG']].startswith(
                        "Likely_pathogenic") or array[dict['CLNSIG']].startswith("drug_response"):
                    result = "true"
                elif array[dict['InterVar_automated']].startswith("Pathogenic") or array[
                    dict['InterVar_automated']].startswith("Likely pathogenic"):
                    result = "true"
                elif freq >= 1:  # at least 1<MAF
                    result = "true"
                else:
                    pass
            if result == "true":
                outfile.write("%s\n" % (line))
    infile.close()
    outfile.close()
if __name__=="__main__":
    if len(sys.argv)!=4:
        print("Usage:\npython3 filter_germline.py maf annovarfile outdir/prefix")
        print("Copyright:fanyucai")
        print("Version:1.0")
        sys.exit(-1)
    germline(sys.argv[1],sys.argv[2],sys.argv[3])