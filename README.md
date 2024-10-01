## About

I created this tool to quickly aggregate the contents of my projects and get feedback on them from an LLM (Large Language Model). The script features a GitHub cloning function, which is especially useful when you don't want to load the entire project locally. It also avoids hidden files, like dependencies in virtual environments, by default.

### Caution

Be mindful of how you use this tool, especially when working with licensed projects. Always ensure that you're following the proper licensing terms when aggregating or sharing project files.

This is a quick tool I built to streamline my workflow and improve the way I manage my projects.


# Project File Collector

This Python script allows you to collect and aggregate the contents of specific file types from a local directory or a GitHub repository. The script supports the following features: Collects files with extensions `.py`, `.txt`, `.json`, and `.md` by default. Clones a GitHub repository and gathers the specified project files. By default, hidden files and directories are ignored, but they can be included using the `-a` flag. The output is written to a single `.txt` file that combines the contents of the collected files.

## Features

- Local file collection: Gathers project files from the current directory or a specified project directory.
- GitHub repository cloning: Clones a GitHub repository and collects the project files from it.
- Customizable inclusion of hidden files: Option to include hidden files and directories using the `-a` flag.
- Output aggregation: The collected file contents are written to a single `.txt` file.
- System prompt integration: Uses a custom system prompt from the `settings.py` file.
- Configurable via `settings.py`: The system prompt, included file types, and configuration files are defined in the `settings.py` file.


## Requirements

- Python 3.x
- GitPython package (for cloning repositories)

To install `GitPython`, run: `pip install gitpython`.

## Usage

### Collecting files from the current directory

To collect files from the current working directory and ignore hidden files, run:

```bash
python ripper.py
```

To collect files and include hidden files and directories, run:

```bash
python ripper.py -a
```

### Cloning a GitHub repository and collecting files

To clone a GitHub repository, collect project files, and ignore hidden files, run:

```bash
python ripper.py -github https://github.com/username/repo.git
```

To include hidden files from the cloned repository, run:

```bash
python ripper.py -github https://github.com/username/repo.git -a
```

## Parameters

- `output_file` (optional): The name of the file where the collected contents will be saved. Defaults to `project_contents.txt`.
- `project_dir` (optional): The directory to collect files from. If not specified, the script uses the current working directory.
- `-a` flag (optional): Include hidden files and directories.

## Example

1. **Local collection without hidden files**: `python3 ripper.py`. This will collect all `.py`, `.txt`, `.json`, and `.md` files from the current directory, excluding hidden files, and store the combined contents in `project_contents.txt`.

2. **Cloning a repository and including hidden files**: `python3 ripper.py -github https://github.com/username/repo.git -a`. This will clone the specified GitHub repository, collect all `.py`, `.txt`, `.json`, and `.md` files (including hidden files), and store them in `project_contents.txt`.

## How It Works

1. **Local Collection**: The script walks through the directory tree starting from the specified directory (or current directory if none is specified). It checks each file’s extension to see if it matches the specified types (`.py`, `.txt`, `.json`, `.md`). It writes the contents of each matching file into a single `.txt` file, separating each file with a header.

2. **GitHub Cloning**: The script clones the specified repository into a local directory. After cloning, it follows the same process as local collection to gather project files. Once the collection is done, the cloned repository is removed.

## License

This project is licensed under the MIT License.

## Getting Started

Follow these steps to set up and use the Ripper script:

### 1. Clone the Repository

Start by cloning this repository to your local machine:

```bash
git clone https://github.com/RapolasRimeika/ripper.git
cd ripper
```

### 2. Install Dependencies

Next, install the required dependencies using `pip`. You only need to install `GitPython` as it’s the only external library:

```bash
pip install -r requirements.txt
```

### 3. Create an Alias for Faster Usage

To streamline the use of this script, you can create an alias so that you can run it from anywhere without typing the full path. To do this, add the following line to your shell configuration file (e.g., `.bashrc`, `.bash_profile`, or `.zshrc` depending on your shell):

```bash
alias ripper="python /path/to/ripper/ripper.py"
```

Make sure to replace `/path/to/ripper/` with the actual path where you cloned the repository. After saving the file, apply the changes by running:

```bash
source ~/.bashrc  # or ~/.zshrc depending on your shell
```

### 4. Usage Example

Now, you can use the script from anywhere on your system by simply typing:

```bash
ripper
```

To include hidden files or clone a GitHub repository, just add the appropriate flags and parameters:

```bash
ripper -a
ripper -github https://github.com/username/repo.git
```
