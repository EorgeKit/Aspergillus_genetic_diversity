#!/bin/bash
#PBS -l select=3:ncpus=24:mpiprocs=24:mem=120gb
#PBS -q normal
#PBS -P CBBI1470
#PBS -l walltime=48:00:00
#PBS -m abe
#PBS -M alleankyalo@gmail.com
#PBS -N BLASTN_aflatoxin_clusters_to_announced_contigs_run2

##Author: George Kitundu 1-OCT-2024, second iteration: 15-December-2025, third iteration: 17 Dec 2024
module load chpc/BIOMODULES
module load ncbi-blast/2.16.0+

##Variables
ann_contig_db=/mnt/lustre/users/maloo/allan_project/allan-George/data/database_announced_contigs
af_gene_clusters=/mnt/lustre/users/maloo/allan_project/allan-George/data/aflatoxin_gene_clusters
out_dir=/mnt/lustre/users/maloo/allan_project/allan-George/analysis/blastn_aflx_2_contigs
af_gene_proteins=/home/maloo/lustre/allan_project/allan-George/data/aflatoxin_proteins
out_dir_tblastn=/mnt/lustre/users/maloo/allan_project/allan-George/analysis/tblastn2
af_rep_seqs=/home/maloo/lustre/allan_project/allan-George/analysis/aflavus_rep_seqs_aligned
blastx_repseqs_out=/mnt/lustre/users/maloo/allan_project/allan-George/analysis/blastx


##The following script performs TBLASTN of all represenative gene sequences to augustus predictions of the announced contigs
for rep_seq in $(ls $af_rep_seqs)
do 
    echo "This is aflatoxin rep seq : $(basename -s .faa $af_proteins)"
    echo
    echo "Beginning FOR LOOP iteration for aflatoxin gene/cluster $(basename -s .faa $af_proteins)"
    echo
    for contig_db in $(ls $ann_contig_db)
        do
            echo "This is announced contigs sample: $contig_db"
            echo
            echo "Running TBLASTN of aflatoxin gene/cluster $(basename -s .faa $af_proteins) on Contigs for sample $contig_db"
            echo
            mkdir -p $out_dir_tblastn/$contig_db
            tblastn \
            -query $af_gene_proteins/$af_proteins \
            -db $ann_contig_db/$contig_db/Aspergillus_contig_$contig_db \
            -outfmt 7 -evalue 1 \
            -num_threads 72 -mt_mode 0  \
            > $out_dir_tblastn/$contig_db/TblastN_$(basename -s .faa $af_proteins)_2_$(basename $contig_db).tab
            echo
            echo "Finished running TBLASTN of aflatoxin gene/cluster $(basename -s .faa $af_proteins) on Contigs for sample $contig_db"
            echo
        done
    echo
    echo "Ending FOR LOOP iteration for aflatoxin gene/cluster $(basename -s .faa $af_proteins)"
    echo
done


##The following script performs BLASTN of all obtained gene clsuters to announced contigs

for af_cluster in $(ls $af_gene_clusters)
do
    echo "This is aflatoxin gene/cluster : $(basename -s .fasta $af_cluster)"
    echo
    echo "Beginning FOR LOOP iteration for aflatoxin gene/cluster $(basename -s .fasta $af_cluster)"
    echo
    for contig_db in $(ls $ann_contig_db)
        do
            echo "This is announced contigs sample: $contig_db"
            echo
            echo "Running BLASTN of aflatoxin gene/cluster $(basename -s .fasta $af_cluster) on Contigs for sample $contig_db"
            echo
            mkdir -p $out_dir/$contig_db
            blastn \
            -query $af_gene_clusters/$af_cluster \
            -db $ann_contig_db/$contig_db/Aspergillus_contig_$contig_db \
            -outfmt 7 \
            -num_threads 72 -mt_mode 0 -perc_identity 90 \
            > $out_dir/$contig_db/BlastN_$(basename -s .fasta $af_cluster)_2_$(basename $contig_db).tab
            echo
            echo "Finished running BLASTN of aflatoxin gene/cluster $(basename -s .fasta $af_cluster) on Contigs for sample $contig_db"
            echo
        done
    echo
    echo "Ending FOR LOOP iteration for aflatoxin gene/cluster $(basename -s .fasta $af_cluster)"
    echo
done

# ##The following script performs TBLASTN of all obtained gene clsuters to announced contigs
for af_proteins in $(ls $af_gene_proteins)
do 
    echo "This is aflatoxin gene/cluster : $(basename -s .faa $af_proteins)"
    echo
    echo "Beginning FOR LOOP iteration for aflatoxin gene/cluster $(basename -s .faa $af_proteins)"
    echo
    for contig_db in $(ls $ann_contig_db)
        do
            echo "This is announced contigs sample: $contig_db"
            echo
            echo "Running TBLASTN of aflatoxin gene/cluster $(basename -s .faa $af_proteins) on Contigs for sample $contig_db"
            echo
            mkdir -p $out_dir_tblastn/$contig_db
            tblastn \
            -query $af_gene_proteins/$af_proteins \
            -db $ann_contig_db/$contig_db/Aspergillus_contig_$contig_db \
            -outfmt 7 -evalue 1 \
            -num_threads 72 -mt_mode 0  \
            > $out_dir_tblastn/$contig_db/TblastN_$(basename -s .faa $af_proteins)_2_$(basename $contig_db).tab
            echo
            echo "Finished running TBLASTN of aflatoxin gene/cluster $(basename -s .faa $af_proteins) on Contigs for sample $contig_db"
            echo
        done
    echo
    echo "Ending FOR LOOP iteration for aflatoxin gene/cluster $(basename -s .faa $af_proteins)"
    echo
done


