# Aligner

`aligner` is a Python package that maps DNA sequences against a larger reference genome. It sequences reads that may contain insertions, deletions, or mutations so that the entire read doesn't need to be an exact match to a portion of the genome. This tool will compare to the `bwa mem` aligner algorithm that we used in Lab 1.

## Installation
You can install the aligner package via pip:
```
pip install git+https://github.com/alisavu/CSE185-Final-Project
```
If the install was successful, the aligner help message should be shown via:
```
aligner -h
```

## Basic Usage
```
aligner [-h] [-o FILE] [-A INT] [-B INT] [-O INT] fasta fastq
```

## Command Line Arguments
- `fasta`: fasta file of reference genome
- `fastq`: fastq file of reads
- `-o`, `--out`: output results to file
- `-A`, `--match`: score for a sequence match
- `-B`, `--mismatch`: score for a mismatch
- `-O`, `--indel`: score for an indel 