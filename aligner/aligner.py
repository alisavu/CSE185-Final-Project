#!/usr/bin/env python
import argparse
from typing import Tuple
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

# find local alignment between each read in fastq file & reference genome in fasta file
"""Input: A match reward, a mismatch penalty, an indel penalty, & 2 nucleotide strings
    Output: The maximum score of a local alignment of two strings, followed by a local
            alignment of these strings achieving the maximum score."""
def local_alignment(match_reward: int, mismatch_penalty: int, indel_penalty: int,
                    s: str, t: str) -> Tuple[int, str, str]:
    score = []
    for row in range(len(s) + 1):
        column = [0] * (len(t) + 1)
        score.append(column)
        
    max_score = 0
    max_s = 0
    max_t = 0
    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            if s[i - 1] == t[j - 1]:
                match_mismatch = score[i - 1][j - 1] + match_reward
            else:
                match_mismatch = score[i - 1][j - 1] - mismatch_penalty
            deletion = score[i - 1][j] - indel_penalty
            insertion = score[i][j - 1] - indel_penalty
            score[i][j] = max(0, match_mismatch, deletion, insertion)
            if score[i][j] > max_score:
                max_score = score[i][j]
                max_s =  i
                max_t = j
    
    s_alignment = ''
    t_alignment = ''
    i = max_s
    j = max_t
    while i > 0 and j > 0 and score[i][j] > 0:
        if s[i - 1] == t[j - 1]:
            match_mismatch = score[i - 1][j - 1] + match_reward
        else:
            match_mismatch = score[i - 1][j - 1] - mismatch_penalty
        if score[i][j] == match_mismatch:
            s_alignment = s[i - 1] + s_alignment
            t_alignment = t[j - 1] + t_alignment
            i -= 1
            j -= 1
        elif score[i][j] == score[i - 1][j] - indel_penalty:
            s_alignment = s[i - 1] + s_alignment
            t_alignment = '-' + t_alignment
            i -= 1
        else:
            s_alignment = '-' + s_alignment
            t_alignment = t[j - 1] + t_alignment
            j -= 1  
    return max_score

#output: [read: best alignment]
def get_alignments(file, match, mismatch, indel):
    genome = ""
    reads = get_reads(file)
    read_lengths = []
    read_scores = []
    best_alignment = {}
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
            local_alignment = local_alignment(10, 10, 10, window, reads[j])
            read_scores.append(local_alignment)
            #compare prev w current local alignments, take max score
        for score in read_scores:
            max_local_score = float('-inf')
            if score > max_local_score:
                score = max_local_score     
    return local_alignment

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
