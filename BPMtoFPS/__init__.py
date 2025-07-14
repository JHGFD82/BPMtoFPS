"""
BPMtoFPS: Convert time between musical and video production formats.

This package provides functions to convert between different time representations
used in music production (MIDI ticks, beats, measures, timecode) and video
production (video frames, timecode, seconds).

Main Functions:
    convert_time: Main conversion function supporting multiple input/output formats
    
Individual Converters:
    ticks_to_seconds: Convert MIDI ticks to seconds
    beats_to_seconds: Convert beats to seconds  
    measures_to_seconds: Convert measures to seconds
    timecode_to_seconds: Convert timecode string to seconds
    video_frames_to_seconds: Convert video frames to seconds
    seconds_to_frames: Convert seconds to video frames
    seconds_to_timecode: Convert seconds to timecode string

Example:
    >>> from BPMtoFPS import convert_time
    >>> result = convert_time('beats', 'frames', 24, bpm=120, fps=29.97)
    >>> print(result)
    {'frames': 720}

    >>> from BPMtoFPS import beats_to_seconds
    >>> seconds = beats_to_seconds(24, 120)
    >>> print(seconds)
    12.0
"""

from .main import convert_time
from .converters import (
    ticks_to_seconds,
    beats_to_seconds,
    measures_to_seconds,
    timecode_to_seconds,
    video_frames_to_seconds,
    seconds_to_frames,
    seconds_to_timecode,
)
from .models import InputFormat, OutputFormat
from .constants import (
    DEFAULT_TICKS_PER_BEAT,
    SECONDS_PER_MINUTE,
    DEFAULT_ROUNDING_THRESHOLD,
    TPB,  # Backward compatibility
    SPM,  # Backward compatibility
    fraction,  # Backward compatibility
)

# Explicitly declare what should be available when importing the package
__all__ = [
    # Main function
    'convert_time',
    
    # Converter functions
    'ticks_to_seconds',
    'beats_to_seconds',
    'measures_to_seconds',
    'timecode_to_seconds',
    'video_frames_to_seconds',
    'seconds_to_frames',
    'seconds_to_timecode',
    
    # Models/Enums
    'InputFormat',
    'OutputFormat',
    
    # Constants
    'DEFAULT_TICKS_PER_BEAT',
    'SECONDS_PER_MINUTE',
    'DEFAULT_ROUNDING_THRESHOLD',
    
    # Backward compatibility constants
    'TPB',
    'SPM',
    'fraction',
]