import os
import subprocess
import sys
import tempfile
import re

def run_single_gene_phylogeny(
    core_gene_dir,                  # e.g., /mnt/lustre/.../core_aflx_genes_aligned/adhA
    output_base_dir,                # e.g., /mnt/lustre/.../individual_core_gene_trees
    gene_name,                      # e.g., "adhA"
    mafft_path="mafft",
    iqtree_path="iqtree2",
    bootstrap_reps=1000,
    threads="AUTO"
):
    """
    Performs alignment (MAFFT) and phylogenetic tree inference (IQ-TREE2) for a single core gene.
    Renames FASTA headers to '>geneName_isolateName' before alignment.

    Args:
        core_gene_dir (str): Path to the directory containing all isolates' FASTA files for this specific gene.
        output_base_dir (str): Base directory where all individual gene tree outputs will go.
        gene_name (str): The name of the core gene being processed (e.g., "adhA").
        mafft_path (str): Path to the MAFFT executable.
        iqtree_path (str): Path to the IQ-TREE2 executable.
        bootstrap_reps (int): Number of ultrafast bootstrap replicates.
        threads (str): Number of parallel threads for IQ-TREE2.
    """
    print(f"\n--- Processing gene: {gene_name} ---")
    
    # 1. Define output directory for this specific gene
    gene_output_dir = os.path.join(output_base_dir, gene_name)
    os.makedirs(gene_output_dir, exist_ok=True)
    print(f"Output for {gene_name} will be in: {gene_output_dir}")

    # 2. Collect all FASTA files for the current gene across isolates
    gene_fasta_files = []
    for fname in os.listdir(core_gene_dir):
        # We need to ensure we only pick FASTA files, and maybe match a pattern if needed
        if fname.startswith(f"Extracted_{gene_name}_") and (fname.endswith(".fa") or fname.endswith(".fasta")):
            gene_fasta_files.append(os.path.join(core_gene_dir, fname))
    
    if not gene_fasta_files:
        print(f"Warning: No FASTA files found for gene '{gene_name}' in '{core_gene_dir}'. Skipping.", file=sys.stderr)
        return

    # Check if there are enough sequences for alignment (min 2)
    if len(gene_fasta_files) < 2:
        print(f"Warning: Only {len(gene_fasta_files)} sequence(s) found for gene '{gene_name}'. Need at least 2 for alignment. Skipping.", file=sys.stderr)
        return

    print(f"Found {len(gene_fasta_files)} sequences for gene '{gene_name}' to align.")

    # 3. Prepare temporary input for MAFFT with renamed headers
    mafft_input_content = ""
    for fasta_file in gene_fasta_files:
        try:
            # Extract isolate name from filename (e.g., Extracted_..._10B.fa -> 10B)
            isolate_match = re.search(r'_([0-9A-Za-z]+)\.fa$', os.path.basename(fasta_file))
            if isolate_match:
                isolate_id = isolate_match.group(1)
                
                # Construct the NEW FASTA header: >geneName_isolateName
                new_fasta_header = f">{gene_name}_{isolate_id}"

                # Read sequence from FASTA file
                with open(fasta_file, 'r') as f:
                    lines = f.readlines()
                    # Skip existing header, join sequence lines
                    sequence_lines = [line.strip() for line in lines if not line.startswith('>')]
                    mafft_input_content += new_fasta_header + "\n" + "".join(sequence_lines) + "\n"
            else:
                print(f"Warning: Could not extract isolate ID from {fasta_file}. Skipping this file.", file=sys.stderr)
        except Exception as e:
            print(f"Error reading sequence from {fasta_file}: {e}. Skipping this file.", file=sys.stderr)
            continue # Continue to next file if one fails to read

    if not mafft_input_content.strip():
        print(f"Error: No valid sequences collected for gene '{gene_name}'. Skipping alignment.", file=sys.stderr)
        return

    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=f"_{gene_name}_mafft_in.fasta") as temp_mafft_in:
        temp_mafft_in.write(mafft_input_content)
        temp_mafft_in_path = temp_mafft_in.name
    print(f"Created temporary MAFFT input for {gene_name} with renamed headers: {temp_mafft_in_path}")

    # 4. Run MAFFT alignment
    aligned_fasta_file = os.path.join(gene_output_dir, f"{gene_name}_aligned.fasta")
    mafft_command = [mafft_path, "--auto", temp_mafft_in_path]

    print(f"Running MAFFT for {gene_name}: {' '.join(mafft_command)} > {aligned_fasta_file}")
    try:
        with open(aligned_fasta_file, 'w') as outfile:
            subprocess.run(
                mafft_command,
                stdout=outfile,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
        print(f"MAFFT alignment for {gene_name} successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during MAFFT alignment for {gene_name}. Stderr: \n{e.stderr}", file=sys.stderr)
        if os.path.exists(temp_mafft_in_path): os.remove(temp_mafft_in_path)
        return
    except FileNotFoundError:
        print(f"Error: MAFFT executable '{mafft_path}' not found for gene {gene_name}. Ensure it's in PATH.", file=sys.stderr)
        if os.path.exists(temp_mafft_in_path): os.remove(temp_mafft_in_path)
        return
    finally:
        if os.path.exists(temp_mafft_in_path):
            os.remove(temp_mafft_in_path)

    # 5. Run IQ-TREE2 phylogenetic inference
    iqtree_output_prefix = os.path.join(gene_output_dir, gene_name)
    iqtree_command = [
        iqtree_path,
        "-s", aligned_fasta_file,
        "-m", "TEST",
        "--alrt", str(bootstrap_reps),
        "-b", str(bootstrap_reps),
        "-T", str(threads),
        "-redo",
        "--prefix", iqtree_output_prefix
    ]

    print(f"Running IQ-TREE2 for {gene_name}: {' '.join(iqtree_command)}")
    try:
        process = subprocess.run(
            iqtree_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        print(f"IQ-TREE2 for {gene_name} successful. Tree: {iqtree_output_prefix}.treefile")
    except subprocess.CalledProcessError as e:
        print(f"Error during IQ-TREE2 execution for {gene_name}. Stderr: \n{e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: IQ-TREE2 executable '{iqtree_path}' not found for gene {gene_name}. Ensure it's in PATH.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during IQ-TREE2 analysis for {gene_name}: {e}", file=sys.stderr)

    print(f"--- Finished processing gene: {gene_name} ---")


def main():
    # --- Configuration ---
    CORE_GENES_ALIGNED_BASE_DIR = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/core_aflx_genes_aligned"
    INDIVIDUAL_GENE_TREES_OUTPUT_DIR = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/concatenated_core_genes/phylogenetic_tree/core_individual_gene_trees"

    CORE_GENES = ["ver-1", "verA", "verB"]

    MAFFT_PATH = "mafft"
    IQ_TREE_PATH = "iqtree2" 

    BOOTSTRAP_REPLICATES = 1000
    NUM_THREADS = "AUTO" 

    print(f"Starting analysis for {len(CORE_GENES)} individual core genes.")
    os.makedirs(INDIVIDUAL_GENE_TREES_OUTPUT_DIR, exist_ok=True)

    for gene_name in CORE_GENES:
        gene_source_dir = os.path.join(CORE_GENES_ALIGNED_BASE_DIR, gene_name)
        
        if not os.path.exists(gene_source_dir):
            print(f"Error: Directory for gene '{gene_name}' not found at '{gene_source_dir}'. Skipping this gene.", file=sys.stderr)
            continue

        run_single_gene_phylogeny(
            gene_source_dir,
            INDIVIDUAL_GENE_TREES_OUTPUT_DIR,
            gene_name,
            mafft_path=MAFFT_PATH,
            iqtree_path=IQ_TREE_PATH,
            bootstrap_reps=BOOTSTRAP_REPLICATES,
            threads=NUM_THREADS
        )
    
    print("\nAll individual core gene phylogenetic analyses complete.")

if __name__ == "__main__":
    main()
