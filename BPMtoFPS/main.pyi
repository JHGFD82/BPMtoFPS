"""
Type stubs for BPMtoFPS main module.
"""

from typing import Dict, List, Union, Optional

def convert_time(
    ref_format: str,
    target_formats: Union[str, List[str]],
    input_value: Union[int, str],
    bpm: Optional[int] = ...,
    fps: Optional[float] = ...,
    ticks_per_beat: int = ...,
    notes_per_measure: Optional[int] = ...,
    do_print: bool = ...
) -> Dict[str, Union[int, float, str]]: ...
