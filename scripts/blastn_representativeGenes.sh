#!/bin/bash
#PBS -l select=3:ncpus=24:mpiprocs=24:mem=120gb
#PBS -q normal
#PBS -P CBBI1470
#PBS -l walltime=48:00:00
#PBS -m abe
#PBS -M alleankyalo@gmail.com
#PBS -N BLASTN_A.flavus_represenative_genes_to_announced_contigs

##Author: George Kitundu 16-December-2024

module load chpc/BIOMODULES
module load ncbi-blast/2.16.0+

ann_contig_db=/mnt/lustre/users/maloo/allan_project/allan-George/data/database_announced_contigs
aFlavus_rep_seqs=/mnt/lustre/users/maloo/allan_project/allan-George/data/housekeeping_genes
out_dir_blastn=/mnt/lustre/users/maloo/allan_project/allan-George/analysis/blastn_representative_seqs


##The following script performs BLASTN of A.flavus represenative genes to announced contigs
for af_rep_seq in $(ls $aFlavus_rep_seqs)
do 
    echo "This is A.flavus represenative gene: $(basename -s .fna $af_rep_seq)"
    echo
    echo "Beginning FOR LOOP iteration for A.flavus represenative gene $(basename -s .fna $af_rep_seq)"
    echo
    for contig_db in $(ls $ann_contig_db)
        do
            echo "This is announced contigs sample: $contig_db"
            echo
            echo "Running BLASTN of A.flavus represenative gene: $(basename -s .fna $af_rep_seq) on Contigs for sample $contig_db"
            echo
            mkdir -p $out_dir_blastn/$contig_db
            blastn \
            -query $aFlavus_rep_seqs/$af_rep_seq \
            -db $ann_contig_db/$contig_db/Aspergillus_contig_$contig_db \
            -outfmt 7 -evalue 1  \
            -num_threads 72 -mt_mode 0  -perc_identity 90 \
            > $out_dir_blastn/$contig_db/blastN_$(basename -s .fna $af_rep_seq)_2_$(basename $contig_db).tab
            echo
            echo "Finished running BLASTN of A.flavus represenative gene: $(basename -s .fna $af_rep_seq) on Contigs for sample $contig_db"
            echo
        done
    echo
    echo "Ending FOR LOOP iteration for A.flavus represenative gene: $(basename -s .fna $af_rep_seq)"
    echo
done
