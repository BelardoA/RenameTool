#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Python script to rename files within subdirectories with SXXEXX prefix for plex"""

# standard python imports
import click
from path import Path
from rich.console import Console
from functions import get_video_files, rename_files

# start Console object for pretty output in console
console = Console()


# create click group for commands
@click.group()
def cli():
    """Welcome to the Rename CLI tool!"""


# add command to rename files within the provided directory
@cli.command("rename_from_root")
@click.option(
    "--root",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path),
    help="Provide the directory to the path that has all of the seasons separated.",
    prompt="Enter the directory",
    required=True,
)
def rename_from_root(root: Path) -> None:
    """Walks the provided root directory and renames all video files within the season sub-folders to match
    SXXEXX format."""
    _rename_from_root(root)


def _rename_from_root(root: Path) -> None:
    """
    Function to rename all files within the sub-folders in the provided root path to have a SXXEXX prefix

    :param Path root: Directory path to the root directory containing season sub-folders
    :return: None
    """
    # get the video files that need to be renamed
    videos = get_video_files(root)

    # rename the files while storing the # of files renamed
    rename_counter = rename_files(videos)

    console.print(f"[green] Renamed {rename_counter} files in {root}")


if __name__ == "__main__":
    cli()
