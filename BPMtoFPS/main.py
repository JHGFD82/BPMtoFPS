import math
import argparse
from typing import Union, Optional, Dict, List, Callable

TPB = 480  # Ticks per beat (resolution)
SPM = 60  # Seconds per minute
fraction = 0.75  # The threshold for rounding


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
    return input_value / ticks_per_beat / bpm * SPM


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
    return input_value / bpm * SPM


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
    return input_value * notes_per_measure / bpm * SPM


def timecode_to_seconds(input_value: str) -> float:
    """
    Convert timecode to seconds

    Parameters:
        input_value (int): The value to convert

    Arithmetic:
        seconds = minutes of timecode * 60 seconds per minute + seconds of timecode

    Returns:
        Total number of seconds
    """
    if ':' in input_value:
        minutes, seconds = map(float, input_value.split(':'))
        return minutes * SPM + seconds
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


def seconds_to_frames(seconds: float, fps: float, frac: Optional[float] = fraction) -> int:
    """
    Convert seconds to frames

    Parameters:
        seconds (int): The number of seconds
        fps (int): The number of frames per second in a video project
        frac (float): The threshold for rounding

    Arithmetic:
        frames = (seconds * fps) rounded depending on decimal vs. fraction

    Returns:
        Total number of frames
    """
    if frac is None:
        frac = fraction
    frame_count = seconds * fps
    whole_frames = math.floor(frame_count)
    fractional_frames: float = frame_count % 1

    if fractional_frames >= frac:
        whole_frames += 1

    return whole_frames


def seconds_to_timecode(seconds: float, fps: float, frac: Optional[float] = fraction) -> str:
    """
    Convert seconds to timecode

    Parameters:
        seconds (int): The number of seconds
        fps (int): The number of frames per second in a video project
        frac (float): The threshold for rounding

    Arithmetic:
        timecode = string(total frames + ":" + total frames - seconds * fps)

    Returns:
        Timecode as string
    """
    whole_frames = seconds_to_frames(seconds, fps, frac)
    whole_seconds = math.floor(seconds)
    frame_part = int(whole_frames - whole_seconds * fps)

    return f"{whole_seconds}:{frame_part:02d}"


