#!/usr/bin/env python
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="aligner",
        description="Command-line script to perform alignments of fastq files"
    )
    
    # required arguments
    parser.add_argument("idxbase", help="index reference genome file", type=str)
    parser.add_argument("in1.fq", help="input fastq file 1", type=str)
    parser.add_argument("in2.fq", help="input fastq file 2", type=str)    
    
    # optional arguments
    parser.add_argument("-o", "--out", help="sam file to output results to [stdout]" \
        "Default: stdout", type=str, metavar="FILE", required=False)
    parser.add_argument("-A", help="score for a sequence match", metavar="INT",
                        type=int, required=False)
    parser.add_argument("-B", help="penalty for a mismatch", metavar="INT",
                        type=int, required=False)
    parser.add_argument("-O", help="penalties for deletions and insertions", 
                        metavar="INT", type=int, required=False)
    args = parser.parse_args()
    
if __name__ == "__main__":
    main()
