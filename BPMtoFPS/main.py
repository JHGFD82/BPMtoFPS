import math
import argparse
import sys
from enum import Enum
from typing import Union, Optional, Dict, List, Callable


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

# Constants
DEFAULT_TICKS_PER_BEAT = 480  # MIDI resolution
SECONDS_PER_MINUTE = 60
DEFAULT_ROUNDING_THRESHOLD = 0.75  # Threshold for frame rounding

# Maintain backward compatibility
TPB = DEFAULT_TICKS_PER_BEAT
SPM = SECONDS_PER_MINUTE
fraction = DEFAULT_ROUNDING_THRESHOLD


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


def _validate_input_value(input_value: Union[int, str, float], ref_format: str) -> Union[int, str]:
    """
    Validate and convert input value based on reference format.
    
    Args:
        input_value: The input value to validate
        ref_format: The reference format type
        
    Returns:
        Properly typed input value
        
    Raises:
        ValueError: If input value is invalid for the given format
    """
    # Do not allow floats under any circumstances. While timecode can have a float in seconds, 
    # it must be entered as string.
    if isinstance(input_value, float):
        raise ValueError("Input must be a string for timecodes or an integer for beats and ticks. "
                        "Floats are not accepted.")

    # Convert input value to integer if numeric format is specified
    numeric_formats = {InputFormat.TICKS.value, InputFormat.BEATS.value, 
                      InputFormat.MEASURES.value, InputFormat.VIDEO_FRAMES.value}
    
    if ref_format in numeric_formats:
        try:
            return int(input_value)
        except ValueError:
            raise ValueError(f"Input for {ref_format} must be an integer.")
    else:
        return str(input_value)


def convert_time(ref_format: str, target_formats: Union[str, List[str]], input_value: Union[int, str],
                 bpm: Optional[int] = None, fps: Optional[float] = None, ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT,
                 notes_per_measure: Optional[int] = None, do_print: bool = False) -> Dict[str, Union[int, float, str]]:
    """
    The main function of BPMtoFPS. Convert a form of audio timing (either MIDI ticks, beats, measures, or timecode),
    or video frames, to a video timing format, either video frames, timecode, or just seconds.

    Required Parameters:
        - ref_format (str): The input format ('ticks', 'beats', 'measures', 'timecode', 'video_frames')
        - target_formats (str or List[str]): The output format(s) ('frames', 'timecode', 'seconds')
        - input_value (int or str): The value to be processed, based on the input format

    Optional Parameters:
        - bpm (int): The beats per minute, required for ticks/beats/measures
        - fps (float): The frames per second, required for video output formats
        - ticks_per_beat (int): The number of ticks per beat (default: 480)
        - notes_per_measure (int): The number of quarter notes per measure, required for measures
        - do_print (bool): If true, print the result to the console

    Returns:
        Dictionary containing the converted values in the requested target formats.
    """
    
    # Validate and convert input value
    validated_input = _validate_input_value(input_value, ref_format)

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


