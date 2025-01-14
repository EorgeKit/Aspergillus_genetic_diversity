#!/bin/bash
#PBS -l select=2:ncpus=24:mpiprocs=24:mem=120gb
#PBS -q normal
#PBS -P CBBI1470
#PBS -l walltime=8:00:00
#PBS -m abe
#PBS -M georgekitundu2@gmail.com
#PBS -N making_protein_blast_database_each_sample_proteome

module load chpc/BIOMODULES
module load ncbi-blast/2.16.0+

##variables
contigs_dir=/mnt/lustre/users/maloo/allan_project/allan-George/data/announced-contigs
db_dir=/mnt/lustre/users/maloo/allan_project/allan-George/data/database_announced_contigs
predicted_augustus_proteins="/home/maloo/lustre/allan_project/allan-George/data/augustus_proteins"
aug_prot_db_dir=/mnt/lustre/users/maloo/allan_project/allan-George/data/database_augustus_proteins

## code making a nucleotide database of the announced contigs

for sample_contig in $(ls $contigs_dir)
do
echo "This is sample $(basename -s .fa $sample_contig)"
echo
echo "Making NUCLEOTIDE BLAST databse for $sample_contig"

makeblastdb \
    -in $contigs_dir/$sample_contig \
    -parse_seqids \
    -blastdb_version 5 \
    -title "Aspergillus_announced_genome_$(basename -s .fa $sample_contig)" \
    -dbtype nucl \
    -out $db_dir/$(basename -s .fa $sample_contig)/Aspergillus_contig_$(basename -s .fa $sample_contig)
done

##code to make a blast database of the announced contigs augustus predicted proteins

for sample_prediction in $(ls $predicted_augustus_proteins)
do
echo "This is sample $(basename -s .faa $sample_prediction)"
echo
echo "Making AMINO ACID BLAST database for $sample_prediction"

makeblastdb \
    -in $predicted_augustus_proteins/$sample_prediction \
    -parse_seqids \
    -blastdb_version 5 \
    -title "Aflavus_redicted_proteome_$(basename -s .faa $sample_prediction)" \
    -dbtype prot \
    -out $aug_prot_db_dir/$(basename -s .faa $sample_prediction)/Aflavus_proteome_$(basename -s .faa $sample_prediction)

done
