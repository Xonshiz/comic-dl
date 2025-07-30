"""
CLI entrypoint: parse args, invoke DownloadManager, handle errors.
"""

import sys
from .config           import parse_args
from .core.manager     import DownloadManager
from .exceptions       import UnsupportedSiteError

def main():
    opts = parse_args()
    mgr  = DownloadManager(opts)
    try:
        mgr.run()
    except UnsupportedSiteError as e:
        print(f"Error: {e}")
        print("Supported layouts:", ", ".join(e.layouts))
        sys.exit(e.error_code)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
