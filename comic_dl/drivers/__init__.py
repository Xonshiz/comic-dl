# file: comic_dl/drivers/__init__.py

import pkgutil
import importlib
from pathlib import Path

# Walk the 'sites' subpackage
_sites_pkg = importlib.import_module(f"{__name__}.sites")
sites_path = Path(_sites_pkg.__file__).parent

for finder, name, is_pkg in pkgutil.iter_modules([str(sites_path)]):
    importlib.import_module(f"{__name__}.sites.{name}")
