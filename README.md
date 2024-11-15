## README.md

# Video File Renamer

This project is a Python-based tool designed to rename video files within subdirectories to follow the `SXXEXX` format, which is commonly used by media servers like Plex. The tool parses video file information, determines the new name based on the season and episode numbers, and renames the files accordingly.

## Features

- Parses video file information including season (from the directory of the file), episode number, and episode name.
- Renames video files to follow the `SXXEXX` format.
- Supports various video file types such as `.mp4`, `.mkv`, `.wmv`, and more.
- Provides a command-line interface (CLI) for easy usage.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/BelardoA/RenameTool
    cd RenameTool
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Please Note

The path to the files must be structured as `/path/to/show`. Within `/path/to/show`, there should be season folders containing the video files. The season folder names are used to number the episodes. Using the following structure:
```shell
tree /path/to/show
├── Season 01
│   ├── episode1.mp4
│   ├── episode2.mkv
│   └── episode3.wmv
├── Season 02
│   ├── episode4.mp4
│   ├── episode5.mkv
│   └── episode6.wmv
└── Season 03
    ├── episode7.mp4
    ├── episode8.mkv
    └── episode9.wmv
```

### Command-Line Interface

The tool provides a CLI for renaming video files. Use the following command to rename files within a specified root directory:

```sh
python rename_tool/main.py rename_from_root --root <path-to-root-directory>
```

You will be prompted to enter the directory if not provided.

### Example

```sh
python rename_tool/main.py rename_from_root --root /path/to/video/files
```

#### This would rename the files to the following format:

```shell
tree /path/to/show
├── Season 01
│   ├── episode1.mp4  -->  S01E01.mp4
│   ├── episode2.mkv  -->  S01E02.mkv
│   └── episode3.wmv  -->  S01E03.wmv
├── Season 02
│   ├── episode4.mp4  -->  S02E01.mp4
│   ├── episode5.mkv  -->  S02E02.mkv
│   └── episode6.wmv  -->  S02E03.wmv
└── Season 03
    ├── episode7.mp4  -->  S03E01.mp4
    ├── episode8.mkv  -->  S03E02.mkv
    └── episode9.wmv  -->  S03E03.wmv
```

## Approach

1. **VideoFile Class**: A Pydantic model that represents a video file with attributes such as season, episode, file path, and new name. It includes a method to determine the new name based on the season and episode numbers.

2. **Functions**:
    - `parse_episode_number_and_name`: Parses the episode number and name from the file name using regular expressions.
    - `get_video_files`: Retrieves video files from the specified directory, organizes them by season, and creates `VideoFile` instances.
    - `rename_files`: Renames the video files based on the new name determined by the `VideoFile` class.

3. **CLI**: Uses the `click` library to create a command-line interface for renaming video files. The `rename_from_root` command walks through the provided root directory and renames all video files within the season sub-folders.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.