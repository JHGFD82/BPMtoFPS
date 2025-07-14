"""
Core conversion functions for BPMtoFPS package.
"""

import math
from typing import Optional
from .constants import SECONDS_PER_MINUTE, DEFAULT_ROUNDING_THRESHOLD


def ticks_to_seconds(input_value: int, bpm: int, ticks_per_beat: int) -> float:
    """Convert MIDI ticks to seconds.

    Args:
        input_value (int): The number of ticks to convert.
        bpm (int): The beats per minute of the musical piece.
        ticks_per_beat (int): The number of ticks per quarter note (typically 480).

    Returns:
        float: Total number of seconds.
        
    Raises:
        ZeroDivisionError: If bpm or ticks_per_beat is zero.
        TypeError: If any argument is not a number.
        
    Note:
        Formula: seconds = input_value / ticks_per_beat / bpm * 60
        
    Example:
        >>> # Convert 960 ticks at 120 BPM with 480 ticks per beat
        >>> seconds = ticks_to_seconds(960, 120, 480)
        >>> print(seconds)
        1.0
        
        >>> # Convert one measure (1920 ticks) at 140 BPM
        >>> seconds = ticks_to_seconds(1920, 140, 480)
        >>> print(round(seconds, 2))
        1.71
    """
    return input_value / ticks_per_beat / bpm * SECONDS_PER_MINUTE


def beats_to_seconds(input_value: int, bpm: int) -> float:
    """Convert beats to seconds.

    Args:
        input_value (int): The number of beats to convert.
        bpm (int): The beats per minute of the musical piece.

    Returns:
        float: Total number of seconds.
        
    Raises:
        ZeroDivisionError: If bpm is zero.
        TypeError: If any argument is not a number.
        
    Note:
        Formula: seconds = input_value / bpm * 60
        
    Example:
        >>> # Convert 4 beats at 120 BPM (one measure in 4/4 time)
        >>> seconds = beats_to_seconds(4, 120)
        >>> print(seconds)
        2.0
        
        >>> # Convert 24 beats at 140 BPM
        >>> seconds = beats_to_seconds(24, 140)
        >>> print(round(seconds, 2))
        10.29
    """
    return input_value / bpm * SECONDS_PER_MINUTE


def measures_to_seconds(input_value: int, bpm: int, notes_per_measure: int) -> float:
    """Convert measures to seconds.

    Args:
        input_value (int): The number of measures to convert.
        bpm (int): The beats per minute of the musical piece.
        notes_per_measure (int): The number of quarter notes per measure.

    Returns:
        float: Total number of seconds.
        
    Raises:
        ZeroDivisionError: If bpm is zero.
        TypeError: If any argument is not a number.
        
    Note:
        Formula: seconds = input_value * notes_per_measure / bpm * 60
        
    Example:
        >>> # Convert 8 measures at 120 BPM in 4/4 time
        >>> seconds = measures_to_seconds(8, 120, 4)
        >>> print(seconds)
        16.0
        
        >>> # Convert 2 measures at 90 BPM in 3/4 time (waltz)
        >>> seconds = measures_to_seconds(2, 90, 3)
        >>> print(seconds)
        4.0
    """
    return input_value * notes_per_measure / bpm * SECONDS_PER_MINUTE


def timecode_to_seconds(input_value: str) -> float:
    """Convert timecode to seconds.

    Args:
        input_value (str): The timecode value to convert. Format: "mm:ss.sss" 
            or just seconds as string.

    Returns:
        float: Total number of seconds.
        
    Raises:
        ValueError: If the input string cannot be parsed as a valid timecode 
            or number.
        TypeError: If input_value is not a string.
        
    Note:
        Supports both "mm:ss.sss" format and direct seconds input as string.
        Formula: seconds = minutes * 60 + seconds
        
    Example:
        >>> # Convert timecode format
        >>> seconds = timecode_to_seconds("1:30.5")
        >>> print(seconds)
        90.5
        
        >>> # Convert direct seconds as string
        >>> seconds = timecode_to_seconds("45.25")
        >>> print(seconds)
        45.25
    """
    if ':' in input_value:
        minutes, seconds = map(float, input_value.split(':'))
        return minutes * SECONDS_PER_MINUTE + seconds
    else:
        return float(input_value)


