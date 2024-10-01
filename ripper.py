import os
import sys
import shutil
import git

def collect_project_files(output_file="project_contents.txt", project_dir=None, include_hidden=False):
    """
    Collects all the files with specified extensions (.py, .txt, .json, .md) from the current directory (or a specified directory)
    and copies their contents into a single .txt file.
    
    Parameters:
    output_file (str): The name of the output file that will store the collected project contents.
    project_dir (str): The directory of the project to collect files from. If None, uses the current directory.
    include_hidden (bool): Whether to include hidden files and directories.
    """
    
    file_extensions = ['.py', '.txt', '.json', '.md']            # File extensions to include
    if project_dir:
        current_directory = os.path.basename(project_dir)        # Get the final directory name of the cloned repo
    else:
        current_directory = os.path.basename(os.getcwd())        # Get the final directory name
    
    with open(output_file, 'w') as f_out:                        # Open the output file for writing
        f_out.write(f"# This is the project file for '{current_directory}'\n\n")  # Write project file header

        for root, dirs, files in os.walk(project_dir or os.getcwd()):  # Walk through all directories and files
            
            # If not including hidden files, filter out hidden directories
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]  # Exclude hidden directories
            
            for file_name in files:
                # Ignore hidden files unless `include_hidden` is set to True
                if not include_hidden and file_name.startswith('.'):
                    continue
                
                _, file_extension = os.path.splitext(file_name)  # Get the file extension

                if file_extension in file_extensions:            # Check if the file has the desired extension
                    file_path = os.path.join(root, file_name)    # Get the full file path

                    f_out.write(f"# This is the {file_name}\n")  # Write file header (file name)

                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_in:  # Open and read file
                        f_out.write(f_in.read())                # Write file contents

                    f_out.write("\n\n")                         # Add space between files

    print(f"All project files have been copied into '{output_file}'")  # Confirmation message


def clone_and_collect_files(github_url, output_file="project_contents.txt", include_hidden=False):
    """
    Clones a GitHub repository and uses the collect_project_files() function to collect the project files.
    
    Parameters:
    github_url (str): The URL of the GitHub repository to clone.
    output_file (str): The name of the output file that will store the collected project contents.
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
    collect_project_files(output_file, project_dir=repo_name, include_hidden=include_hidden)
    
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
        collect_project_files(include_hidden=include_hidden)  # If no -github flag, just collect files from the current directory
