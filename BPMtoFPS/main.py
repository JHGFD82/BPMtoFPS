"""
Main BPMtoFPS module containing the primary convert_time function.
"""

import sys
import os
from typing import Union, Optional, Dict, List, Callable

# Standard imports - always use relative imports for modules
from .models import InputFormat, OutputFormat
from .constants import DEFAULT_TICKS_PER_BEAT, DEFAULT_ROUNDING_THRESHOLD
from .validation import validate_input_value
from .converters import (
    ticks_to_seconds,
    beats_to_seconds,
    measures_to_seconds,
    timecode_to_seconds,
    video_frames_to_seconds,
    seconds_to_frames,
    seconds_to_timecode
)


def convert_time(ref_format: str, target_formats: Union[str, List[str]], input_value: Union[int, str],
                 bpm: Optional[int] = None, fps: Optional[float] = None, ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT,
                 notes_per_measure: Optional[int] = None, do_print: bool = False) -> Dict[str, Union[int, float, str]]:
    """Convert between musical time and video time formats.
    
    The main function of BPMtoFPS. Converts audio timing formats (MIDI ticks, beats, 
    measures, or timecode) or video frames to video timing formats (frames, timecode, 
    or seconds).
    
    Args:
        ref_format (str): The input format. One of: 'ticks', 'beats', 'measures', 
            'timecode', 'video_frames'.
        target_formats (str or List[str]): The output format(s). One or more of: 
            'frames', 'timecode', 'seconds'.
        input_value (int or str): The value to convert, based on the input format.
        bpm (int, optional): Beats per minute. Required for ticks/beats/measures 
            conversions.
        fps (float, optional): Frames per second. Required for video output formats.
        ticks_per_beat (int, optional): Number of ticks per beat. Defaults to 480.
        notes_per_measure (int, optional): Number of quarter notes per measure. 
            Required for measures conversion.
        do_print (bool, optional): If True, print the result to console. Defaults 
            to False.
    
    Returns:
        Dict[str, Union[int, float, str]]: Dictionary containing the converted values 
            in the requested target formats.
    
    Raises:
        ValueError: If required parameters are missing (bpm for musical formats, 
            fps for video formats, notes_per_measure for measures), if input_value 
            is invalid for the specified format, if ref_format or target_formats 
            contain unsupported values, or if conversion fails due to invalid data.
        KeyError: If ref_format or target_format contains unsupported format strings.
        
    Example:
        >>> result = convert_time('beats', 'frames', 24, bpm=120, fps=29.97)
        >>> print(result)
        {'frames': 359}
        
        >>> result = convert_time('ticks', ['frames', 'timecode'], 1440, 
        ...                      bpm=120, fps=29.97, ticks_per_beat=480)
        >>> print(result)
        {'frames': 45, 'timecode': '1:15'}
    """
    
    # Validate and convert input value
    validated_input = validate_input_value(input_value, ref_format)

    # Conversion maps to functions with proper validation
    def validate_and_convert_ticks(x: Union[int, str]) -> float:
        if bpm is None:
            raise ValueError("bpm is required for ticks conversion")
        return ticks_to_seconds(int(x), bpm, ticks_per_beat)

    def validate_and_convert_beats(x: Union[int, str]) -> float:
        if bpm is None:
            raise ValueError("bpm is required for beats conversion")
        return beats_to_seconds(int(x), bpm)

    def validate_and_convert_measures(x: Union[int, str]) -> float:
        if bpm is None or notes_per_measure is None:
            raise ValueError("bpm and notes_per_measure are required for measures conversion")
        return measures_to_seconds(int(x), bpm, notes_per_measure)

    def validate_and_convert_video_frames(x: Union[int, str]) -> float:
        if fps is None:
            raise ValueError("fps is required for video_frames conversion")
        return video_frames_to_seconds(int(x), fps)

    in_conversion_map: Dict[str, Callable[[Union[int, str]], float]] = {
        InputFormat.TICKS.value: validate_and_convert_ticks,
        InputFormat.BEATS.value: validate_and_convert_beats,
        InputFormat.MEASURES.value: validate_and_convert_measures,
        InputFormat.TIMECODE.value: lambda x: timecode_to_seconds(str(x)),
        InputFormat.VIDEO_FRAMES.value: validate_and_convert_video_frames
    }
    out_conversion_map: Dict[str, Callable[[float, float, float], Union[int, str]]] = {
        OutputFormat.FRAMES.value: lambda s, f, frac: seconds_to_frames(s, f, frac),
        OutputFormat.TIMECODE.value: lambda s, f, frac: seconds_to_timecode(s, f, frac)
    }

    # Attempt conversion, using conversion maps to navigate to proper function
    try:
        seconds = in_conversion_map[ref_format](validated_input)
    except Exception as err:
        raise ValueError(f"An error occurred during conversion: {err}")

    # If the target_formats variable is not a list, make it a list
    if not isinstance(target_formats, list):
        target_formats = [target_formats]

    # If 'seconds' are indicated in target_formats, add the seconds to the dictionary first and remove it from the list
    if OutputFormat.SECONDS.value in target_formats:
        output: Dict[str, Union[int, float, str]] = {OutputFormat.SECONDS.value: seconds}
        target_formats.remove(OutputFormat.SECONDS.value)
    else:
        output = {}

    # Now do the other target formats
    for target_format in target_formats:
        try:
            if fps is None:
                raise ValueError(f"fps is required for {target_format} conversion")
            output[target_format] = out_conversion_map[target_format](seconds, fps, DEFAULT_ROUNDING_THRESHOLD)
        except Exception as err:
            raise ValueError(f"An error occurred during conversion: {err}")

    # Print results if requested
    if do_print:
        print(output)

    return output


# CLI entry point
if __name__ == '__main__':
    # For direct execution, we need to handle the relative import differently
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from BPMtoFPS.cli import main
    main()
