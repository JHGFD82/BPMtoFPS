"""
Type stubs for BPMtoFPS package.
"""

from typing import Dict, List, Union, Optional

# Main conversion function
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

# Input converter functions
def ticks_to_seconds(input_value: int, bpm: int, ticks_per_beat: int) -> float: ...
def beats_to_seconds(input_value: int, bpm: int) -> float: ...
def measures_to_seconds(input_value: int, bpm: int, notes_per_measure: int) -> float: ...
def timecode_to_seconds(input_value: str) -> float: ...
def video_frames_to_seconds(input_value: int, fps: float) -> float: ...

# Output converter functions
def seconds_to_frames(seconds: float, fps: float, frac: Optional[float] = ...) -> int: ...
def seconds_to_timecode(seconds: float, fps: float, frac: Optional[float] = ...) -> str: ...

# Constants
DEFAULT_TICKS_PER_BEAT: int
SECONDS_PER_MINUTE: int
DEFAULT_ROUNDING_THRESHOLD: float

# Backward compatibility constants
TPB: int
SPM: int
fraction: float
