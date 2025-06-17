#!/usr/bin/env bash

module load chpc/BIOMODULES
module load bedtools/2.27.1

CLUSTER_FILE="/mnt/lustre/users/maloo/allan_project/allan-George/data/aflatoxin_gene_clusters/AF13-ABGC-AY510451.fasta"
SCRIPT_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/scripts/"
OUT_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/data/aflatoxin_genes_extracted_from_cluster"

mkdir -p "$OUT_DIR"

echo "Starting gene extraction from ${CLUSTER_FILE}..."
echo

while read -r gene start end; do
    # Skip header or comment lines (those starting with '#')
    if [[ "$gene" == \#* ]]; then
        echo "Skipping header/comment line: $gene"
        continue
    fi

    echo
    echo "Processing gene: ${gene} with original coordinates: ${start}-${end}"
    echo

    # Convert start coordinate from 1-based to 0-based for BED format
    bed_start=$((start - 1))
    echo "Converted coordinate for ${gene}: BED start=${bed_start}, end=${end}"
    echo

    # Create a temporary BED file for this gene
    CONTIG="AY510451.1"
    echo -e "${CONTIG}\t${bed_start}\t${end}\t${gene}" > "$SCRIPT_DIR/temp.bed"
    # Extract the gene region using bedtools; the -name option assigns the gene name in the FASTA header.
    bedtools getfasta -fi "$CLUSTER_FILE" -bed $SCRIPT_DIR/temp.bed -fo $OUT_DIR/"${gene}.fa" -name
    
    echo "Extracted ${gene}.fa"
    echo "------------------------------------------"
    echo
    
done < $SCRIPT_DIR/gene_coordinates.txt

rm $SCRIPT_DIR/temp.bed
echo "Done extracting genes."