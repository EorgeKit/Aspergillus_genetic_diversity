import os
import subprocess # For running external commands like MAFFT
import sys        # For printing errors to stderr
import tempfile   # For creating temporary files

def run_mafft_alignment(input_concat_dir, output_alignment_dir, alignment_filename="core_genes_aligned.fasta", mafft_path="mafft"):
    """
    Performs multiple sequence alignment on all concatenated FASTA files using MAFFT.

    Args:
        input_concat_dir (str): Directory containing individual concatenated FASTA files
                                (e.g., /mnt/lustre/.../concatenated_core_genes).
        output_alignment_dir (str): Directory where the final aligned FASTA file will be saved.
        alignment_filename (str): Name of the output alignment file (e.g., "core_genes_aligned.fasta").
        mafft_path (str): Path to the MAFFT executable. Assumes 'mafft' is in PATH by default.
                          Specify full path if not (e.g., '/usr/local/bin/mafft').
    """
    print(f"Starting MAFFT alignment from files in: {input_concat_dir}")
    print(f"Alignment output will be saved to: {output_alignment_dir}/{alignment_filename}")

    # 1. Create output directory if it doesn't exist
    os.makedirs(output_alignment_dir, exist_ok=True)
    print(f"Ensured output directory '{output_alignment_dir}' exists.")

    # 2. Collect all concatenated FASTA files
    input_fasta_files = []
    for fname in os.listdir(input_concat_dir):
        if fname.endswith(".fasta") or fname.endswith(".fa"):
            input_fasta_files.append(os.path.join(input_concat_dir, fname))
    
    if not input_fasta_files:
        print(f"Error: No FASTA files found in '{input_concat_dir}'. Please check the input path and file extensions.", file=sys.stderr)
        return

    print(f"Found {len(input_fasta_files)} concatenated FASTA files to align.")

    # 3. Read all sequences into a single string for MAFFT input
    # MAFFT typically takes a single input file containing all sequences
    mafft_input_content = ""
    for fasta_file in input_fasta_files:
        try:
            with open(fasta_file, 'r') as f:
                mafft_input_content += f.read() + "\n" # Add newline to ensure separation
        except Exception as e:
            print(f"Error reading {fasta_file}: {e}", file=sys.stderr)
            return # Exit if a file can't be read

    if not mafft_input_content.strip():
        print("Error: Collected sequences are empty. Cannot perform alignment.", file=sys.stderr)
        return

    # 4. Create a temporary input file for MAFFT
    # tempfile.NamedTemporaryFile ensures unique filenames and handles cleanup
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".fasta") as temp_in_fasta:
        temp_in_fasta.write(mafft_input_content)
        temp_input_path = temp_in_fasta.name
    print(f"Created temporary MAFFT input file: {temp_input_path}")

    # 5. Define the output alignment file path
    output_alignment_path = os.path.join(output_alignment_dir, alignment_filename)

    # 6. Construct the MAFFT command
    # Using '--auto' for automatic algorithm selection, which is generally good.
    # You can customize MAFFT options here if needed (e.g., --localpair, --genafpair)
    mafft_command = [
        mafft_path,
        "--auto", # MAFFT automatically selects the best algorithm for the data size
        temp_input_path
    ]
    print(f"Executing MAFFT command: {' '.join(mafft_command)}")

    # 7. Execute MAFFT
    try:
        # We redirect stdout to a file and capture stderr
        with open(output_alignment_path, 'w') as outfile:
            process = subprocess.run(
                mafft_command,
                stdout=outfile,       # Redirect MAFFT's standard output to our output file
                stderr=subprocess.PIPE, # Capture MAFFT's standard error
                check=True,           # Raise an exception if the command returns a non-zero exit code
                text=True             # Capture stderr as text
            )
        print(f"MAFFT alignment successful. Output saved to: {output_alignment_path}")
        if process.stderr:
            print(f"MAFFT stderr (may contain warnings/info): \n{process.stderr}", file=sys.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Error during MAFFT execution. Command '{e.cmd}' returned non-zero exit status {e.returncode}.", file=sys.stderr)
        print(f"MAFFT stderr: \n{e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: MAFFT executable not found. Please ensure '{mafft_path}' is correct and MAFFT is installed and in your system's PATH.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during MAFFT alignment: {e}", file=sys.stderr)
    finally:
        # 8. Clean up the temporary input file
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)
            print(f"Cleaned up temporary file: {temp_input_path}")

    print("\nMAFFT alignment script finished.")

if __name__ == "__main__":
    # Define the directory containing your concatenated FASTA files
    INPUT_CONCAT_DIR = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/core_aflx_genes_aligned/concatenated_core_genes"

    # Define the directory where the final aligned FASTA will be saved
    OUTPUT_ALIGNMENT_DIR = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/extracted_algnd_aflx_genes/core_aflx_genes_aligned/concatenated_core_genes/aligned_core_genes"
    
    # Define the name for the output alignment file
    ALIGNMENT_FILENAME = "core_genes_mafft_aligned.fasta"

    # Define the path to the MAFFT executable.
    # If 'mafft' is in your system's PATH, you can leave it as "mafft".
    # Otherwise, specify the full path, e.g., MAFFT_PATH = "/usr/local/bin/mafft"
    MAFFT_PATH = "mafft" 

    run_mafft_alignment(INPUT_CONCAT_DIR, OUTPUT_ALIGNMENT_DIR, ALIGNMENT_FILENAME, MAFFT_PATH)
