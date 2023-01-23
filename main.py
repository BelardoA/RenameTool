#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Python script to rename files within subdirectories with SXXEXX prefix for plex"""

# standard python imports
import click
from path import Path
from rich.console import Console

# start Console object for pretty output in console
console = Console()


# create click group for commands
@click.group()
def cli():
    """Welcome to the Rename CLI tool!"""


# add command to rename files within the provided directory
@click.command("rename_from_root")
@click.option(
    "--root",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path),
    help="Provide the directory to the path that has all of the seasons separated.",
    prompt="Enter the directory",
    required=True,
)
def rename_from_root(root: Path) -> None:
    """
    Function to rename all files within the sub-folders in
    the provided root path to have a SXXEXX prefix
    :param Path root:
    :return: None
    """


if __name__ == "__main__":
    print("We made it.")
