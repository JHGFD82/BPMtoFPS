"""
Type stubs for BPMtoFPS validation module.
"""

from typing import List, Union

def validate_formats(ref_format: str, target_formats: Union[str, List[str]]) -> None: ...
def validate_input_value(input_value: Union[int, str, float], ref_format: str) -> Union[int, str]: ...
