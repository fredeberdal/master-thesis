import os
import shutil
from tabulate import tabulate

def is_code_file(filename):
    """
    Determine if file is a code file based on extension.
    """
    code_extensions = ('.py', '.js', '.ts', '.html', '.tsx', '.jsx')
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff') 
    return filename.endswith(code_extensions) and not filename.endswith(image_extensions)

def search_keyword_in_file(file_path, keywords):
    """
    Search for keywords in a file and count their occurrences.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            return sum(contents.count(keyword) for keyword in keywords)
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return 0
    except Exception as e:
        print(f"An error occurred while trying to read {file_path}: {e}")
        return 0

def search_keyword_in_folder(folder_path, keywords, relevant_files_folder):
    """
    Search for keywords in all files in the specified folder and copy relevant files to another folder.
    """
    if not os.path.exists(relevant_files_folder):
        os.makedirs(relevant_files_folder)

    selected_files = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if not is_code_file(filename):
                continue

            file_path = os.path.join(root, filename)
            keyword_count = search_keyword_in_file(file_path, keywords)
            if keyword_count > 0:
                print(f"------Found keywords {keyword_count} times in {file_path}. Copying to {relevant_files_folder}.")
                relative_path = os.path.relpath(file_path, folder_path)
                target_subfolder = os.path.join(relevant_files_folder, os.path.dirname(relative_path))
                if not os.path.exists(target_subfolder):
                    os.makedirs(target_subfolder)
                shutil.copy(file_path, os.path.join(target_subfolder, os.path.basename(file_path)))
                selected_files.append([relative_path, keyword_count])
            else:
                print(f"No keywords found in {file_path}.")

    # Sort by keyword occurrences
    selected_files = sorted(selected_files, key=lambda x: x[1], reverse=True)

    # Print data in a table format
    if selected_files:
        print(tabulate(selected_files, headers=['File', 'Keywords'], tablefmt='grid'))

# Running function
source_path = "C:/Users/frede/OneDrive/Dokumenter/1Skole/Master/master_thesis/testprojects/control"
relevant_files_folder = 'C:/Users/frede/OneDrive/Dokumenter/1Skole/Master/master_thesis/keyword_chosen_files'
snippet = ("useNavigate", "useState", "useEffect")
search_keyword_in_folder(source_path, snippet, relevant_files_folder)
