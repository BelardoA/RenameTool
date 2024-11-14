"""
Class for easier parsing of video information
"""

from typing import Optional
from pathlib import Path
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
    new_name: Optional[str] = Field(
        "", title="New Name", description="The new name for the video file"
    )
    index: int = Field(
        ..., title="Index", description="The index of the video file in the directory"
    )
