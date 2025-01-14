#!/bin/bash
#PBS -l select=3:ncpus=24:mpiprocs=24:mem=120gb
#PBS -q normal
#PBS -P CBBI1470
#PBS -l walltime=48:00:00
#PBS -m abe
#PBS -M alleankyalo@gmail.com
#PBS -N orthofinder_to_detect_single_copy_orthologous_genes

eval "$(conda shell.bash hook)"
conda activate orthoFinder

##Variables 
predicted_proteins="/home/maloo/lustre/allan_project/allan-George/data/augustus_proteins"
ortho_out_dir="/home/maloo/lustre/allan_project/allan-George/analysis/orthoFinder"


##Run orthofinder
orthofinder \
-t 72 -a 72 -M msa -A mafft -S diamond -T fasttree \
-f $predicted_proteins \
-o $ortho_out_dir