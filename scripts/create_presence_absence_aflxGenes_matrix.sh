#!/bin/bash

# Directories
GENE_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes"
OUTPUT_FILE="/mnt/lustre/users/maloo/allan_project/allan-George/analysis/aflx_diversity/presence_absence_matrix.csv"
GENE_LIST="/mnt/lustre/users/maloo/allan_project/allan-George/scripts/gene_coordinates.txt"
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")

# Extract gene names from the gene list file
awk '!/^#/{print $1}' "$GENE_LIST" > "$OUTPUT_DIR"/gene_list.txt

# Start the matrix with the header row
echo -n "Isolate" > "$OUTPUT_FILE"
while read -r gene; do
    echo -n ",${gene%%_*}" >> "$OUTPUT_FILE"
done < "$OUTPUT_DIR"/gene_list.txt
echo "" >> "$OUTPUT_FILE"

# Loop through each sample directory
for sample_dir in "$GENE_DIR"/*; do
    if [ -d "$sample_dir" ]; then
        sample_name=$(basename "$sample_dir")
        echo -n "$sample_name" >> "$OUTPUT_FILE"

        # Check presence of each gene
        while read -r gene; do
            gene_file="$sample_dir/Extracted_${gene}_${sample_name}.fa"
            if [ -f "$gene_file" ] && [ -s "$gene_file" ]; then
                echo -n ",1" >> "$OUTPUT_FILE"
            else
                echo -n ",0" >> "$OUTPUT_FILE"
            fi
        done < "$OUTPUT_DIR"/gene_list.txt
        echo "" >> "$OUTPUT_FILE"
    fi
done

echo "Presence-absence matrix created: $OUTPUT_FILE"