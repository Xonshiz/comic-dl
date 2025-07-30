"""
Define RunOptions dataclass and parsing logic using argparse.
"""

from dataclasses import dataclass
from typing      import Optional
import argparse

@dataclass
class RunOptions:
    url:            str
    output:         Optional[str]
    format:         str
    verbose:        bool
    log_file:       Optional[str]
    language:       str
    sort:           str
    start_chapter:  Optional[int]
    end_chapter:    Optional[int]
    keep_files:     bool

def parse_args() -> RunOptions:
    parser = argparse.ArgumentParser(
        description="Download comics (single chapter or full series) from supported sites."
    )
    parser.add_argument("url", help="URL of the comic chapter or title to download")
    parser.add_argument("-o", "--output",
                        help="Output path (file base name for single, directory for series)")
    parser.add_argument("-f", "--format",
                        choices=["cbz", "pdf"], default="cbz",
                        help="Output format: cbz (default) or pdf")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="Enable verbose logging")
    parser.add_argument("--log-file", help="Path to write detailed log output")

    parser.add_argument("--language", default="en",
                        help="Chapter language code for series (default: en)")
    parser.add_argument("--sort", choices=["asc", "desc"], default="asc",
                        help="Order of chapters when downloading a series")
    parser.add_argument("--start", type=int, default=None,
                        help="1‑based start index of chapters to download in series")
    parser.add_argument("--end", type=int, default=None,
                        help="Inclusive end index of chapters to download in series")
    parser.add_argument("--keep", dest="keep_files", action="store_true",
                        help="Do not delete raw images after conversion")
    args = parser.parse_args()

    return RunOptions(
        url=args.url,
        output=args.output,
        format=args.format,
        verbose=args.verbose,
        log_file=args.log_file,
        language=args.language,
        sort=args.sort,
        start_chapter=args.start,
        end_chapter=args.end,
        keep_files=args.keep_files,
    )