def format_cli_output(result: Dict[str, Union[int, float, str]], quiet: bool = False) -> str:
    """
    Format the conversion result for CLI output in a user-friendly way.
    
    Args:
        result: Dictionary containing conversion results
        quiet: If True, return only values without labels
        
    Returns:
        Formatted string for CLI output
    """
    if quiet:
        # Return only values, space-separated for piping
        return ' '.join(str(v) for v in result.values())
    
    # Format for human-readable output
    formatted_lines = []
    for key, value in result.items():
        if key == 'frames':
            formatted_lines.append(f"Frames: {value}")
        elif key == 'timecode':
            formatted_lines.append(f"Timecode: {value}")
        elif key == 'seconds':
            if isinstance(value, float):
                formatted_lines.append(f"Seconds: {value:.3f}")
            else:
                formatted_lines.append(f"Seconds: {value}")
    
    return '\n'.join(formatted_lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert MIDI ticks, beats, measures, or audio timecode to video frames, timecode, or seconds',
        epilog='''
Examples:
  %(prog)s -b -i 24 -B 128 -F 29.97 -V     # Convert 24 beats at 128 BPM to frames
  %(prog)s -t -i 480 -B 120 -F 24 -C       # Convert 480 ticks to timecode
  %(prog)s -c -i "1:30.5" -F 25 -S         # Convert timecode to seconds
  %(prog)s -m -i 8 -B 140 -N 4 -F 30 -VCS  # Convert 8 measures to all formats
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Add version info
    parser.add_argument('--version', action='version', version='BPMtoFPS 1.4.0')

    # Group all input types together so only one can be selected
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-t', '--ticks', dest='input_type', action='store_const', const=InputFormat.TICKS.value,
                             help='Input is MIDI ticks')
    input_group.add_argument('-b', '--beats', dest='input_type', action='store_const', const=InputFormat.BEATS.value,
                             help='Input is beats')
    input_group.add_argument('-m', '--measures', dest='input_type', action='store_const', const=InputFormat.MEASURES.value,
                             help='Input is measures')
    input_group.add_argument('-c', '--timecode', dest='input_type', action='store_const', const=InputFormat.TIMECODE.value,
                             help='Input is timecode in mm:ss.sss format')
    input_group.add_argument('-v', '--video-frames', dest='input_type', action='store_const', const=InputFormat.VIDEO_FRAMES.value,
                             help='Input is video frame number')

    # Output format arguments - default to frames if none specified
    parser.add_argument('-V', '--frames', dest='output_types', action='append_const', const=OutputFormat.FRAMES.value,
                        help='Output as frames')
    parser.add_argument('-C', '--timecode-out', dest='output_types', action='append_const', const=OutputFormat.TIMECODE.value,
                        help='Output as timecode')
    parser.add_argument('-S', '--seconds', dest='output_types', action='append_const', const=OutputFormat.SECONDS.value,
                        help='Output as seconds')
    parser.add_argument('-A', '--all-formats', dest='output_all', action='store_true',
                        help='Output in all available formats')

    # Required parameters
    parser.add_argument('-i', '--input-value', type=str, required=True,
                        help='Input value (number of ticks, beats, measures, frames, or timecode)')
    parser.add_argument('-F', '--fps', type=float,
                        help='Frames per second of the video (required for video output formats)')
    
    # Conditional parameters
    parser.add_argument('-B', '--bpm', type=int,
                        help='Beats per minute (required for ticks, beats, and measures)')
    parser.add_argument('-D', '--division', type=int, default=DEFAULT_TICKS_PER_BEAT,
                        help=f'MIDI ticks per beat (default: {DEFAULT_TICKS_PER_BEAT})')
    parser.add_argument('-N', '--notes-per-measure', type=int,
                        help='Quarter notes per measure (required for measures)')

    # Output control
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Output only values (useful for scripting)')
    parser.add_argument('--no-output', action='store_true',
                        help='Suppress all output (useful for validation)')

    args = parser.parse_args()

    # Handle default output format
    if args.output_all:
        args.output_types = [OutputFormat.FRAMES.value, OutputFormat.TIMECODE.value, OutputFormat.SECONDS.value]
    elif args.output_types is None:
        # Default to frames if no output format specified
        args.output_types = [OutputFormat.FRAMES.value]

    # Validate required parameters based on input/output types
    video_output_formats = {OutputFormat.FRAMES.value, OutputFormat.TIMECODE.value}
    needs_fps = any(fmt in video_output_formats for fmt in args.output_types)
    
    if needs_fps and args.fps is None:
        parser.error("-F/--fps is required for video output formats (frames, timecode)")

    # Input-specific validation
    if args.input_type == InputFormat.TICKS.value and args.bpm is None:
        parser.error("-B/--bpm is required for ticks input")
    elif args.input_type == InputFormat.BEATS.value and args.bpm is None:
        parser.error("-B/--bpm is required for beats input")
    elif args.input_type == InputFormat.MEASURES.value:
        if args.bpm is None or args.notes_per_measure is None:
            parser.error("-B/--bpm and -N/--notes-per-measure are required for measures input")
    elif args.input_type == InputFormat.VIDEO_FRAMES.value and args.fps is None:
        parser.error("-F/--fps is required for video frames input")

    try:
        # Perform conversion
        result = convert_time(
            args.input_type, 
            args.output_types, 
            args.input_value, 
            args.bpm, 
            args.fps, 
            args.division,
            args.notes_per_measure, 
            do_print=False  # We'll handle output ourselves
        )
        
        # Output results
        if not args.no_output:
            output = format_cli_output(result, args.quiet)
            print(output)
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
