import pandas as pd
from scipy.spatial.distance import pdist, squareform

def calculate_jaccard_distance(matrix_file):
    """
    Calculate the Jaccard distance matrix for a gene presence/absence matrix.

    Args:
        matrix_file (str): Path to the CSV file containing the gene presence/absence matrix.

    Returns:
        pd.DataFrame: A DataFrame containing the Jaccard distance matrix.
    """
    # Load the gene presence/absence matrix
    data = pd.read_csv(matrix_file, index_col=0)

    # Ensure the data is binary (0s and 1s)
    if not ((data == 0) | (data == 1)).all().all():
        raise ValueError("The matrix must contain only binary values (0 or 1).")

    # Calculate pairwise Jaccard distances
    distances = pdist(data.values, metric="jaccard")

    # Convert the distances into a square matrix
    distance_matrix = squareform(distances)

    # Create a DataFrame for better readability
    distance_df = pd.DataFrame(
        distance_matrix, index=data.index, columns=data.index
    )

    return distance_df


if __name__ == "__main__":
    # Example usage
    matrix_file = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/aflx_diversity/presence_absence_matrix.csv"  # Replace with your file path
    distance_matrix = calculate_jaccard_distance(matrix_file)

    # Save the distance matrix to a CSV file
    output_file = "/mnt/lustre/users/maloo/allan_project/allan-George/analysis/aflx_diversity/jaccard_distance_matrix.csv"
    distance_matrix.to_csv(output_file)

    print(f"Jaccard distance matrix saved to {output_file}")