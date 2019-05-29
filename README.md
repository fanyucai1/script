# vcf文件注释说明

## 关于annovar的注释说明

*common snp in dbsnp*

    common SNP is one that has at least one 1000Genomes population with a MAF >= 1% and for which 2 or more founders contribute to that minor allele frequency 
    ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/

*Variants listed in COSMIC were considered hotspot point mutations if they presented with >=5 mentions*
    
    Cheng D T, Mitchell T N, Zehir A, et al. Memorial Sloan Kettering-Integrated Mutation Profiling of Actionable Cancer Targets (MSK-IMPACT): a hybridization capture-based next-generation sequencing clinical assay for solid tumor molecular oncology[J]. The Journal of molecular diagnostics, 2015, 17(3): 251-264.
    Analysis of Tumor Mutational Burden with TruSight® Tumor 170

*filter*

    filter:synonymous SNV,intronic,intergenic
    filter:(MAF>0.01):1000g2015aug_all','ExAC_ALL','esp6500siv2_all','genomeAD'

*non-synonymous variants annotation*

    'SIFT_pred','Polyphen2_HDIV_pred','CADD_phred','FATHMM_pred','MutationAssessor_pred'
*clivar*
        
        
   
## 从37版本转化为hg19的说明    
     ftp://gsapubftp-anonymous@ftp.broadinstitute.org/Liftover_Chain_Files/b37tohg19.chain
***
     gatk  --java-options "-Djava.io.tmpdir=./ -Xmx60G"" LiftoverVcf -I query.vcf.gz -O query.hg19.vcf.gz -R ucsc.hg19.fasta --REJECT unmapped.vcf -C b37tohg19.chain
     bgzip -c query.hg19.vcf > query.hg19.vcf.gz
     tabix -p vcf query.hg19.vcf.gz
 
## 参考基因组hg19下载的说明
    ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg19/ucsc.hg19.fasta.gz
    
## 关于hgvs [http://varnomen.hgvs.org/recommendations/general/]
	
	“c.” for a coding DNA reference sequence
	
    “g.” for a linear genomic reference sequence
    
    “m.” for a mitochondrial DNA reference sequence
    
    “n.” for a non-coding DNA reference sequence
    
    “o.” for a circular genomic reference sequence
    
    “p.” for a protein reference sequence
    
    “r.” for an RNA reference sequence (transcript)

## 关于经典转录本 [https://ionreporter.thermofisher.com/ionreporter/help/GUID-A5502535-2C81-46FD-93C2-50FCB1F02CFD.html]

protein-coding gene:
    
    19196+23 https://www.genenames.org/download/statistics-and-files/
    
    19054 found in gencode.v30lift37.annotation.gtf
    
    5444 gene not found appris_principal_1标签使用最长转录本代替