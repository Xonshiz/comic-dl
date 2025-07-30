"""
Configure logging for the library.
"""

import logging
from typing import Optional

def setup_logger(name: str, verbose: bool = False,
                 log_file: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)

    fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    ch  = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger
