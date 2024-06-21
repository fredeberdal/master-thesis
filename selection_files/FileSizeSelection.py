import os
import shutil
from heapq import nlargest
from tabulate import tabulate  # Import the tabulate function

def is_code_file(filename):
    """
    Determine if file is a code file based on extension.
    """
    code_extensions = ('.py', '.js', '.ts', '.html', '.tsx', '.jsx')
    exclude_files = ('.env', 'tsconfig.json')
    exclude_patterns = ('.env.', 'node_modules')
    
    if filename.endswith(code_extensions) and not filename.endswith(exclude_files) and not any(filename.find(pattern) != -1 for pattern in exclude_patterns):
        return True
    return False

def find_largest_files_by_lines(folder_path, number_of_files, relevant_files_folder):
    """
    Find the code files with the most lines in the specified folder and copy them to another folder.
    """
    if not os.path.exists(relevant_files_folder):
        os.makedirs(relevant_files_folder)

    line_counts = []
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if 'node_modules' not in d]
        for filename in files:
            if is_code_file(filename):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        # Filter out empty lines, whitespace-only lines, and lines with only comments
                        lines = sum(1 for line in file if line.strip() and not line.strip().startswith(('#', '//')))
                    line_counts.append((lines, file_path))
                except Exception as e:
                    print(f"An error occurred while trying to read {file_path}: {e}")

    # Sort by number of lines
    largest_files = nlargest(number_of_files, line_counts, key=lambda x: x[0])

    # Print data in a table format
    table = [[os.path.relpath(path, folder_path), lines] for lines, path in largest_files]
    print(tabulate(table, headers=['File', 'Lines'], tablefmt="grid"))

    # Copying files to new location
    for lines, file_path in largest_files:
        relative_path = os.path.relpath(file_path, folder_path)
        destination_path = os.path.join(relevant_files_folder, relative_path)
        destination_dir = os.path.dirname(destination_path)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        shutil.copy(file_path, destination_path)
        print(f"Copying {file_path} ({lines} lines) to {destination_path}.")

# Running function
source_path = "C:/Users/frede/OneDrive/Dokumenter/1Skole/Master/master_thesis/testprojects/control"
relevant_files_folder = 'C:/Users/frede/OneDrive/Dokumenter/1Skole/Master/master_thesis/size_chosen_files'
find_largest_files_by_lines(source_path, 8, relevant_files_folder)