def convert_time(ref_format: str, target_formats: Union[str, List[str]], input_value: Union[int, str],
                 bpm: Optional[int] = None, fps: Optional[float] = None, ticks_per_beat: int = TPB,
                 notes_per_measure: Optional[int] = None, do_print: bool = False) -> Dict[str, Union[int, float, str]]:
    """
    The main function of BPMtoFPS. Convert a form of audio timing (either MIDI ticks, beats, measures, or timecode),
    or video frames, to a video timing format, either video frames, timecode, or just seconds.

    Required Parameters:
        - ref_format (string): The input of the function as either a number of ticks, beats, or timecode
        - target_format (list): The output of the function as any combination of video frames, timecode, or seconds
        - input_value (string/int): The number of ticks or the timecode to be processed, based on the input provided
        - fps (float): The frames per second of the video project

    Optional Parameters:
        - bpm (float): The beats per minute, not required if inputting timecode
        - ticks_per_beat (int): The number of ticks per beat
        - notes_per_measure (int): The number of quarter notes that make up a measure of music
        - do_print (bool): If true, print the result to the console

    Returns:
        Depending on the target_format, this function returns either the number of frames in the video as an
        integer, the specific timecode in the video as string, and/or just the seconds as a float. All results
        are returned in a dictionary.
    """

    # Do not allow floats under any circumstances. While timecode can have a float in seconds, it must be entered as
    # string.
    if isinstance(input_value, float):
        raise ValueError("Input must be a string for timecodes or an integer for beats and ticks. Floats are not "
                         "accepted.")

    # Convert input value to integer if 'ticks' or 'beats' is specified.
    if ref_format in ['ticks', 'beats', 'measures', 'video_frames']:
        try:
            input_value = int(input_value)
        except ValueError:
            raise ValueError("Input for ticks, beats, measures, and video_frames must be an integer.")
    else:
        input_value = str(input_value)
    # No conversion needed here for timecode, but instead ensure that the value is passed through as string.

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
        'ticks': validate_and_convert_ticks,
        'beats': validate_and_convert_beats,
        'measures': validate_and_convert_measures,
        'timecode': lambda x: timecode_to_seconds(str(x)),
        'video_frames': validate_and_convert_video_frames
    }
    out_conversion_map: Dict[str, Callable[[float, float, float], Union[int, str]]] = {
        'frames': lambda s, f, frac: seconds_to_frames(s, f, frac),
        'timecode': lambda s, f, frac: seconds_to_timecode(s, f, frac)
    }

    # Attempt conversion, using conversion maps to navigate to proper function
    try:
        seconds = in_conversion_map[ref_format](input_value)
    except Exception as err:
        raise ValueError(f"An error occurred during conversion: {err}")

    # If the target_formats variable is not a list, make it a list
    if not isinstance(target_formats, list):
        target_formats = [target_formats]

    # If 'seconds' are indicated in target_formats, add the seconds to the dictionary first and remove it from the list
    if 'seconds' in target_formats:
        output: Dict[str, Union[int, float, str]] = {'seconds': seconds}
        target_formats.remove('seconds')
    else:
        output = {}

    # Now do the other target formats
    for target_format in target_formats:
        try:
            if fps is None:
                raise ValueError(f"fps is required for {target_format} conversion")
            output[target_format] = out_conversion_map[target_format](seconds, fps, fraction)
        except Exception as err:
            raise ValueError(f"An error occurred during conversion: {err}")

    # Print results if requested
    if do_print:
        print(output)

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert MIDI ticks, beats, measures, or audio timecode '
                                                 'to video frames, timecode, or seconds')

    # Group all input types together so only one can be selected
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-t', '--ticks', dest='input_type', action='store_const', const='ticks',
                             help='Input is MIDI ticks')
    input_group.add_argument('-b', '--beats', dest='input_type', action='store_const', const='beats',
                             help='Input is beats')
    input_group.add_argument('-m', '--measures', dest='input_type', action='store_const', const='measures',
                             help='Input is measures')
    input_group.add_argument('-c', '--timecode_in', dest='input_type', action='store_const', const='timecode',
                             help='Input is timecode in mm:ss.sss format')
    input_group.add_argument('-v', '--video_frames', dest='input_type', action='store_const', const='video_frames',
                             help='Input is video frame number')

    # Group all output types together so any combination is accepted
    parser.add_argument('-V', '--frames', dest='output_types', action='append_const', const='frames',
                        help='Output as frames')
    parser.add_argument('-C', '--timecode_out', dest='output_types', action='append_const', const='timecode',
                        help='Output as timecode')
    parser.add_argument('-S', '--seconds', dest='output_types', action='append_const', const='seconds',
                        help='Output as seconds')

    # Additional parameters, requirement based on input type
    parser.add_argument('-i', '--input_value', type=str, required=True,
                        help='Input value (number of ticks, beats, or timecode)')
    parser.add_argument('-B', '--bpm', type=int,
                        help='Beats per minute, required when inputting ticks, beats, and measures')
    parser.add_argument('-F', '--fps', type=float, required=True,
                        help='Frames per second of the video, required for all input types')
    parser.add_argument('-D', '--division', type=int, default=TPB,
                        help='Number of MIDI ticks per beat (division), default is 480, required for ticks')
    parser.add_argument('-N', '--notes_per_measure', type=int,
                        help='Number of quarter notes that make a measure of music, required for measures')

    # Optional parameters
    parser.add_argument('-p', '--print', action='store_true',
                        help='Print the output to the console')

    args = parser.parse_args()

    # Since BPM is not required for timecode, catch errors if it's not supplied for other inputs
    if args.input_type == 'ticks' and (args.bpm is None or args.division is None):
        parser.error("-B/--bpm and -D/--division is required when 'ticks' is the input type")
    elif args.input_type == 'beats' and args.bpm is None:
        parser.error("-B/--bpm is required when 'beats' is the input type")
    elif args.input_type == 'measures' and (args.bpm is None or args.notes_per_measure is None):
        parser.error("-B/--bpm and -N/--notes_per_measure is required when 'measures' is the input type")
    elif args.input_type == 'video_frames' and args.fps is None:
        parser.error("-F/--fps is required when 'video_frames' is the input type")

    if args.output_types is None:
        parser.error("At least one output type must be specified using -F/--frames, -C/--timecode_out, or -S/--seconds")

    convert_time(args.input_type, args.output_types, args.input_value, args.bpm, args.fps, args.division,
                 args.notes_per_measure, args.print)
