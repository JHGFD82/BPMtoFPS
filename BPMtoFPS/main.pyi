"""
Type stubs for BPMtoFPS main module.
"""

from typing import Dict, List, Union, Optional

def convert_time(
    ref_format: str,
    target_formats: Union[str, List[str]],
    input_value: Union[int, str],
    bpm: Optional[Union[int, float]] = None,
    fps: Optional[float] = None,
    ticks_per_beat: int = 480,
    notes_per_measure: Optional[int] = None,
    frac: float = 0.75,
    do_print: bool = False  # Deprecated: print the return value yourself
) -> Dict[str, Union[int, float, str]]: ...
