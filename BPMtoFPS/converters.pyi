"""
Type stubs for BPMtoFPS converters module.
"""

from typing import Optional

def ticks_to_seconds(input_value: int, bpm: int, ticks_per_beat: int) -> float: ...
def beats_to_seconds(input_value: int, bpm: int) -> float: ...
def measures_to_seconds(input_value: int, bpm: int, notes_per_measure: int) -> float: ...
def timecode_to_seconds(input_value: str) -> float: ...
def video_frames_to_seconds(input_value: int, fps: float) -> float: ...
def seconds_to_frames(seconds: float, fps: float, frac: Optional[float] = ...) -> int: ...
def seconds_to_timecode(seconds: float, fps: float, frac: Optional[float] = ...) -> str: ...
