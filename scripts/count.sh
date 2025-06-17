for file in *.fa; do
    # Calculate the total length of sequences in the current file
    length=$(grep -v "^>" "$file" | awk '{total += length($0)} END {print total}')
    echo "$file: $length"
done | tee lengths.txt

# Calculate the total length across all files
total_length=$(grep -v "^>" *.fa | awk '{total += length($0)} END {print total}')
echo "Total length: $total_length"