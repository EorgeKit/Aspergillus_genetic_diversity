#!/bin/bash
#PBS -l select=2:ncpus=24:mpiprocs=24:mem=120gb
#PBS -N blastn_aflxGenes_2_contigs
#PBS -q normal
#PBS -P CBBI1470
#PBS -l walltime=48:00:00
#PBS -m abe
#PBS -M alleankyalo@gmail.com

#Author: GEORGE KITUNDU and some help from github copilot using chatgpt o3-mini model
#Date: May 16, 2025

module load chpc/BIOMODULES
module load ncbi-blast/2.16.0+

# This script performs a blastn mapping of all aflatoxin genes extracted from the cluster AF13-ABGC-AY510451 against contigs from different samples.
# Directories
GENES_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/data/aflatoxin_genes_extracted_from_cluster"
OUTPUT_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/analysis/blastn_aflxGenes_2_contigs"
DB_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/data/database_announced_contigs"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Starting blastn mapping for all genes and samples..."
echo

# Loop through each gene file in GENES_DIR
for gene_file in "$GENES_DIR"/*.fa; do
    gene=$(basename "$gene_file" .fa)
    echo "Mapping gene: $gene"
    
    # Loop through each sample database directory
    for sample_dir in "$DB_DIR"/*; do
        if [ -d "$sample_dir" ]; then
            sample=$(basename "$sample_dir")
            # Assume the database was built using files with a common prefix as below.
            db_prefix="${sample_dir}/Aspergillus_contig_${sample}"
            
            echo "  Running blastn for $gene against sample: $sample"
            echo
            mkdir -p $OUTPUT_DIR/$sample

            # Run blastn command
            # Note: Adjust the blastn command options as needed
            blastn -query "$gene_file" \
                   -db "$db_prefix" \
                   -out "$OUTPUT_DIR/$sample/BLASTN_${gene}_${sample}.tab" \
                   -outfmt 7 -num_threads 48 -mt_mode 0  -perc_identity 90
            echo "  Output written to BLASTN_${gene}_${sample}.tab"
            echo
        fi
    done
    echo "Finished mapping gene: $gene"
    echo "------------------------------------------"
    echo
done

echo "Blastn mapping complete."