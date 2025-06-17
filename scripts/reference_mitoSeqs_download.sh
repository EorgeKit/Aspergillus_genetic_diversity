#!/bin/bash
#PBS -l select=2:ncpus=24:mpiprocs=24:mem=120gb
#PBS -N downloading_mitochondrial_references
#PBS -q normal
#PBS -P CBBI1470
#PBS -l walltime=8:00:00
#PBS -m abe
#PBS -M alleankyalo@gmail.com

#Author: GEORGE KITUNDU
#Date: sept 21, 2024

eval "$(conda shell.bash hook)"
conda activate entrez


##variables
accsn_file=/mnt/lustre/users/maloo/mbinda-George/scripts/mito_refs_accsn.txt
out_dir=/mnt/lustre/users/maloo/mbinda-George/data/mitogenomes_refs

for accession in $(cat $accsn_file)
do
epost -db nucleotide -id $accession | efetch -format fasta  > $out_dir/$accession.fasta
done
