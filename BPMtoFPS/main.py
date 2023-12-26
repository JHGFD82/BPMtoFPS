import math
import argparse

TPB = 480  # Ticks per beat (resolution)
SPM = 60  # Seconds per minute
fraction = 0.75  # The threshold for rounding


def ticks_to_seconds(input_value, bpm, ticks_per_beat):
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


def beats_to_seconds(input_value, bpm):
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


def timecode_to_seconds(input_value):
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


def calculate_frame_count(seconds, fps, frac=fraction):
    """
    Calculate frame count for supplied seconds, with custom rounding based on fraction parameter

    Parameters:
        seconds (int): The seconds to convert to frames
        fps (int): The frames per second of the video project
        frac (float): The threshold for rounding

    Arithmetic:
        frames = round by fraction(seconds * fps)

    Returns:
        Total number of frames
    """
    frame_count = seconds * fps
    whole_frames = math.floor(frame_count)
    fractional_frames = frame_count % 1

    if fractional_frames >= frac:
        whole_frames += 1

    return whole_frames


def seconds_to_frames(seconds, fps, frac=fraction):
    """
    Convert sections to frames

    Parameters:
        seconds (int): The number of seconds
        fps (int): The number of frames per second in a video project
        frac (float): The threshold for rounding

    Arithmetic:
        frames = (seconds * fps) rounded depending on decimal vs. fraction

    Returns:
        Total number of frames
    """
    return calculate_frame_count(seconds, fps, frac)


def seconds_to_timecode(seconds, fps, frac=fraction):
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
    whole_frames = calculate_frame_count(seconds, fps, frac)
    whole_seconds = math.floor(seconds)
    frame_part = int(whole_frames - whole_seconds * fps)

    return f"{whole_seconds}:{frame_part:02d}"


def convert_time(ref_format, target_format, input_value, bpm=None, fps=None, ticks_per_beat=TPB, do_print=False):
    """
    The main function of BPMtoFPS. Convert a form of audio timing (either MIDI ticks, beats, or timecode) to a video
    format (either video frames or timecode).

    Required Parameters:
        ref_format (string): The input of the function as either a number of ticks, beats, or timecode
        target_format (string): The output of the function as either a number of video frames, timecode, or both
        input_value (string/int): The number of ticks or the timecode to be processed, based on the input provided
        fps (float): The frames per second of the video project

    Optional Parameters:
        bpm (float): The beats per minute, not required if inputting timecode
        ticks_per_beat (int): The number of ticks per beat
        do_print (bool): If true, print the result to the console

    Returns:
        Depending on the target_format, this function returns either the number of frames in the video as an
        integer, the specific timecode in the video as string, or both as a tuple.
    """

    if isinstance(input_value, float):
        raise ValueError("Input must be a string for timecodes or an integer for beats and ticks. Floats are not "
                         "accepted.")

    # Convert input value to appropriate type based on ref_format
    if ref_format in ['ticks', 'beats']:
        try:
            input_value = int(input_value)
        except ValueError:
            raise ValueError("Input for ticks and beats must be an integer.")
    elif ref_format == 'timecode':
        # No conversion needed, handled in timecode_to_seconds function
        pass

    in_conversion_map = {
        'ticks': lambda x: ticks_to_seconds(x, bpm, ticks_per_beat),
        'beats': lambda x: beats_to_seconds(x, bpm),
        'timecode': timecode_to_seconds
    }
    out_conversion_map = {
        'frames': seconds_to_frames,
        'timecode': seconds_to_timecode
    }

    try:
        seconds = in_conversion_map[ref_format](input_value)
        if target_format == 'both':
            output = (out_conversion_map['frames'](seconds, fps), out_conversion_map['timecode'](seconds, fps))
        else:
            output = out_conversion_map[target_format](seconds, fps)
    except Exception as err:
        raise ValueError(f"An error occurred during conversion: {err}")

    if do_print:
        print(output)

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert MIDI ticks or timecode to video frames or timecode')
    parser.add_argument('-i', '--input', type=str, required=True, choices=["ticks", "beats", "timecode"],
                        help='Input format')
    parser.add_argument('-o', '--output', type=str, required=True, choices=["frames", "timecode", "both"],
                        help='Output format ("both" will output frames and timecode in a tuple)')
    parser.add_argument('-iv', '--input_value', type=str, required=True,
                        help='Number of MIDI ticks, specific musical beat, or timecode in mm:ss.sss or ss.sss format')
    parser.add_argument('-b', '--bpm', type=float,
                        help='Beats per minute of the song, not required if inputting timecode')
    parser.add_argument('-f', '--fps', type=float, required=True, help='Frames per second of the video')
    parser.add_argument('-tpb', '--ticks_per_beat', type=int, default=TPB,
                        help='Number of ticks per beat (default is 480)')
    parser.add_argument('-p', '--print', action='store_true', help='Print the output to the console')
    args = parser.parse_args()

    convert_time(args.input, args.output, args.input_value, args.bpm, args.fps, args.ticks_per_beat,
                 args.print)

    if args.input == 'ticks' and args.bpm is None:
        parser.error("-b/--bpm is required when -i/--input is 'ticks'")
    elif args.input == 'beats' and args.bpm is None:
        parser.error("-b/--bpm is required when -i/--input is 'beats'")
