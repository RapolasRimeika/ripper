import os
import sys
import shutil
import git
from settings import SYSTEM_PROMPT, CONFIG_FILES, FILE_EXTENSIONS


def collect_project_files(project_dir=None, include_hidden=False):
    """
    Collects all the files with specified extensions (.py, .txt, .json, .md) from the current directory (or a specified directory)
    and copies their contents into a single .txt file. The output file is named after the project directory with '_ripped.txt' appended.
    Configuration files like `requirements.txt` are highlighted in a separate section.
    
    Parameters:
    project_dir (str): The directory of the project to collect files from. If None, uses the current directory.
    include_hidden (bool): Whether to include hidden files and directories.
    """
    # Determine the name of the project directory or repository
    current_directory = os.path.basename(project_dir) if project_dir else os.path.basename(os.getcwd())
    
    # Define the output file name
    output_file = f"{current_directory}_ripped.txt"
    
    with open(output_file, 'w') as f_out:
        f_out.write(SYSTEM_PROMPT)  # Write the system prompt from settings.py
        f_out.write(f"# This is the project file for '{current_directory}'\n\n")  # Write project file header
        
        # Section for Configuration Files
        f_out.write("# ---- CONFIGURATION FILES ----\n\n")
        for root, dirs, files in os.walk(project_dir or os.getcwd()):
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]  # Exclude hidden directories
            for file_name in files:
                _, file_extension = os.path.splitext(file_name)
                if file_name in CONFIG_FILES:
                    file_path = os.path.join(root, file_name)
                    f_out.write(f"# ---- BEGIN {file_name} ----\n")
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_in:
                        f_out.write(f_in.read())
                    f_out.write(f"\n# ---- END {file_name} ----\n\n")

        # Section for Project Files (non-config)
        f_out.write("# ---- PROJECT FILES ----\n\n")
        for root, dirs, files in os.walk(project_dir or os.getcwd()):
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file_name in files:
                _, file_extension = os.path.splitext(file_name)
                if file_extension in FILE_EXTENSIONS and file_name not in CONFIG_FILES:
                    file_path = os.path.join(root, file_name)
                    f_out.write(f"# ---- BEGIN {file_name} ----\n")
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_in:
                        f_out.write(f_in.read())
                    f_out.write(f"\n# ---- END {file_name} ----\n\n")

    print(f"All project files and configuration files have been copied into '{output_file}' with clear delineation markers.")


def clone_and_collect_files(github_url, include_hidden=False):
    """
    Clones a GitHub repository and uses the collect_project_files() function to collect the project files.
    
    Parameters:
    github_url (str): The URL of the GitHub repository to clone.
    include_hidden (bool): Whether to include hidden files and directories.
    """
    # Extract the repository name from the GitHub URL
    repo_name = github_url.split('/')[-1].replace('.git', '')
    
    # Clone the repository
    if os.path.exists(repo_name):
        shutil.rmtree(repo_name)  # Remove the directory if it already exists to avoid conflicts
    git.Repo.clone_from(github_url, repo_name)
    
    print(f"Cloned repository '{repo_name}' from {github_url}")
    
    # Collect project files from the cloned repository
    collect_project_files(project_dir=repo_name, include_hidden=include_hidden)
    
    # Optionally remove the cloned directory after processing
    shutil.rmtree(repo_name)
    print(f"Removed the cloned repository '{repo_name}' after processing")


# Main script logic for handling flags
if __name__ == "__main__":
    include_hidden = '-a' in sys.argv  # Check for the -a flag

    if len(sys.argv) > 1 and sys.argv[1] == '-github' and len(sys.argv) > 2:
        github_url = sys.argv[2]
        clone_and_collect_files(github_url, include_hidden=include_hidden)
    else:
        collect_project_files(include_hidden=include_hidden)
