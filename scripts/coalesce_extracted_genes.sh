#!/bin/bash

#This Bash script organizes and consolidates gene-specific FASTA files from multiple sample directories into a centralized structure.

# Define directories
EXTRACTED_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes"
COALESCED_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_genes_coalesced"
GENE_LIST_FILE="/mnt/lustre/users/maloo/allan_project/allan-George/scripts/gene_coordinates.txt"  # Replace with the actual path to your gene list file

# Ensure the target directory exists
mkdir -p "$COALESCED_DIR"

# Extract gene names from the file (ignoring lines starting with '#')
GENES=($(awk '!/^#/ {print $1}' "$GENE_LIST_FILE"))

# Loop through each gene
for gene in "${GENES[@]}"; do
    # Create a directory for the gene in the coalesced directory
    gene_dir="$COALESCED_DIR/$gene"
    mkdir -p "$gene_dir"
    
    echo "Processing gene: $gene"
    
    # Loop through all sample directories
    for sample_dir in "$EXTRACTED_DIR"/*; do
        if [ -d "$sample_dir" ]; then
            # Find the FASTA file for the gene in the current sample directory
            fasta_file=$(find "$sample_dir" -type f -name "Extracted_${gene}_*.fa")
            
            # If the file exists, copy it to the gene directory
            if [ -n "$fasta_file" ]; then
                cp "$fasta_file" "$gene_dir/"
                echo "  Copied $(basename "$fasta_file") to $gene_dir"
            else
                echo "  No FASTA file found for $gene in $(basename "$sample_dir")"
            fi
        fi
    done
done

echo "Coalescing complete."


# The following script renames the headers of FASTA files in each gene directory to match the file name.

# Loop through all subdirectories
for gene_dir in "$COALESCED_DIR"/*; do
    if [ -d "$gene_dir" ]; then
        echo "Processing directory: $gene_dir"
        
       # Loop through all FASTA files in the current gene directory
        for fasta_file in "$gene_dir"/*.fa; do
            if [ -f "$fasta_file" ]; then
                # Extract the file name without the extension and remove "Extracted_"
                file_name=$(basename "$fasta_file" .fa)
                clean_name=${file_name#Extracted_}
                
                # Replace the header with the cleaned file name
                sed -i "1s/.*/>$clean_name/" "$fasta_file"
                
                echo "  Updated header in $fasta_file"
            fi
        done
    fi
done

echo "FASTA header renaming complete."