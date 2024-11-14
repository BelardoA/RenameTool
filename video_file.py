"""
Class for easier parsing of video information
"""

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


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
    index: int = Field(
        ..., title="Index", description="The index of the video file in the directory"
    )
