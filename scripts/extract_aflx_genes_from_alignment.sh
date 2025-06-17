#!/bin/bash
#PBS -l select=2:ncpus=24:mpiprocs=24:mem=120gb
#PBS -N extract_aflxGenes_mapped_to_contigs
#PBS -q normal
#PBS -P CBBI1470
#PBS -l walltime=48:00:00
#PBS -m abe
#PBS -M alleankyalo@gmail.com

# This script extracts mapped regions from the blastn outputs.
# It loops over each sample directory in the BLAST output folder,
# parses each BLASTN_*.tab file to get hit coordinates, and then
# uses blastdbcmd to extract the corresponding sequence regions.

module load chpc/BIOMODULES
module load ncbi-blast/2.16.0+

# Directories (adjust if necessary)
OUTPUT_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/analysis/blastn_aflxGenes_2_contigs"
DB_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/data/database_announced_contigs"
EXTRACTED_DIR="/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes"

mkdir -p "$EXTRACTED_DIR"

echo "Extracting mapped regions..."

# Loop over sample directories in the BLAST output folder
for sample_path in "$OUTPUT_DIR"/*; do
    if [ -d "$sample_path" ]; then
        sample=$(basename "$sample_path")
        echo "Processing sample: $sample"
        for blast_file in "$sample_path"/BLASTN_*_"$sample".tab; do
            if [ -f "$blast_file" ]; then
                # Extract gene name from filename using the pattern: BLASTN_${gene}_${sample}.tab
                gene=$(basename "$blast_file")
                gene=${gene#BLASTN_}
                gene=${gene%_"$sample".tab}
                
                # Create output directory for the sample if it doesn't exist
                mkdir -p "$EXTRACTED_DIR/$sample"
                # Output file for extracted regions
                # Use the gene name and sample name to create a unique output file
                output_fasta="$EXTRACTED_DIR/$sample/Extracted_${gene}_${sample}.fa"
                echo "  Extracting regions for gene: $gene"
                
                # Remove any existing file for clean extraction
                rm -f "$output_fasta"
                
                while read -r line; do
                    # Skip comment lines (those starting with '#' or blank lines)
                    [[ "$line" =~ ^#.*$ ]] && continue
                    [ -z "$line" ] && continue
                    
                    # Read the BLAST columns:
                    # qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore
                    read -r qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore <<< "$line"
                    # query acc.ver, subject acc.ver, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score
                    # Ensure proper orientation of the subject region
                    if [ "$sstart" -gt "$send" ]; then
                        start=$send
                        end=$sstart
                    else
                        start=$sstart
                        end=$send
                    fi
                    
                    # Extract the region from the corresponding BLAST database using blastdbcmd
                    region=$(blastdbcmd -db "$DB_DIR/$sample/Aspergillus_contig_${sample}" -entry "$sseqid" -range "${start}-${end}" 2>/dev/null)
                    
                    # Warn if no region was extracted
                    if [ -z "$region" ]; then
                        echo "Warning: No region extracted for $sseqid in $blast_file" >&2
                        continue
                    fi
                    
                    # Write to output fasta with a header noting gene, subject, and coordinates.
                    echo ">${gene}_${sseqid}_${start}-${end}" >> "$output_fasta"
                    # Remove the header line from blastdbcmd output and write the sequence
                    echo "$region" | sed '1d' >> "$output_fasta"
                    
                done < "$blast_file"
                
                echo "  Extracted regions written to $(basename "$output_fasta")"
            fi
        done
    fi
done

echo "Extraction complete."