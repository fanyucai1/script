import os
import sys
import argparse
sub=os.path.abspath(__file__)
dir_name=os.path.dirname(sub)
sys.path.append(dir_name)
import core
import shutil
import subprocess

def run(pe1,pe2,samplelist,outdir,prefix):
    core
