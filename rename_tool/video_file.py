"""
Class for easier parsing of video information
"""
import re
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class VideoFile(BaseModel):
    """
    Class for easier parsing of video information
    """

    season: int = Field(
        ..., title="Season Number", description="The season number of the video file"
    )
    episode: int = Field(
        ..., title="Episode Number", description="The episode number of the video file"
    )
    episode_name: Optional[str] = Field(
        "", title="Episode Name", description="The name of the episode"
    )
    file_path: Path = Field(
        ..., title="File Path", description="The path to the video file"
    )
    file_name: str = Field(
        ..., title="File Name", description="The name of the video file"
    )
    file_type: str = Field(
        ..., title="File Type", description="The file type of the video file"
    )
    directory: Path = Field(
        ..., title="Directory", description="The directory of the video file"
    )
    new_name: Optional[str] = Field(
        "", title="New Name", description="The new name for the video file"
    )

    @model_validator(mode="after")
    def determine_new_name(self):
        """
        Method to determine the new name of the video file
        :return: The new name of the video file
        """
        pattern = re.compile(r"\s*episode\s*", re.IGNORECASE)
        episode_name = f" {self.episode_name}" if self.episode_name else ""
        episode_name = f"S{self.season:02}E<epNumber>{episode_name}{self.file_type}"
        self.new_name = pattern.sub("", episode_name)

    def update_new_name(self, index: int) -> None:
        """
        Method to update the new name of the video file

        :param int index: Index of the video file in the season directory
        """
        ep_number = (
            self.episode
            if self.episode < index
            else index
        )
        if ep_number >= 100:
            self.new_name = self.new_name.replace("<epNumber>", f"{ep_number}")
        else:
            self.new_name = self.new_name.replace("<epNumber>", f"{ep_number:02}")
