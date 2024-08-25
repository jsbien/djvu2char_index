# -*- coding: utf-8 -*-
import csv
import re
import sys
import os

def parse_dsed_file(dsed_file):
    with open(dsed_file, 'r') as file:
        content = file.read()
    
    # Extract document name
    document_name = re.search(r"select\s*'(.+?)'", content).group(1)
    
    # Initialize counters
    page_count = 0
    column_count = 0
    paragraph_count = 0
    line_count = 0
    word_count = 0
    char_count = 0
    
    # Prepare CSV output file
    base_name = os.path.basename(document_name)
    output_csv = base_name.replace('.djvu', '.csv')
    
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        
        # Extract all char elements
        chars = re.findall(r"\(char\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+\"(.+?)\"\)", content)
        
        for char in chars:
            x_min, y_min, x_max, y_max, character = char
            
            # Update counters based on position in hierarchy
            # (Assuming hierarchy parsing logic will be handled here)
            # This is a simplified assumption for now
            
            char_count += 1
            
            # Convert coordinates for djview4
            width = int(x_max) - int(x_min)
            height = int(y_max) - int(y_min)
            
            highlight = f"{x_min},{y_min},{width},{height}"
            
            # Create URL for djview4
            url = f"file:{base_name}?djvuopts=&page={page_count+1}&highlight={highlight}"
            
            # Create description of the character position
            description = f"p {page_count+1} c {column_count+1} pa {paragraph_count+1} l {line_count+1} w {word_count+1} c {char_count}"
            
            # Write to CSV
            csv_writer.writerow([character, url, description, f" ※ {base_name}"])
    
    print(f"CSV file '{output_csv}' has been created.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python djvu2char_index.py <path_to_dsed_file>")
        sys.exit(1)
    
    dsed_file_path = sys.argv[1]
    
    if not os.path.isfile(dsed_file_path):
        print(f"Error: File '{dsed_file_path}' not found.")
        sys.exit(1)
    
    parse_dsed_file(dsed_file_path)
