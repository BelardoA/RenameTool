#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Miscellaneous functions that are used in main.py """

# standard python imports
import glob
import ntpath
import os
import platform
import sys
from pathlib import Path

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
                break
            except ValueError:
                # continue to the next item
                continue
    else:
        console.print(f"[red] Cannot parse episode number from {episode_name}")
        episode_number = 0
    # return the episode number
    return episode_number


def get_video_files(file_path: Path) -> dict:
    """
    Function to go to the provided file_path and returns a dictionary
    of all the files within the provided path
    :param Path file_path: Directory to get all files in
    :raises: General error if the provided file_path doesn't exist
    :return: dictionary of files in the provided directory
    :rtype: dict
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
        folders = {
            Path(item).parts[-2]: len(
                [i for i in file_list if Path(item).parts[-2] in i]
            )
            for item in file_list
        }

        # convert the list of video_files to a dictionary following the folders
        videos = {folder: [] for folder in folders}
        for file in file_list:
            if get_file_type(file) in video_types:
                # parse the needed information from the file path
                season_dir = Path(file).parts[-2]
                episode_name = get_file_name(file)
                episode_number = get_episode_number(episode_name)

                # add the episode to the season list
                videos[season_dir].insert(episode_number - 1, file)
    else:
        console.print(
            f"[red]The provided file path doesn't exist! Provided: {file_path}"
        )
        sys.exit(1)
    # return the list of files
    return videos


def rename_files(file_list: dict) -> int:
    """
    Function to rename the items in the provided file_list
    :param dict file_list: dictionary of files that need to be renamed
    :return: # of files that were renamed
    :rtype: int
    """

    def format_number(number: str) -> str:
        """
        Function to format a number into 2 digit string
        :param int number: episode or season number to convert
        :return: XX format of the provided number
        :rtype: str
        """
        return str(number) if len(number) == 2 else f"0{number}"

    # create a counter for files renamed
    counter = 0

    for season, episodes in file_list.items():
        # start episode counter at 1
        episode_num = 1

        # parse the season #
        season_num = format_number(season.split(" ")[-1])
        # iterate through the season's episodes and rename them
        for episode in episodes:
            # parse the episode name
            episode_name = Path(episode).parts[-1]

            # format episode number
            ep_number = format_number(str(episode_num))

            # get the episode's path
            path = f"{os.sep}".join(list(Path(episode).parts)[1:-2])

            # get remove everything before the first dash
            new_name = f"{os.sep}{path}{os.sep}{season}{os.sep}S{season_num}E{ep_number} {episode_name[episode_name.find('-'):]}"

            if "Linux" in platform.system():
                # get the episode number
                os.system(f'sudo mv "{episode}" "{new_name}"')
            elif "Windows" in platform.system():
                os.system(f'mv "{episode}" "{new_name}"')

            # increment our counters
            episode_num += 1
            counter += 1
    # return counter for console output
    return counter
