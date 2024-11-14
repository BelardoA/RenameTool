#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Miscellaneous functions that are used in main.py """

# standard python imports
import glob
import os
import platform
import re
import sys
from pathlib import Path

from rich.console import Console

from video_file import VideoFile

console = Console()


def get_episode_number(episode_name: str) -> int:
    """
    Function to parse the provided episode_name for an episode number

    :param str episode_name: File name for the episode
    :return: The provided episode_name's episode #
    :rtype: int
    """
    # use regex to see if it fits the SXXEXX format
    if match := re.search(r"S(\d{2,3})E(\d{2,3})", episode_name, re.IGNORECASE):
        return match.group(2)
    # use regex to find the episode number
    if match := re.search(r"(\d{2,3})", episode_name):
        return match.group()
    # see if underscores are used
    for split_char in ["_", "-", "."]:
        if split_char in episode_name:
            split_episode_name = episode_name.split(split_char)
            for item in split_episode_name:
                try:
                    episode_number = int(item)
                    return episode_number
                except ValueError:
                    continue
    console.print(f"[red] Cannot parse episode number from {episode_name}")
    return 0


def get_video_files(file_path: Path) -> list[VideoFile]:
    """
    Function to go to the provided file_path and returns a dictionary
    of all the files within the provided path

    :param Path file_path: Directory to get all files in
    :return: List of video files
    :rtype: list[VideoFile]
    """
    # plex supported videos
    video_types = [
        ".mp4",
        ".mkv",
        ".wmv",
        ".mpeg",
        ".mpegts",
        ".mov",
        ".avi",
        ".asf",
        ".flv",
        ".m4v",
        ".mpg",
    ]
    season_file_mapping = {}
    videos = []

    # verify the provided file_path exists
    if os.path.exists(file_path):
        # get the folders in the provided file_path
        folders = [
            f for f in os.listdir(file_path) if os.path.isdir(f"{file_path}/{f}")
        ]
        for folder in folders:
            season_folder = []
            for video_type in video_types:
                # get the list of files from the provided path
                season_folder += glob.glob(f"{file_path}/{folder}/*{video_type}")
            # mirror folder structure into a dictionary
            season_file_mapping[folder] = [Path(item) for item in season_folder]

        for folder, files in season_file_mapping.items():
            # parse the needed information from the file path
            for file in files:
                videos.append(
                    VideoFile(
                        season=int(folder.split(" ")[-1]),
                        episode=get_episode_number(file.stem),
                        file_path=file,
                        index=files.index(file),
                    )
                )
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
