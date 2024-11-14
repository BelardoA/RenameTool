import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from main import _rename_from_root


class TestRenameFiles(unittest.TestCase):

    @patch('main.get_video_files')
    @patch('main.rename_files')
    def test_rename_files_in_season_subfolders(self, mock_rename_files, mock_get_video_files):
        mock_get_video_files.return_value = [Path("S01E01.mp4"), Path("S01E02.mp4")]
        mock_rename_files.return_value = 2

        root = Path("/fake/root")
        _rename_from_root(root)

        mock_get_video_files.assert_called_once_with(root)
        mock_rename_files.assert_called_once_with([Path("S01E01.mp4"), Path("S01E02.mp4")])

    @patch('main.get_video_files')
    @patch('main.rename_files')
    def test_no_files_to_rename(self, mock_rename_files, mock_get_video_files):
        mock_get_video_files.return_value = []
        mock_rename_files.return_value = 0

        root = Path("/fake/root")
        _rename_from_root(root)

        mock_get_video_files.assert_called_once_with(root)
        mock_rename_files.assert_called_once_with([])

    @patch('main.get_video_files')
    @patch('main.rename_files')
    def test_handle_large_number_of_files(self, mock_rename_files, mock_get_video_files):
        mock_get_video_files.return_value = [Path(f"S01E{i:02}.mp4") for i in range(1, 101)]
        mock_rename_files.return_value = 100

        root = Path("/fake/root")
        _rename_from_root(root)

        mock_get_video_files.assert_called_once_with(root)
        mock_rename_files.assert_called_once_with([Path(f"S01E{i:02}.mp4") for i in range(1, 101)])

    @patch('main.get_video_files')
    @patch('main.rename_files')
    def test_handle_invalid_file_paths(self, mock_rename_files, mock_get_video_files):
        mock_get_video_files.return_value = [Path("invalid_path.mp4")]
        mock_rename_files.side_effect = OSError("Invalid file path")

        root = Path("/fake/root")
        try:
            _rename_from_root(root)
        except OSError:
            pass

        mock_get_video_files.assert_called_once_with(root)
        mock_rename_files.assert_called_once_with([Path("invalid_path.mp4")])

    @patch('main.get_video_files')
    @patch('main.rename_files')
    def test_handle_files_with_no_season_or_episode(self, mock_rename_files, mock_get_video_files):
        mock_get_video_files.return_value = [Path("random_video.mp4")]
        mock_rename_files.return_value = 0

        root = Path("/fake/root")
        _rename_from_root(root)

        mock_get_video_files.assert_called_once_with(root)
        mock_rename_files.assert_called_once_with([Path("random_video.mp4")])

    @patch('main.get_video_files')
    @patch('main.rename_files')
    def test_handle_files_with_special_characters(self, mock_rename_files, mock_get_video_files):
        mock_get_video_files.return_value = [Path("S01E01_@special!.mp4")]
        mock_rename_files.return_value = 1

        root = Path("/fake/root")
        _rename_from_root(root)

        mock_get_video_files.assert_called_once_with(root)
        mock_rename_files.assert_called_once_with([Path("S01E01_@special!.mp4")])
