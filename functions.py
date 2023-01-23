#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Miscellaneous functions that are used in main.py """
import sys

# standard python imports
from pathlib import Path
import glob
import fnmatch
import os
import ntpath
from rich.console import Console

console = Console()


def get_file_type(file_name: str) -> str:
    """
    Function to get the file type of the provided file_path and returns it as a string
    :param str file_name: Path to the file
    :return: Returns string of file type
    :rtype: str
    """
    file_type = Path(file_name).suffix
    return file_type.lower()


def get_file_name(file_path: str) -> str:
    """
    Function to parse the provided file path and returns the file's name as a string
    :param str file_path: path to the file
    :return: File name
    :rtype: str
    """
    # split the provided file_path with ntpath
    directory, file_name = ntpath.split(file_path)
    # return the file_path or directory
    return file_name or ntpath.basename(directory)


def get_episode_number(episode_name: str) -> int:
    """
    Function to parse the provided episode_name for an episode number
    :param str episode_name: File name for the episode
    :return: The provided episode_name's episode #
    :rtype: int
    """
    # see if spaces are used in filename
    split_char = " " if episode_name.find(" ") > 0 else None

    if not split_char:
        # see if underscores are used
        split_char = "_" if episode_name.find("_") > 0 else None

    # split the provided file name at spaces
    if split_char:
        split_episode_name = episode_name.split(split_char)
        # iterate through the new list for the first integer
        for item in split_episode_name:
            # try to convert split string item to an integer
            try:
                episode_number = int(item)
                # means item is an integer, return it
                return episode_number
            except ValueError:
                # continue to the next item
                continue
    else:
        console.print(f"[red] Cannot parse episode number from {episode_name}")

def get_video_files(file_path: Path) -> list:
    """
    Function to go to the provided file_path and returns a list
    of all the files within the provided path
    :param Path file_path: Directory to get all files in
    :raises: General error if the provided file_path doesn't exist
    :return: list of files in the provided directory
    :rtype: list
    """
    # plex supported videos
    video_types = [".mp4", ".mkv", ".wmv", ".mpeg", ".mpegts", ".mov", ".avi", ".asf"]
    # file list of all plex supported video types
    file_list = []

    # verify the provided file_path exists
    if os.path.exists(file_path):
        for video_type in video_types:
            # get the list of files from the provided path
            file_list += glob.glob(f"{file_path}/**/*{video_type}")
        # mirror folder structure into a dictionary
        folder_structure = {Path(item).parts[-2]: len([i for i in file_list if Path(item).parts[-2] in i]) for item in file_list}

        # convert the list of video_files to a dictionary
        videos = {}
        for file in file_list:
            if get_file_type(file) in video_types:
                season_dir = Path(file).parent
                episode_name = get_file_name(file)
                episode_number = get_episode_number(episode_name)
                # check to see if key exists for the season, create it if not
                if season_dir in videos.keys():
                    videos[season_dir].insert(episode_number, episode_name)
                else:
                    # add the key to videos dictionary
                    videos[season_dir] = [episode_name]

            # append the episode to the season's list at the episodes # index

    else:
        console.print(f"[red]The provided file path doesn't exist! Provided: {file_path}")
        sys.exit(1)
    # return the list of files
    return file_list


get_video_files(Path(os.getcwd()))
