import os
import sys
import shutil
import git

def collect_project_files(output_file="project_contents.txt", project_dir=None, include_hidden=False):
    """
    Collects all the files with specified extensions (.py, .txt, .json, .md) from the current directory (or a specified directory)
    and copies their contents into a single .txt file. Configuration files like `requirements.txt` are highlighted in a separate section.
    
    Parameters:
    output_file (str): The name of the output file that will store the collected project contents.
    project_dir (str): The directory of the project to collect files from. If None, uses the current directory.
    include_hidden (bool): Whether to include hidden files and directories.
    """
    sys_prompt = "# System: You are a helpful assistant. The following content is project-related information that should be used to assist in development.\n\n"

    config_files = ['requirements.txt', 'settings.json', 'config.yaml', 'hyperparameters.json']  # Add your config files here
    file_extensions = ['.py', '.txt', '.json', '.md']  # File extensions to include

    if project_dir:
        current_directory = os.path.basename(project_dir)  # Get the final directory name of the cloned repo
    else:
        current_directory = os.path.basename(os.getcwd())  # Get the final directory name
    
    with open(output_file, 'w') as f_out:  # Open the output file for writing
        f_out.write(sys_prompt)  # Write the system prompt
        f_out.write(f"# This is the project file for '{current_directory}'\n\n")  # Write project file header

        # Section for Configuration Files
        f_out.write("# ---- CONFIGURATION FILES ----\n\n")  # Write the CONFIGURATION marker

        for root, dirs, files in os.walk(project_dir or os.getcwd()):  # Walk through all directories and files
            # If not including hidden files, filter out hidden directories
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]  # Exclude hidden directories
            
            for file_name in files:
                _, file_extension = os.path.splitext(file_name)  # Get the file extension
                
                # Check if the file is a configuration file
                if file_name in config_files:
                    file_path = os.path.join(root, file_name)  # Get the full file path

                    # Write the BEGIN marker for configuration files
                    f_out.write(f"# ---- BEGIN {file_name} ----\n")

                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_in:  # Open and read config file
                        f_out.write(f_in.read())  # Write file contents

                    # Write the END marker for configuration files
                    f_out.write(f"\n# ---- END {file_name} ----\n\n")

        # Section for Project Files (non-config)
        f_out.write("# ---- PROJECT FILES ----\n\n")  # Write a separator for other project files

        for root, dirs, files in os.walk(project_dir or os.getcwd()):  # Walk through all directories and files
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]  # Exclude hidden directories
            
            for file_name in files:
                _, file_extension = os.path.splitext(file_name)  # Get the file extension

                # If it's not a config file but has a valid extension, include it in project files
                if file_extension in file_extensions and file_name not in config_files:
                    file_path = os.path.join(root, file_name)  # Get the full file path

                    # Write the BEGIN marker for project files
                    f_out.write(f"# ---- BEGIN {file_name} ----\n")

                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_in:  # Open and read project file
                        f_out.write(f_in.read())  # Write file contents

                    # Write the END marker for project files
                    f_out.write(f"\n# ---- END {file_name} ----\n\n")

    print(f"All project files and configuration files have been copied into '{output_file}' with clear delineation markers.")  # Confirmation message


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
