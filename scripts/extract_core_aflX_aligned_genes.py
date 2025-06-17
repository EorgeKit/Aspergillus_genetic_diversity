import os
import shutil
import sys 

def extract_core_genes(source_base_dir, output_base_dir, core_genes_list):
    """
    Extracts FASTA files for specified core genes from individual isolate directories
    and stores them in a new, organized core genes directory.

    Args:
        source_base_dir (str): The root directory containing isolate subdirectories.
                                (e.g., /mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes)
        output_base_dir (str): The directory where core genes will be organized.
                                (e.g., /mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/core_aflx_genes_aligned)
        core_genes_list (list): A list of gene names identified as core.
    """
    print(f"Starting core gene extraction from: {source_base_dir}")
    print(f"Core genes will be stored in: {output_base_dir}")

    # Create the main output directory if it doesn't exist
    os.makedirs(output_base_dir, exist_ok=True)
    print(f"Ensured output directory '{output_base_dir}' exists.")

    # Get the basename of the output directory for exclusion
    output_dir_basename = os.path.basename(output_base_dir)

    # Get list of all isolate directories, explicitly excluding the output directory if it's within source_base_dir
    isolate_dirs = []
    for d in os.listdir(source_base_dir):
        full_path = os.path.join(source_base_dir, d)
        if os.path.isdir(full_path) and d != output_dir_basename:
            isolate_dirs.append(d)
    
    if not isolate_dirs:
        print(f"Warning: No valid isolate subdirectories found in '{source_base_dir}'. Please check the path and structure, and ensure the output directory is not the only directory present.")
        return

    print(f"Found {len(isolate_dirs)} isolate directories: {', '.join(isolate_dirs)}")

    # Iterate through each core gene to create its dedicated folder and copy files
    for gene_name in core_genes_list:
        gene_output_dir = os.path.join(output_base_dir, gene_name)
        os.makedirs(gene_output_dir, exist_ok=True)
        print(f"Created directory for gene '{gene_name}': {gene_output_dir}")

        for isolate_name in isolate_dirs:
            isolate_gene_dir = os.path.join(source_base_dir, isolate_name)
            
            # Construct a pattern for the filename to find the correct file
            found_file = None
            for fname in os.listdir(isolate_gene_dir):
                # Using a more flexible check to avoid issues with potential minor variations
                # in the descriptive text within the filename.
                # The assumption is that the core gene name and isolate name are consistent.
                if fname.startswith(f"Extracted_{gene_name}_") and fname.endswith(f"_{isolate_name}.fa"):
                    found_file = fname
                    break # Found the correct file, move to next isolate

            if found_file:
                source_file_path = os.path.join(isolate_gene_dir, found_file)
                destination_file_path = os.path.join(gene_output_dir, found_file)
                
                try:
                    shutil.copy2(source_file_path, destination_file_path)
                    # print(f"Copied '{found_file}' to '{gene_output_dir}'") # Commented out to reduce verbose output
                except FileNotFoundError:
                    print(f"Error: Source file not found for {gene_name} in {isolate_name}: {source_file_path}", file=sys.stderr)
                except Exception as e:
                    print(f"Error copying file {source_file_path} to {destination_file_path}: {e}", file=sys.stderr)
            else:
                print(f"Warning: Core gene '{gene_name}' (expected: Extracted_{gene_name}_*_{isolate_name}.fa) not found for isolate '{isolate_name}' in '{isolate_gene_dir}'. This might indicate a discrepancy in core gene identification or file naming.", file=sys.stderr)
    
    print("\nCore gene extraction complete.")

if __name__ == "__main__":
    # Define your source and target directories
    SOURCE_BASE_DIR = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes"
    OUTPUT_BASE_DIR = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/core_aflx_genes_aligned"

    # Define the 16 core genes identified from your data
    CORE_GENES = [
        "adhA",
        "aflJ",
        "avfA",
        "avnA",
        "cypX",
        "estA",
        "moxY",
        "norA",
        "omtA",
        "omtB",
        "ordA",
        "ordB",
        "vbs",
        "ver-1",
        "verA",
        "verB"
    ]

    extract_core_genes(SOURCE_BASE_DIR, OUTPUT_BASE_DIR, CORE_GENES)
