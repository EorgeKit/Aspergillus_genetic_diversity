# A unified script for analyzing genomic diversity from a distance matrix.
# Combines hierarchical clustering and Principal Coordinates Analysis (PCoA).

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
from skbio.stats.ordination import pcoa
from skbio.stats.ordination import OrdinationResults
import argparse
import sys

def plot_hierarchical_clustering(distance_df: pd.DataFrame, linkage_method: str, output_file: str):
    """
    Performs hierarchical clustering and saves the resulting dendrogram.

    Args:
        distance_df (pd.DataFrame): A square DataFrame of pairwise distances.
        linkage_method (str): The linkage algorithm to use (e.g., 'average', 'complete', 'ward').
        output_file (str): Path to save the output plot.
    """
    print(f"Performing hierarchical clustering using '{linkage_method}' linkage...")
    # Convert the square-form distance matrix back into a condensed distance matrix
    # for efficiency with the linkage function.
    try:
        condensed_dist_matrix = squareform(distance_df)
    except ValueError as e:
        print(f"Error: The distance matrix is not a valid square matrix. {e}", file=sys.stderr)
        sys.exit(1)

    linkage_matrix = linkage(condensed_dist_matrix, method=linkage_method)

    # Plot the dendrogram
    plt.figure(figsize=(15, 9))
    dendrogram(
        linkage_matrix,
        labels=distance_df.index.tolist(),
        leaf_rotation=90,
        leaf_font_size=10,
    )

    # Customize and save the plot
    plt.title(f"Hierarchical Clustering Dendrogram ({linkage_method.capitalize()} Linkage)", fontsize=16)
    plt.ylabel("Jaccard Distance", fontsize=12)
    plt.xlabel("Isolates", fontsize=12)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close() # Close the plot to free up memory
    print(f"Dendrogram saved to {output_file}")

def plot_pcoa(distance_df: pd.DataFrame, output_file: str):
    """
    Performs PCoA and saves the resulting 2D scatter plot.

    Args:
        distance_df (pd.DataFrame): A square DataFrame of pairwise distances.
        output_file (str): Path to save the output plot.
    """
    print("Performing Principal Coordinates Analysis (PCoA)...")
    # Perform PCoA using scikit-bio, which correctly handles distance matrices
    # and provides proportion of variance explained.
    try:
        pcoa_results: OrdinationResults = pcoa(distance_df)
    except Exception as e:
        print(f"Error during PCoA calculation: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Extract coordinates and explained variance
    pcoa_coords = pcoa_results.samples
    prop_explained = pcoa_results.proportion_explained

    # Create the scatter plot
    plt.figure(figsize=(12, 10))
    sns.scatterplot(x='PC1', y='PC2', data=pcoa_coords, s=120, edgecolor='black', alpha=0.8)

    # Customize and save the plot
    plt.title("PCoA of Isolates (based on Gene Presence/Absence)", fontsize=16)
    plt.xlabel(f"PC1 ({prop_explained['PC1']:.2%})", fontsize=12)
    plt.ylabel(f"PC2 ({prop_explained['PC2']:.2%})", fontsize=12)
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)

    # Annotate points with isolate names for clarity
    for isolate_name, (pc1, pc2) in pcoa_coords.iterrows():
        plt.text(x=pc1 + 0.01, y=pc2, s=isolate_name, fontsize=9)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close() # Close the plot to free up memory
    print(f"PCoA plot saved to {output_file}")


def main():
    """Main function to parse arguments and run analyses."""
    parser = argparse.ArgumentParser(
        description="Analyze genomic diversity from a Jaccard distance matrix using Hierarchical Clustering and/or PCoA."
    )
    parser.add_argument(
        "distance_matrix_file",
        type=str,
        help="Path to the input CSV file containing the Jaccard distance matrix."
    )
    parser.add_argument(
        "--analysis",
        type=str,
        choices=['clustering', 'pcoa', 'both'],
        default='both',
        help="The type of analysis to perform. Default: both"
    )
    parser.add_argument(
        "--output_prefix",
        type=str,
        default="analysis_output",
        help="Prefix for the output plot files. Default: 'analysis_output'"
    )
    parser.add_argument(
        "--linkage_method",
        type=str,
        choices=['average', 'complete', 'single', 'ward'],
        default='average',
        help="Linkage method for hierarchical clustering. 'average' is UPGMA. Default: average"
    )
    
    args = parser.parse_args()

    # Load the distance matrix once
    try:
        distance_df = pd.read_csv(args.distance_matrix_file, index_col=0)
    except FileNotFoundError:
        print(f"Error: The file '{args.distance_matrix_file}' was not found.", file=sys.stderr)
        sys.exit(1)

    # Run the selected analysis
    if args.analysis in ['clustering', 'both']:
        output_file = f"{args.output_prefix}_dendrogram.png"
        plot_hierarchical_clustering(distance_df, args.linkage_method, output_file)

    if args.analysis in ['pcoa', 'both']:
        output_file = f"{args.output_prefix}_pcoa_plot.png"
        plot_pcoa(distance_df, output_file)
        
    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()