import os
from Bio import Entrez, SeqIO

# Set your email
Entrez.email = "georgekitundu2@gmail.com"  # Your email

# List of accession numbers
accession_numbers = [
    "AF391094",  # fas-2 (hexA)
    "AF391094",  # fas-1 (hexB)
    "Z47198",    # pksA
    "L27801",    # nor-1
    "U24698",    # norA, aad
    "U32377",    # adh-2 in A. flavus
    "U62774",    # avnA
    "L40839",    # ord-1
    "U76621",    # adhA
    "AF154050",  # avfA
    "L40840",    # ord-2
    "AF159789",  # (AF159789 in A. flavus)
    "AF417002",  # estA
    "AF169016",  # vbs
    "U51327",    # vbs
    "AF106958",  # verB
    "AF106959",  # (AF106959 in A. flavus)
    "AF106960",  # (AF106960 in A. flavus)
    "M91369",    # ver-1
    "HM355067",  # verA
    "XM_033560158", #hypA
    "DQ390844",   #ordB
    "AB022905",  # dmtA (mt-I)
    "AB022906",  # dmtA (mt-I)
    "AF154050",  # omtB
    "AF159789",  # (AF159789 in A. flavus)
    "L25834",    # omtA
    "L22091",    # omt-1 cDNA
    "L25836",    # (L25836 in A. flavus)
    "AF017151",  # ordA
    "AF169016",  # ordA
    "U81806",    # A. flavus ord-1
    "U81807",    # A. flavus ord-1
    "L26222",    # aflR
    "L22177",    # apa-2
    "AF427616",  # afl-2
    "AF441429",  # afl-2
    "AF002660",  # aflJ
    "AF077975",  # (AF077975 in A. flavus)
    "AF268071",  # aflT
    "AF169016",  # cypX
    "AF169016",  # moxY
    "AF452809",  # aflR2
    "AF452809",  # aflJ2
    "AF452809",  # adhA2
    "AF452809",  # estA2
    "AF452809",  # norA2
    "AF452809",  # ver-1B
    "AY510455.1",  # Aspergillus flavus isolate AF36 aflatoxin biosynthesis gene cluster
    "AY510451.1"   # Aspergillus flavus isolate AF13 aflatoxin biosynthesis gene cluster
]

# Set the output directory
output_dir = "/mnt/lustre/users/maloo/allan_project/allan-George/data/aflatoxin_gene_clusters"  # Change this to your desired output directory

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Download sequences
for accession in accession_numbers:
    try:
        handle = Entrez.efetch(db="nucleotide", id=accession, rettype="fasta", retmode="text")
        sequence_data = handle.read()
        handle.close()
        
        # Save the sequence to a file in the output directory
        with open(os.path.join(output_dir, f"{accession}.fasta"), "w") as output_file:
            output_file.write(sequence_data)
        
        print(f"Downloaded {accession} successfully")
    
    except Exception as e:
        print(f"Error downloading {accession}: {e}")

print("All downloads completed.")