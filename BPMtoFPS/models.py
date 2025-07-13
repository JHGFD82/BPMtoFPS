"""
Data models and enums for BPMtoFPS package.
"""

from enum import Enum


class InputFormat(Enum):
    """Supported input formats for conversion."""
    TICKS = 'ticks'
    BEATS = 'beats'
    MEASURES = 'measures'
    TIMECODE = 'timecode'
    VIDEO_FRAMES = 'video_frames'


class OutputFormat(Enum):
    """Supported output formats for conversion."""
    FRAMES = 'frames'
    TIMECODE = 'timecode'
    SECONDS = 'seconds'
