#!/usr/bin/env python
import argparse
from typing import Tuple, List

def get_reads(file: str) -> List[str]:
    reads = []
    with open(file) as fastq:
        for line in fastq:
            line = line.rstrip()
            reads.append(line)
    return reads

def local_alignment(match_reward: int, mismatch_penalty: int, indel_penalty: int,
                    s: str, t: str) -> Tuple[int, str, str]:
    score = []
    for row in range(len(s) + 1):
        column = [0] * (len(t) + 1)
        score.append(column)
        
    max_score = 0
    max_i, max_j = 0, 0

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
                max_i, max_j = i, j

    s_alignment, t_alignment = '', ''
    i, j = max_i, max_j
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

    return max_score, s_alignment, t_alignment

def get_alignments(fq: str, fa: str, match: int, mismatch: int, indel: int):
    reads = get_reads(fq)
    genome = ""
    with open(fa) as fasta:
        for line in fasta:
            if not line.startswith(">"):
                genome += line.strip()

    best_alignments = {}
    for read in reads:
        max_local_score = float('-inf')
        best_alignment = (0, "", "")
        for i in range(len(genome) - len(read) + 1):
            window = genome[i:i+len(read)]
            alignment = local_alignment(match, mismatch, indel, window, read)
            if alignment[0] > max_local_score:
                max_local_score = alignment[0]
                best_alignment = alignment
        best_alignments[read] = best_alignment
    return best_alignments

def main():
    parser = argparse.ArgumentParser(
        prog="aligner",
        description="Command-line script to perform alignments of fastq files"
    )

    parser.add_argument("-fa", "--fasta", help="index reference genome file", type=str, required=True)
    parser.add_argument("-fq", "--fastq", help="input fastq file", type=str, required=True)
    parser.add_argument("-o", "--out", help="output file to write results to", type=str, default="output.sam", required=False)
    parser.add_argument("-A", "--match", help="score for a sequence match", type=int, default=1)
    parser.add_argument("-B", "--mismatch", help="penalty for a mismatch", type=int, default=-1)
    parser.add_argument("-O", "--indel", help="penalty for insertions and deletions", type=int, default=-1)
    
    args = parser.parse_args()

    alignments = get_alignments(args.fastq, args.fasta, args.match, args.mismatch, args.indel)

    with open(args.out, 'w') as out_file:
        for read, alignment in alignments.items():
            out_file.write(f"{read}\t{alignment}\n")

if __name__ == "__main__":
    main()
