#!/usr/bin/env python
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="bwa mem",
        desctription="Command-line script to perform alignments of fastq files"
    )
    
    # required
    parser.add_argument("idxbase", help="index reference genome file", type=str)
    parser.add_argument("in1.fq", help="input fastq file 1", type=str)
    parser.add_argument("in2.fq", help="input fastq file 2", type=str)    
    
    # optional
    parser.add_argument("-o", "--out", help="Write output to file." \
        "Defualt: stdout", metavar="FILE", type=str, required=False)
    parser.add_argument("-f", "--fasta-ref", \
        help="faidx indexed reference sequence file")
    args = parser.parse_args()
    
    if __name__ == "__main__":
        main()