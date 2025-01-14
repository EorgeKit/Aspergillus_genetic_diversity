#!/usr/bin/env bash

module load chpc/BIOMODULES 
module load bedtools/2.27.1

bed_dir=/mnt/lustre/users/maloo/allan_project/allan-George/analysis/bed_files_representatives
aflavus_rep_seqs=/mnt/lustre/users/maloo/allan_project/allan-George/data/housekeeping_genes
blastn_dir=/mnt/lustre/users/maloo/allan_project/allan-George/analysis/blastn_representative_seqs
announced_contigs=/mnt/lustre/users/maloo/allan_project/allan-George/data/announced-contigs

# Creating bed files based on aligned regions from blastn tabular output
for sample in `ls $blastn_dir`;
do 
    echo "THIS IS SAMPLE $sample"
    echo
    for fasta in `ls $aflavus_rep_seqs`;
    do 
        echo "This is fasta" $fasta
        echo
        mkdir -p $bed_dir/$sample
        grep -v '#' $blastn_dir/$sample/blastN_$(basename -s .fna $fasta)_2_$sample.tab \
        | awk '{
            if ($9 < $10) {
                sign = "+";
                print $2, $9, $10, $1 "." $9 "-" $10, 0, sign;
            } else if ($9 > $10) {
                sign = "-";
                print $2, $10, $9, $1 "." $9 "-" $10, 0, sign;  # Flipped order when $9 > $10
            } else {
                sign = ".";
                print $2, $9, $10, $1 "." $9 "-" $10, 0, sign;
            }
        }' > $bed_dir/$sample/$(basename -s .fna $fasta).bed
        sed -i 's/ \+/\'\t'/g'  $bed_dir/$sample/$(basename -s .fna $fasta).bed
    done
done

#Extracting fasta sequences based on bed files
for sample in `ls -d $bed_dir/*/` ; 
 do
  echo "This is sample $(basename $sample)"
  echo
  for bed in `ls $sample/*.bed`
   do
    echo "This is bed file $(basename $bed)"
    echo
    mkdir -p $bed_dir/../aflavus_rep_seqs_aligned/$(basename $sample)
    bedtools getfasta  -name -s  -fi $announced_contigs/$(basename -s / $sample).fa  \
    -bed $bed  -fo $bed_dir/../aflavus_rep_seqs_aligned/$(basename $sample)/$(basename -s .bed $bed).fasta
    echo
   done
 done

# ##random code
# #code to .....
# for sample in `ls`; 
# do echo "SAMPLE :$sample"; 
# for fasta in $(cat ../../data/available_fasta.txt); 
# do echo "FASTA NAME: $fasta"; 
# cd $sample
# touch unavailable_fasta.txt
# for ufasta in $(cat unavailable_fasta.txt)
# do
# rm -rf BlastN_"$ufasta"_2_"$sample".tab
# rm unavailable_fasta.txt
# cd ../
# done
# done
# done

# random code to rename fasta ids with the corresponding isolate name
for sample in ./*;  do echo $sample; sed -i "s/(+)/(+)_$(basename "$sample")/g;s/(-)/(-)_$(basename "$sample")/g" $sample/*; done


# random code to concatenate the fasta file
for sample in  ../aflavus_rep_seqs_aligned/*;
 do
  echo "Sample: $sample"; 
 for file in $sample/*;
  do 
  echo "File: $file"; 
  cat $file >> ./$(basename -s fasta $file)_concat.fasta;
   done;
done

# for samle in `ls -d */`;
#  do echo;
#  echo "This is $sample"; 
#  echo sed -i 's/ /\t/g' $sample/*.bed;
#   done


# ##renaming fasta headers based on basenames of fasta files
# # Loop through all FASTA files in the current directory
for fasta_file in *.fasta; 
do
    # Get the base name of the file (without path or extension)
    base_name=$(basename "$fasta_file" .fasta)
    # Use awk to replace headers with the base name of the file
    awk -v name="$base_name" 'BEGIN { OFS = "\n" } /^>/ { print ">" name; next } { print }' \
    "$fasta_file" > "modified_$fasta_file"
done

# ##renaming fasta headers based on accesion which is the first part of the fasta header
for fasta_file in *.fasta; 
do
awk '/^>/ {print ">" $1; next} {print}'  $fasta_file > "modified_$fasta_file"
done
