#!/bin/python

import os
import subprocess
import sys

def run_iqtree_phylogeny(input_alignment_file, output_dir, iqtree_path="iqtree2", bootstrap_reps=1000, threads="AUTO"):
    """
    Performs phylogenetic tree inference using IQ-TREE, including model selection and bootstrapping.

    Args:
        input_alignment_file (str): Full path to the trimmed multiple sequence alignment FASTA file.
                                    (e.g., /mnt/lustre/.../aligned_core_genes/core_genes_mafft_trimmed.fasta)
        output_dir (str): Directory where IQ-TREE output files (tree, log, etc.) will be saved.
        iqtree_path (str): Path to the IQ-TREE executable. Assumes 'iqtree2' is in PATH by default.
                           Specify full path if not (e.g., '/usr/local/bin/iqtree2').
        bootstrap_reps (int): Number of ultrafast bootstrap replicates for branch support. Default is 1000.
        threads (str): Number of parallel threads to use. "AUTO" uses all available cores.
                       Specify an integer for a fixed number (e.g., "8").
    """
    print(f"Starting IQ-TREE phylogenetic inference for: {input_alignment_file}")
    print(f"Output files will be saved to: {output_dir}")

    # 1. Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Ensured output directory '{output_dir}' exists.")

    # 2. Verify input alignment file exists
    if not os.path.exists(input_alignment_file):
        print(f"Error: Input alignment file '{input_alignment_file}' not found.", file=sys.stderr)
        sys.exit(1)

    # 3. Get the base name of the alignment file for IQ-TREE's -prefix
    alignment_basename = os.path.basename(input_alignment_file)
    # Remove file extension for the prefix
    prefix = os.path.splitext(alignment_basename)[0]
    output_prefix_path = os.path.join(output_dir, prefix)

    # 4. Construct the IQ-TREE command
    # -s: input alignment file
    # -m TEST: automatically select the best-fit model (ModelFinder)
    # --alrt <reps>: perform SH-aLRT test for branch support
    # -bb <reps>: perform Ultrafast Bootstrap (UFBoot) for branch support (IQ-TREE 2 uses -B or -bb)
    # -T <threads>: number of threads/cores to use (AUTO for all available)
    # -redo: overwrite existing files (useful for re-runs)
    # -prefix: specify prefix for output files and the output directory for them
    iqtree_command = [
        iqtree_path,
        "-s", input_alignment_file,
        "-m", "TEST",            # ModelFinder: best-fit model selection
        "--alrt", str(bootstrap_reps), # SH-aLRT test for branch support
        "-b", str(bootstrap_reps),  # Ultrafast Bootstrap replicates (use -bb with iqtree2)
        "-T", str(threads),      # Number of threads (use -T with iqtree2)
        "-redo",                 # Overwrite existing files
        "--prefix", output_prefix_path # Output prefix and directory
    ]

    print(f"Executing IQ-TREE command: {' '.join(iqtree_command)}")

    # 5. Execute IQ-TREE
    try:
        process = subprocess.run(
            iqtree_command,
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture standard error
            check=True,              # Raise CalledProcessError for non-zero exit codes
            text=True                # Capture output as text
        )

        print("IQ-TREE execution successful.")
        
        # Print stdout and stderr for user's review
        if process.stdout:
            print("\nIQ-TREE Standard Output:")
            print(process.stdout)
        if process.stderr:
            print("\nIQ-TREE Standard Error (may contain warnings/progress):")
            print(process.stderr)

        print(f"\nPhylogenetic analysis complete. Check '{output_dir}' for results.")
        print(f"The main tree file will be: {output_prefix_path}.treefile")

    except subprocess.CalledProcessError as e:
        print(f"Error during IQ-TREE execution. Command '{e.cmd}' returned non-zero exit status {e.returncode}.", file=sys.stderr)
        print(f"IQ-TREE stderr: \n{e.stderr}", file=sys.stderr)
        print("Please check IQ-TREE output for detailed error messages.", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: IQ-TREE executable not found. Please ensure '{iqtree_path}' is correct and IQ-TREE is installed and in your system's PATH (after loading modules).", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during IQ-TREE analysis: {e}", file=sys.stderr)

    print("\nIQ-TREE script finished.")

if __name__ == "__main__":
    # --- Configuration ---
    # Path to your trimmed multiple sequence alignment file (output from Aliview after trimming)
    INPUT_ALIGNMENT_FILE = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/core_aflx_genes_aligned/concatenated_core_genes/aligned_core_genes/core_genes_mafft_trimmed.fasta"
    
    # Directory to store IQ-TREE's output files (tree, log, statistics)
    OUTPUT_TREE_DIR = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/core_aflx_genes_aligned/concatenated_core_genes/aligned_core_genes/phylogenetic_tree"
    
    # Path to the IQ-TREE executable.
    # Set to "iqtree2" based on your cluster's executable name.
    IQ_TREE_PATH = "iqtree2" 

    # Number of bootstrap replicates (e.g., 1000 for good support values)
    BOOTSTRAP_REPLICATES = 1000

    # Number of CPU threads to use. "AUTO" is usually best on clusters.
    # You can specify an integer if you want to limit it (e.g., 8)
    NUM_THREADS = "AUTO" 

    run_iqtree_phylogeny(
        INPUT_ALIGNMENT_FILE,
        OUTPUT_TREE_DIR,
        iqtree_path=IQ_TREE_PATH,
        bootstrap_reps=BOOTSTRAP_REPLICATES,
        threads=NUM_THREADS
    )
