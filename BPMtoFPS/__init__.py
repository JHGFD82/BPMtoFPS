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