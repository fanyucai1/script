#! /bin/bash

# author: d2jvkpn
# date: 2017-04-13
# description: convert bam to cram, sam to cram, and cram to sam.

usage=$(
cat <<EOF
Convert bam to cram, sam to cram, and cram to bam, USAGE:
    sh  $0  -f  <genome fasta>  -i  <input bam/sam/cram>  -p  [compress threads]

    Note: Make sure you have samtools 1.0 or higher, and multi input files as
      arguments should be quoted, E.g. -i "1.bam 2.sam 3.cram".
EOF
)

if [ -z $1 ] || [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; then
    echo "$usage"; exit 0
fi

test -z $(which samtools)  &&  { echo "Can't usage samtools"; exit; }

while getopts "i:f:p:" arg; do
    case $arg in
        i) input=$OPTARG;;
        f) genome_fa=$OPTARG;;
        p) threads="-@ $OPTARG";;
        *) exit;;
    esac
done

if [ -z $genome_fa ] || [ ! -s $genome_fa ]; then
    echo "Genome fasta \"$genome_fa\" not available."; exit
fi

for i in $input; do
    test -s $i  ||  { echo -e "Input file \"$i\" not exists.\n"; continue; }

    if [[ $i == *".bam" ]] || [ $i == *".sam" ]; then
        o=${i%.bam}.cram; o=${o%.sam}; bC="-C"

    elif [[ $i == *".cram" ]]; then
        o=${i%.cram}.bam; bC="-b"

    else
        echo -e "Wrong filename extension \"$i\".\n"; continue

    fi

    test -s $o  &&  { echo -e "\"$o\" exists, skip.\n"; continue; }

    echo "Convert \"$i\" to \"$o\", $(date)"
    samtools view $threads -T $genome_fa $i $bC -o $o

    test $? -eq 0 -a -s $o  &&  echo -e "    OK\n"  ||
    { echo -e "    FAILED\n"; rm $o; }

done
