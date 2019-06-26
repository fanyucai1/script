import os
import shutil
import subprocess
def tumor_only(p1,p2,sampelID,outdir,purity,sex,typen,n1="0",n2="0"):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    ##################################tumor sample
    pe1 = os.path.basename(p1)
    pe2 = os.path.basename(p2)
    if not os.path.exists("%s/%s" %(outdir,pe1)):
        shutil.copy(p1,outdir)
    if not os.path.exists("%s/%s" % (outdir, pe2)):
        shutil.copy(p2,outdir)
    ##################################output parameter
    outfile = open("%s/run_sm_counter_v2.params.txt" % (outdir), "w")
    outfile.write("[general]\n"
                  "cutadaptDir = /opt/conda/bin/\n"
                  "bwaDir      = /opt/conda/bin/\n"
                  "samtoolsDir = /srv/qgen/bin/samtools-1.5/bin/\n"
                  "javaExe     = /opt/conda/jre/bin/java\n"
                  "sswPyFile = /srv/qgen/bin/ssw/src/ssw_wrap.py\n"
                  "torrentBinDir = /srv/qgen/bin/TorrentSuite/\n"
                  "vcflibDir = /srv/qgen/bin/vcflib/bin/\n"
                  "quandicoDir = /srv/qgen/code/qiaseq-dna/copy_number/\n"
                  "numCores = 0\n"
                  "deleteLocalFiles = False\n"
                  "samtoolsMem = 25000M\n"
                  "outputDetail = True\n"
                  "primer3Bases  = 8\n"
                  "genomeFile = /srv/qgen/data/genome/hg19/ucsc.hg19.fa\n"
                  "endogenousLenMin = 15\n"
                  "tagNameUmiSeq    = mi\n"
                  "tagNameUmi       = Mi\n"
                  "tagNameDuplex    = Du\n"
                  "tagNamePrimer    = pr\n"
                  "tagNamePrimerErr = pe\n"
                  "tagNameResample  = re\n"
                  "vcfComplexGapMax = 3\n"
                  "snpEffPath   = /opt/conda/share/snpeff-4.2-0/\n"
                  "snpEffConfig = /opt/conda/share/snpeff-4.2-0/snpEff.config\n"
                  "snpEffData   = /srv/qgen/data/annotation/snpEff/\n"
                  "dbSnpFile    = /srv/qgen/data/annotation/common_all_20160601.vcf.gz\n"
                  "cosmicFile   = /srv/qgen/data/annotation/CosmicAllMuts_v69_20140602.vcf.gz\n"
                  "clinVarFile  = /srv/qgen/data/annotation/clinvar_20160531.vcf.gz\n"
                  "umiCutoff = 10\n"
                  "pValCutoff = 0.01\n"
                  "tumorPurity  = %s\n"
                  "[smCounter]\n"
                  "minBQ = 25\n"
                  "minMQ = 50\n"
                  "hpLen = 8\n"
                  "mismatchThr = 6.0\n"
                  "consThr = 0.8\n"
                  "minAltUMI = 3\n"
                  "maxAltAllele = 2\n"
                  "primerDist = 2\n"
                  "repBed = /srv/qgen/data/annotation/simpleRepeat.full.bed\n"
                  "srBed = /srv/qgen/data/annotation/SR_LC_SL.full.bed\n"
                  "[%s]\n"
                  "readFile1 =/project/%s\n"
                  "readFile2 = /project/%s\n"
                  "instrument = Other\n"
                  "primerFile =/srv/qgen/example/DHS-3501Z.primer3.txt\n"
                  "roiBedFile =/srv/qgen/example/DHS-3501Z.roi.bed\n"
                  "platform = Illumina\n"
                   "runCNV = True\n"
                  "duplex = False\n"
                   % (purity,sampelID, pe1, pe2))
    if type=="cfDNA":
        outfile.write(
            "refUmiFiles =/srv/qgen/data/base_line_cfDNA/%s1.sum.primer.umis.txt,/srv/qgen/data/base_line_cfDNA/%s2.sum.primer.umis.txt,/srv/qgen/data/base_line_cfDNA/%s3.sum.primer.umis.txt,/srv/qgen/data/base_line_cfDNA/%s4.sum.primer.umis.txt\n"
            % (sex, sex, sex,sex))
    else:
        outfile.write("refUmiFiles =/srv/qgen/data/base_line_tissue/%s1.sum.primer.umis.txt,/srv/qgen/data/base_line_tissue/%s2.sum.primer.umis.txt,/srv/qgen/data/base_line_tissue/%s3.sum.primer.umis.txt\n"
                      %(sex,sex,sex))
    ####################################normal sample
    if n1 != "0" and n2 != "0":
        pe3 = os.path.basename(n1)
        pe4 = os.path.basename(n1)
        if not os.path.exists("%s/%s" % (outdir, pe3)):
            shutil.copy(n1, outdir)
        if not os.path.exists("%s/%s" % (outdir, pe4)):
            shutil.copy(n2, outdir)
        outfile.write(
            "sampleType =tumor\n"
            "[normal]\n"
            "readFile1 = /project/%s\n"
            "readFile2 = /project/%s\n"
            "instrument = Other\n"
            "primerFile =/srv/qgen/example/DHS-3501Z.primer3.txt\n"
            "roiBedFile =/srv/qgen/example/DHS-3501Z.roi.bed\n"
            "platform = Illumina\n"
            "sampleType =normal\n"
            "duplex = False\n"%(pe3,pe4))
    else:
        outfile.write("sampleType =Single\n")
    outfile.close()
    ###################################
    cmd = "docker run -v /software/qiaseq-dna/data/:/srv/qgen/data/ -v %s:/project/ " \
          "qiaseq275:1.0 python /srv/qgen/code/qiaseq-dna/run_qiaseq_dna.py run_sm_counter_v2.params.txt v2 single %s" \
          % (outdir, sampelID)
    if not os.path.exists("%s/%s.smCounter.anno.vcf"%(outdir,sampelID)):
        subprocess.check_call(cmd,shell=True)
    else:
        pass