#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Miscellaneous functions that are used in main.py """

# standard python imports
import glob
import os
import re
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console

from .video_file import VideoFile

console = Console()


def parse_episode_number_and_name(file_name: str) -> tuple[int, Optional[str]]:
    """
    Function to parse the provided episode_name for an episode number and name

    :param str file_name: File name for the video file
    :return: The provided episode_name's episode # and episode name
    :rtype: tuple[int, Optional[str]]
    """
    # use regex to see if it fits the SXXEXX format
    if match := re.search(r"S(\d{2,3})E(\d{2,3})", file_name, re.IGNORECASE):
        return int(match.group(2)), file_name.replace(match.group(), "").strip()
    # use regex to find the episode number
    if match := re.search(r"(\d{1,3})", file_name):
        return int(match.group()), file_name.replace(match.group(), "").strip()
    # see if underscores are used
    for split_char in ["_", "-", "."]:
        if split_char in file_name:
            split_episode_name = file_name.split(split_char)
            for item in split_episode_name:
                try:
                    episode_number = int(item)
                    return episode_number, None
                except ValueError:
                    continue
    console.print(f"[red] Cannot parse episode number from {file_name}")
    return 0, None


def get_video_files(file_path: Path) -> dict[str, list[VideoFile]]:
    """
    Function to go to the provided file_path and returns a dictionary
    of all the files within the provided path

    :param Path file_path: Directory to get all files in
    :return: Dictionary with a key for each season with a list of its videos
    :rtype: dict[str, list[VideoFile]]
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
    videos = {}

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
            videos[folder] = []
            # parse the needed information from the file path
            for file in files:
                episode_number, episode_name = parse_episode_number_and_name(file.stem)
                videos[folder].append(
                    VideoFile(
                        season=int(folder.split(" ")[-1]),
                        episode=episode_number,
                        episode_name=episode_name,
                        file_path=file,
                        file_name=file.stem,
                        file_type=file.suffix,
                        directory=file.parent,
                    )
                )
            # sort the season folder by lowest episode number
            videos[folder] = sorted(videos[folder], key=lambda x: x.episode)
    else:
        console.print(
            f"[red]The provided file path doesn't exist! Provided: {file_path}"
        )
        sys.exit(1)
    # return the list of files
    return videos


def rename_files(videos_by_season: dict[str, list[VideoFile]]) -> int:
    """
    Function to rename the items in the provided file_list

    :param dict[str, list[VideoFile]] videos_by_season: Dictionary with a key
     for each season with a list of its videos
    :return: # of files that were renamed
    :rtype: int
    """
    # create a counter for files renamed
    counter = 0
    failed_files = []
    for _, videos in videos_by_season.items():
        for video in videos:
            try:
                video.update_new_name(videos.index(video) + 1)
                os.rename(video.file_path, video.directory / video.new_name)
                counter += 1
            except OSError as err:
                failed_files.append(video.file_name)
                console.print(f"[red]Failed to rename {video.file_name} - {err}")
    # return counter for console output
    if failed_files:
        console.print(
            f"[red]Failed to rename {len(failed_files)} files: {failed_files}"
        )
    return counter
