
### step1:make_database.py
    This script will get info from COSMIC and clinvar database to classify sites into germline and somatic.
    
### step2:identify_site.py
    Input vcf and split into three vcf files named:somatic.vcf,germline.vcf and snp.vcf. 
    If database not contains site,this site will be classify by VAF:40=<VAF<=60 and VAF>=95 will be germline,otherwise will be somatic.
