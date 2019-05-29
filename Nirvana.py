import os
import argparse
import json
import subprocess

dotnet="/software/dotnet/dotnet"
Nirvana="/software/Nirvana/Nirvana.dll"
cache="/software/Nirvana/database/Cache/latest/GRCh37/Ensembl"
ref="/software/Nirvana/database/References/5/Homo_sapiens.GRCh37.Nirvana.dat"
sd="/software/Nirvana/database/GRCh37/"
parser=argparse.ArgumentParser("This script will annotate vcf use Nirvana.")
parser.add_argument("-v","--vcf",required=True,help="vcf file")
parser.add_argument("-p","--prefix",required=True,help="prefix of output")
parser.add_argument("-o","--outdir",required=True,help="output directory")
args=parser.parse_args()
out=args.outdir+args.prefix
cmd=dotnet+" "+Nirvana+" -c "+cache+" -r "+ref+" -i "+args.vcf+" --sd "+sd+" -o "+out
subprocess.check_call(cmd,shell=True)
subprocess.check_call('gunzip %s.json.gz' %(out),shell=True)
outfile=open("%s.tsv" %(out),"w")
outfile.write("chromosome\tposition\trefAllele\taltAlleles\t")
with open("%s.json" % (out), "r") as load_f:
    load_dict = json.load(load_f)
