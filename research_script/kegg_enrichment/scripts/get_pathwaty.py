import sys
import os

if len( sys.argv ) != 3:
        sys.stderr.write("Script to download KEGG pathway maps.\n\n")
        sys.stderr.write("Usage: python %s <outdir> <prefix>\n\n" % sys.argv[0] )
        sys.stderr.write( "This script is used to download KEGG pathway maps\n" )
        sys.exit(1)

outdir = sys.argv[1].strip()
pre = sys.argv[2].strip()


pathway='/allwegene/dat2/pipeline/refTR/Enrichment/KEGG/scripts/pathway_annotation_flow_parallel_simple_tolerant.pyc'

os.chdir(outdir)
kegg_path=open('runPathway.sh','w')
kegg_path.write('python %s --table %s\n' % (pathway,outdir+'/'+pre+'.KEGG_pathway_enrichment_result.xls'))
kegg_path.write('mv %s %s\n' % (outdir+'/'+pre+'.KEGG_pathway_enrichment_result.xls_rendered_html_detail.html',outdir+'/'+pre+'.KEGG_pathway_enrichment_result.html'))
kegg_path.close()

assert not os.system('sh runPathway.sh')
