"""
Type stubs for BPMtoFPS CLI module.
"""

from typing import Dict, Union

def format_cli_output(result: Dict[str, Union[int, float, str]], quiet: bool = ...) -> str: ...
def main() -> None: ...
