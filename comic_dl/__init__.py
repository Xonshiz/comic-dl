"""
comic_dl: A library to download and convert comics from various sites.
Expose parse_args, RunOptions, and DownloadManager.
"""

from .config        import parse_args, RunOptions
from .core.manager  import DownloadManager

__all__ = ["parse_args", "RunOptions", "DownloadManager"]
