#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate amas
# This script concatenates all aligned FASTA files from different directories into a single supermatrix alignment file
# and generates a partition file for the concatenated alignment using AMAS.
# It assumes that the aligned files are in subdirectories of a base directory and that they are named 'concatenated_aligned.fa'.

# Define variables
BASE_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_genes_coalesced"
OUTPUT_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/analysis/alignment-supermatrix"
OUTPUT_ALIGNMENT="$OUTPUT_DIR/supermatrix_alignment.fa"
OUTPUT_PARTITIONS="$OUTPUT_DIR/partitions.txt"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Run AMAS to concatenate all aligned files
python /home/maloo/.conda/envs/amas/lib/python3.9/site-packages/amas/AMAS.py concat \
    -i "$BASE_DIR"/*/concatenated_aligned.fa \
    -f fasta \
    -d dna \
    -t "$OUTPUT_ALIGNMENT" \
    -p "$OUTPUT_PARTITIONS"

# Print completion message
echo "Supermatrix alignment created: $OUTPUT_ALIGNMENT"
echo "Partition file created: $OUTPUT_PARTITIONS"