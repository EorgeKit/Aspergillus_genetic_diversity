#!/bin/bash
#PBS -l select=2:ncpus=24:mpiprocs=24:mem=120gb
#PBS -N fastqc_on_raw_data
#PBS -q normal
#PBS -P CBBI1470
#PBS -l walltime=8:00:00
#PBS -m abe
#PBS -M alleankyalo@gmail.com

#Author: GEORGE KITUNDU
#Date: sept 17, 2024

module load chpc/BIOMODULES
module load trimmomatic/0.36

 