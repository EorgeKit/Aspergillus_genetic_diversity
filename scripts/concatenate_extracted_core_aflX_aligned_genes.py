import os
import re # Import re for regular expressions
import sys # Import sys for stderr output

def concatenate_core_genes(core_genes_base_dir, output_concat_dir, core_genes_order):
    """
    Concatenates FASTA sequences of core genes for each isolate in a defined order.
    The output is one FASTA file per isolate, containing all its core gene sequences
    joined together.

    Args:
        core_genes_base_dir (str): The directory containing subdirectories for each core gene,
                                   where each gene directory holds FASTA files for all isolates.
                                   (e.g., /mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/core_aflx_genes_aligned)
        output_concat_dir (str): The directory where the concatenated FASTA files will be stored.
                                 (e.g., /mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/core_aflx_genes_aligned/concatenated_core_genes)
        core_genes_order (list): A list of gene names defining the exact order in which
                                 their sequences should be concatenated for each isolate.
    """
    print(f"Starting concatenation of core gene sequences from: {core_genes_base_dir}")
    print(f"Concatenated FASTA files will be stored in: {output_concat_dir}")

    # Create the output directory for concatenated files if it doesn't exist
    os.makedirs(output_concat_dir, exist_ok=True)
    print(f"Ensured output directory '{output_concat_dir}' exists.")

    # Get a list of all isolates by looking into the first core gene's directory
    # Assumes that each core gene directory contains files for all isolates.
    if not core_genes_order:
        print("Error: The core_genes_order list is empty. Cannot concatenate.", file=sys.stderr)
        return

    first_gene_dir = os.path.join(core_genes_base_dir, core_genes_order[0])
    if not os.path.exists(first_gene_dir):
        print(f"Error: The first core gene directory '{first_gene_dir}' does not exist.", file=sys.stderr)
        return

    # Extract isolate names from the filenames in the first gene's directory
    # Example filename: Extracted_adhA_short_chain_alcohol_dehydrogenase_10B.fa
    isolate_names = set()
    for fname in os.listdir(first_gene_dir):
        match = re.search(r'_([0-9A-Za-z]+)\.fa$', fname) # Regex to capture isolate ID before .fa
        if match:
            isolate_names.add(match.group(1))

    if not isolate_names:
        print(f"Warning: No isolate names found in '{first_gene_dir}'. Please check file naming convention.", file=sys.stderr)
        return
    
    # Convert set to sorted list for consistent processing order
    isolate_names = sorted(list(isolate_names)) 
    print(f"Found {len(isolate_names)} isolates: {', '.join(isolate_names)}")

    # Iterate through each isolate to build its concatenated sequence
    for isolate_name in isolate_names:
        concatenated_sequence = ""
        missing_genes_for_isolate = []

        print(f"Processing isolate: {isolate_name}")
        # Iterate through the core genes in the specified order
        for gene_name in core_genes_order:
            gene_dir = os.path.join(core_genes_base_dir, gene_name)
            
            # Find the specific FASTA file for this gene and isolate
            gene_fasta_file = None
            for fname in os.listdir(gene_dir):
                if fname.startswith(f"Extracted_{gene_name}_") and fname.endswith(f"_{isolate_name}.fa"):
                    gene_fasta_file = os.path.join(gene_dir, fname)
                    break

            if gene_fasta_file and os.path.exists(gene_fasta_file):
                try:
                    # Read sequence from FASTA file
                    with open(gene_fasta_file, 'r') as f:
                        lines = f.readlines()
                        # Assuming sequence starts from the second line (after header)
                        # and may be split across multiple lines
                        sequence = "".join([line.strip() for line in lines if not line.startswith('>')])
                        concatenated_sequence += sequence
                except Exception as e:
                    print(f"Error reading sequence from {gene_fasta_file}: {e}", file=sys.stderr)
                    # If an error occurs, consider adding placeholder Ns or skipping,
                    # depending on desired alignment behavior. For now, proceed.
                    missing_genes_for_isolate.append(gene_name) # Mark as effectively missing due to error
            else:
                # This should ideally not happen if genes are truly "core" and files are present
                missing_genes_for_isolate.append(gene_name)
                print(f"Warning: Core gene '{gene_name}' FASTA for isolate '{isolate_name}' not found at {gene_fasta_file}. This gene will be skipped for this isolate.", file=sys.stderr)

        # Write the concatenated sequence for the current isolate to an output FASTA file
        if concatenated_sequence: # Only write if we actually got some sequence
            output_fasta_filename = f"concatenated_{isolate_name}_core_genes.fasta"
            output_fasta_path = os.path.join(output_concat_dir, output_fasta_filename)
            
            with open(output_fasta_path, 'w') as out_f:
                out_f.write(f">{isolate_name}\n")
                # Add a note if genes were missing (optional but good for debugging)
                if missing_genes_for_isolate:
                    out_f.write(f"# WARNING: Missing genes for {isolate_name}: {', '.join(missing_genes_for_isolate)}\n")
                out_f.write(concatenated_sequence + "\n")
            print(f"Successfully created: {output_fasta_filename}")
        else:
            print(f"Error: No sequence could be concatenated for isolate {isolate_name}. Skipping output file.", file=sys.stderr)

    print("\nConcatenation complete. Files are ready for alignment.")

if __name__ == "__main__":
    # Define your source directory where core genes are organized
    CORE_GENES_BASE_DIR = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/core_aflx_genes_aligned"
    
    # Define the output directory for the concatenated FASTA files
    OUTPUT_CONCAT_DIR = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/core_aflx_genes_aligned/concatenated_core_genes"

    # Define the 16 core genes in the exact order for concatenation.
    # This order is crucial for downstream alignment and phylogenetic analysis.
    CORE_GENES_ORDER = [
        "adhA", "aflJ", "avfA", "avnA", "cypX", "estA", "moxY", "norA",
        "omtA", "omtB", "ordA", "ordB", "vbs", "ver-1", "verA", "verB"
    ]

    concatenate_core_genes(CORE_GENES_BASE_DIR, OUTPUT_CONCAT_DIR, CORE_GENES_ORDER)