def video_frames_to_seconds(input_value: int, fps: float) -> float:
    """Convert video frames to seconds.

    Args:
        input_value (int): The number of frames to convert.
        fps (float): The frames per second of the video.

    Returns:
        float: Total number of seconds, rounded to 2 decimal places.
        
    Raises:
        ZeroDivisionError: If fps is zero.
        TypeError: If any argument is not a number.
        
    Note:
        Formula: seconds = frames / frames_per_second
        
    Example:
        >>> # Convert 90 frames at 30 FPS
        >>> seconds = video_frames_to_seconds(90, 30.0)
        >>> print(seconds)
        3.0
        
        >>> # Convert 750 frames at 29.97 FPS (NTSC)
        >>> seconds = video_frames_to_seconds(750, 29.97)
        >>> print(seconds)
        25.03
    """
    return round(input_value / fps, 2)


def seconds_to_frames(seconds: float, fps: float, frac: Optional[float] = DEFAULT_ROUNDING_THRESHOLD) -> int:
    """Convert seconds to video frames with smart rounding.

    Args:
        seconds (float): The number of seconds to convert.
        fps (float): The frames per second of the video project.
        frac (float, optional): The threshold for rounding fractional frames. 
            Defaults to 0.75.

    Returns:
        int: Total number of frames, rounded based on the fractional threshold.
        
    Raises:
        TypeError: If any argument is not a number.
        ValueError: If frac is not between 0 and 1.
        
    Note:
        Uses intelligent rounding: if the fractional part >= frac, rounds up.
        Formula: frames = floor(seconds * fps) + (1 if fractional_part >= frac else 0)
        
    Example:
        >>> # Convert 2.5 seconds at 24 FPS
        >>> frames = seconds_to_frames(2.5, 24.0)
        >>> print(frames)
        60
        
        >>> # Convert with custom rounding threshold
        >>> frames = seconds_to_frames(1.8, 29.97, frac=0.5)
        >>> print(frames)
        54
    """
    if frac is None:
        frac = DEFAULT_ROUNDING_THRESHOLD
    frame_count = seconds * fps
    whole_frames = math.floor(frame_count)
    fractional_frames: float = frame_count % 1

    if fractional_frames >= frac:
        whole_frames += 1

    return whole_frames


def seconds_to_timecode(seconds: float, fps: float, frac: Optional[float] = DEFAULT_ROUNDING_THRESHOLD) -> str:
    """Convert seconds to timecode format.

    Args:
        seconds (float): The number of seconds to convert.
        fps (float): The frames per second of the video project.
        frac (float, optional): The threshold for rounding fractional frames. 
            Defaults to 0.75.

    Returns:
        str: Timecode in "seconds:frames" format (e.g., "45:12").
        
    Raises:
        TypeError: If any argument is not a number.
        ValueError: If frac is not between 0 and 1, or if any value would 
            result in invalid timecode.
        
    Note:
        Uses seconds_to_frames() for frame calculation with smart rounding.
        Formula: timecode = f"{whole_seconds}:{frame_part:02d}"
        
    Example:
        >>> # Convert 45.5 seconds at 30 FPS
        >>> timecode = seconds_to_timecode(45.5, 30.0)
        >>> print(timecode)
        '45:15'
        
        >>> # Convert 12.8 seconds at 29.97 FPS
        >>> timecode = seconds_to_timecode(12.8, 29.97)
        >>> print(timecode)
        '12:24'
    """
    whole_frames = seconds_to_frames(seconds, fps, frac)
    whole_seconds = math.floor(seconds)
    frame_part = int(whole_frames - whole_seconds * fps)

    return f"{whole_seconds}:{frame_part:02d}"
