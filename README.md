# Aligner

`aligner` is a Python package that maps DNA sequences against a larger reference genome. It sequences reads that may contain insertions, deletions, or mutations so that the entire read doesn't need to be an exact match to a portion of the genome. This tool will compare to the `bwa mem` aligner algorithm that we used in Lab 1.

To open help menu: python aligner.py --help\
usage: aligner [-h] [-o FILE] [-A INT] [-B INT] [-O INT] idxbase in1.fq in2.fq
