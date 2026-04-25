"""
Type stubs for BPMtoFPS package.
"""

from typing import Dict, List, Union, Optional

__version__: str

# Main conversion function
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

# Input converter functions
def ticks_to_seconds(input_value: int, bpm: Union[int, float], ticks_per_beat: int) -> float: ...
def beats_to_seconds(input_value: int, bpm: Union[int, float]) -> float: ...
def measures_to_seconds(input_value: int, bpm: Union[int, float], notes_per_measure: int) -> float: ...
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
