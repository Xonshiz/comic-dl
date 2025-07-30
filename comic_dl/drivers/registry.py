"""
Registry mapping URL patterns to drivers and layouts.
"""

import re
from typing import List, Type, Dict
from .base           import BaseDriver
from ..exceptions    import UnsupportedSiteError

_registry: List[Dict] = []

def register_driver(pattern: str,
                    driver_cls: Type[BaseDriver],
                    layout_name: str):
    regex = re.compile(pattern)
    _registry.append({
        "pattern": regex,
        "cls":     driver_cls,
        "layout":  layout_name
    })

def get_driver(url: str) -> BaseDriver:
    for entry in _registry:
        if entry["pattern"].search(url):
            return entry["cls"]()
    layouts = [e["layout"] for e in _registry]
    raise UnsupportedSiteError(url, layouts)

def available_layouts() -> List[str]:
    return [e["layout"] for e in _registry]
