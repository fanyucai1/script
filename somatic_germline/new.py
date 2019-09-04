import re
import os
import subprocess

clinvar_vcf="/data/Database/clinvar/variant_summary.txt"
clinvar_anno="/data/Database/clinvar/2019.7.20/clinvar.vcf"
annovar="/software/docker_tumor_base/Resource/Annovar/"
Canonical_transcript_file="/data/Database/knownCanonical/clinvar_canonical_trans.txt"
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene','ExonicFunc.refGene','AAChange.refGene','cytoBand',
          'avsnp150','snp138','ExAC_ALL','esp6500siv2_all','1000g2015aug_all','genome_AF','exome_AF',
          'cosmic88_coding','CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG','InterVar_automated','Canonical_transcript','SIFT_pred','Polyphen2_HDIV_pred', 'Polyphen2_HVAR_pred','MutationTaster_pred','MutationAssessor_pred','FATHMM_pred',
          'CADD_phred','FORMAT']
def run(vcf,sample_name,outdir,prefix):
    #####################
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out = outdir + "/" + prefix
    #####################parse input vcf and clinvar
    dict={}
    cmd="perl %s/convert2annovar.pl -format vcf4 %s >%s.avinput"%(annovar,vcf,out)
    subprocess.check_call(cmd,shell=True)
    infile=open("%s.avinput","r")
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        tmp=array[0]+"\t"+array[1]+"\t"+array[3]+"\t"+array[4]
        dict[tmp]=1
    infile.close()
    AlleleID={}
    infile=open(clinvar_anno,"r")
    for line in infile:
        line=line.strip()
        array=line.split("\t")
        if not line.startswith("#"):
            AlleleID[array[0]]=array[2]
    infile.close()
    infile = open(clinvar_vcf, "r")
    for line in infile:
        if not line.startswith("#"):
            p=re.compile(r'ALLELEID=(\d+);')
            line = line.strip()
            array = line.split("\t")
            tmp=array[0]+"\t"+array[1]+"\t"+array[3]+"\t"+array[4]
            a=p.findall(line)
            if tmp in dict:
                dict[tmp]=AlleleID[a[0]]
    infile.close()
    ###############################run annovar
    par = " -protocol refGeneWithVer,cytoBand,snp138,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118"
    par += " -operation g,r,f,f,f,f,f,f,f,f,f,f,f "
    par += " -nastring . -polish "
    subprocess.check_call("perl %s/table_annovar.pl %s %s/humandb -buildver hg19 -out %s -remove %s -vcfinput " % (
    annovar, vcf, annovar, out, par), shell=True)
    ###############################
    transcript = {}
    infile = open(Canonical_transcript_file, "r")
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        transcript[array[0]] = []
        for i in range(1, len(array)):
            tmp = array[i].split(".")
            transcript[array[0]].append(tmp[0])
    #################################
    invcf = open("%s.hg19_multianno.vcf" % (out), "r")
    format,sample = 0,0
    for line in invcf:
        line = line.strip()
        array = line.split("\t")
        if line.startswith("#CHROM"):
            for i in range(len(array)):
                if array[i] == "FORMAT":
                    format = i
                if array[i] == sample_name:
                    sample = i
        else:
            continue
    invcf.close()
    #################################
    outfile = open("%s.annovar.tsv" % (out), "w")
    for i in range(len(out_name)):
        if i == 0:
            outfile.write("%s" % (out_name[i]))
        else:
            outfile.write("\t%s" % (out_name[i]))
    outfile.write("\n")

    infile = open("%s.hg19_multianno.txt" % (out), "r")
    name=[]
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        tmp=
        if line.startswith("Chr"):
            for i in range(len(array)):
                if array[i] != "Otherinfo":
                    name.append(array[i])
                    dict[array[i]] = i
            column = len(array) - 1
        else:
            final_nm = ""
            tmp = array[dict['AAChange.refGene']].split(",")
            if not array[6] in transcript:
                print(array[6])
                final_nm = tmp[0]
            else:
                if len(tmp) == 1:
                    final_nm = tmp[0]
                else:
                    if final_nm == "":
                        for i in transcript[array[6]]:
                            if final_nm == "":
                                for k in tmp:
                                    if final_nm == "" and re.search(i, k):
                                        final_nm = k
                                        continue
            for m in range(len(out_name)):
                if m == 0:
                    outfile.write("%s" % (array[dict[out_name[m]]]))
                elif out_name[m] == "Canonical_transcript":
                    outfile.write("\t%s" % (final_nm))
                elif out_name[m] == "FORMAT":
                    outfile.write("\t%s" % (array[column + format + 3]))
                elif out_name[m] == sample_name:
                    outfile.write("\t%s" % (array[column + sample + 3]))
                else:
                    outfile.write("\t%s" % (array[dict[out_name[m]]]))
            outfile.write("\n")
            if array[8] == "synonymous SNV" or array[5] == "intronic" or array[5] == "intergenic" or array[
                5].startswith("UTR"):
                continue
            result, counts, freq = "", 0, 0
            if array[dict['CLNSIG']].startswith("Pathogenic") or array[dict['CLNSIG']].startswith(
                    "Likely_pathogenic") or array[dict['CLNSIG']].startswith("drug_response"):
                result = "true"
            if array[dict['InterVar_automated']].startswith("Pathogenic") or array[
                dict['InterVar_automated']].startswith("Likely pathogenic"):
                result = "true"
            if array[dict['cosmic88_coding']].startswith("ID="):
                pattern = re.compile(r'ID=(\S+);')
                a = pattern.findall(array[dict['cosmic88_coding']])
                cosmic = a[0].split(",")
                for i in cosmic:
                    counts += int(cnt[i])
                if counts >= 50:
                    result = "true"
            for i in database:
                if array[dict[i]] != "." and float(array[dict[i]]) > 0.01:
                    freq += 1
            if result == "true":
                for l in range(len(out_name)):
                    if l == 0:
                        filter.write("%s" % (array[dict[out_name[l]]]))
                    elif out_name[l] == "Canonical_transcript":
                        filter.write("\t%s" % (final_nm))
                    elif out_name[l] == "FORMAT":
                        filter.write("\t%s" % (array[column + format + 3]))
                    elif out_name[l] == sample_name:
                        filter.write("\t%s" % (array[column + sample + 3]))
                    else:
                        filter.write("\t%s" % (array[dict[out_name[l]]]))
                filter.write("\n")
            else:
                if freq == 0:
                    for l in range(len(out_name)):
                        if l == 0:
                            filter.write("%s" % (array[dict[out_name[l]]]))
                        elif out_name[l] == "Canonical_transcript":
                            filter.write("\t%s" % (final_nm))
                        elif out_name[l] == "FORMAT":
                            filter.write("\t%s" % (array[column + format + 3]))
                        elif out_name[l] == sample_name:
                            filter.write("\t%s" % (array[column + sample + 3]))
                        else:
                            filter.write("\t%s" % (array[dict[out_name[l]]]))
                    filter.write("\n")
    outfile.close()
    filter.close()
    infile.close()
    subprocess.check_call("rm -rf %s.avinput %s.hg19_multianno.vcf %s.hg19_multianno.txt" % (out, out, out), shell=True)

