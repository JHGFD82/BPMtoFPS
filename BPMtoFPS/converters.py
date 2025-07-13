"""
Core conversion functions for BPMtoFPS package.
"""

import math
from typing import Optional
from .constants import SECONDS_PER_MINUTE, DEFAULT_ROUNDING_THRESHOLD


def ticks_to_seconds(input_value: int, bpm: int, ticks_per_beat: int) -> float:
    """
    Convert ticks to seconds

    Parameters:
        input_value (int): The value to convert
        bpm (int): The beats per minute of the piece of music
        ticks_per_beat (int): The number of ticks per quarter note (default is 480)

    Arithmetic:
        seconds = input_value / ticks_per_beat / bpm * 60 seconds per minute

    Returns:
         Total number of seconds
    """
    return input_value / ticks_per_beat / bpm * SECONDS_PER_MINUTE


def beats_to_seconds(input_value: int, bpm: int) -> float:
    """
    Convert beats to seconds

    Parameters:
        input_value (int): The value to convert
        bpm (int): The beats per minute of the piece of music

    Arithmetic:
        seconds = input_value / bpm * 60 seconds per minute

    Returns:
        Total number of seconds
    """
    return input_value / bpm * SECONDS_PER_MINUTE


def measures_to_seconds(input_value: int, bpm: int, notes_per_measure: int) -> float:
    """
    Convert measures to seconds

    Parameters:
        input_value (int): The value to convert
        bpm (int): The beats per minute of the piece of music
        notes_per_measure (int): The number of quarter notes per measure

    Arithmetic:
        seconds = input_value * notes_per_measure / bpm * 60 seconds per minute

    Returns:
         Total number of seconds
    """
    return input_value * notes_per_measure / bpm * SECONDS_PER_MINUTE


def timecode_to_seconds(input_value: str) -> float:
    """
    Convert timecode to seconds

    Parameters:
        input_value (str): The timecode value to convert (format: "mm:ss" or just seconds as string)

    Arithmetic:
        seconds = minutes of timecode * 60 seconds per minute + seconds of timecode

    Returns:
        Total number of seconds
    """
    if ':' in input_value:
        minutes, seconds = map(float, input_value.split(':'))
        return minutes * SECONDS_PER_MINUTE + seconds
    else:
        return float(input_value)


def video_frames_to_seconds(input_value: int, fps: float) -> float:
    """
    Convert frames to seconds

    Parameters:
        input_value (int): The value to convert
        fps (float): The frames per second of the video

    Arithmetic:
        seconds = frame / frames per second

    Returns:
        Total number of seconds as a float
    """
    return round(input_value / fps, 2)


def seconds_to_frames(seconds: float, fps: float, frac: Optional[float] = DEFAULT_ROUNDING_THRESHOLD) -> int:
    """
    Convert seconds to frames

    Parameters:
        seconds (float): The number of seconds
        fps (float): The number of frames per second in a video project
        frac (float): The threshold for rounding (default: 0.75)

    Arithmetic:
        frames = (seconds * fps) rounded depending on decimal vs. fraction

    Returns:
        Total number of frames
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
    """
    Convert seconds to timecode

    Parameters:
        seconds (float): The number of seconds
        fps (float): The number of frames per second in a video project
        frac (float): The threshold for rounding (default: 0.75)

    Arithmetic:
        timecode = string(total frames + ":" + total frames - seconds * fps)

    Returns:
        Timecode as string
    """
    whole_frames = seconds_to_frames(seconds, fps, frac)
    whole_seconds = math.floor(seconds)
    frame_part = int(whole_frames - whole_seconds * fps)

    return f"{whole_seconds}:{frame_part:02d}"
