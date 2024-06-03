#!/usr/bin/env python
import argparse

#read reads from fastq file
#for each read find max score against ref genome
#output alignments in sam file

def get_reads(file):
    reads = []
    with open(file) as fastq:
        for line in fastq:
            line = line.rstrip()
            reads.append(line)
    return reads

def locAL_linear(file, match, mismatch, indel):
    sequences = []
    with open(file, 'r') as fasta:
        sequence = ''
        for line in fasta:
            if line.startswith('>'):
                if sequence:
                    sequences.append(sequence)
                    sequence = ''
            else:
                sequence += line.strip()
        sequences.append(sequence)
    s = sequences[0]
    t = sequences[1]

    max_score = 0
    max_pos = (0, 0)
    curr_row = [0] * (len(t) + 1)
    prev_row = [0] * (len(t) + 1)

    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            if s[i - 1] == t[j - 1]:
                match_mismatch = prev_row[j - 1] + match
            else:
                match_mismatch = prev_row[j - 1] + mismatch
            deletion = prev_row[j] + indel
            insertion = curr_row[j - 1] + indel
            curr_row[j] = max(0, match_mismatch, deletion, insertion)
            if curr_row[j] > max_score:
                max_score = curr_row[j]
                max_pos = (i, j)

        prev_row = curr_row
        curr_row = [0] * (len(t) + 1)

    i, j = max_pos
    s_alignment = ''
    t_alignment = ''

    while i > 0 and j > 0 and prev_row[j] > 0:
        if s[i - 1] == t[j - 1]:
            match_mismatch = prev_row[j - 1] + match
        else:
            match_mismatch = prev_row[j - 1] + mismatch
        if prev_row[j] == match_mismatch:
            s_alignment = s[i - 1] + s_alignment
            t_alignment = t[j - 1] + t_alignment
            i -= 1
            j -= 1
        elif prev_row[j] == curr_row[j] + indel:
            s_alignment = s[i - 1] + s_alignment
            t_alignment = '-' + t_alignment
            i -= 1
        else:
            s_alignment = '-' + s_alignment
            t_alignment = t[j - 1] + t_alignment
            j -= 1
    len_best_alignment = len(s_alignment)
    return max_score, len_best_alignment, s_alignment, t_alignment

def get_alignments(file, match, mismatch, indel):
    genome = ""
    alignments = []
    reads = get_reads(file)
    read_lengths = []
    #get read length
    for i in reads:
        length = len(i)
        read_lengths.append(length)
    with open(file) as fasta:
        for line in fasta:
            if line.startswith() == False:
                genome += line
    for i in genome:
        for j in read_lengths:
            window = genome[i:i+j]
            local_alignment = locAL_linear()
            #compare prev w current local alignments, take max score
        
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
