import math
import argparse

TPB = 480  # Ticks per beat (resolution)
SPM = 60  # Seconds per minute


def ticks_or_timecode(value):
    """
    Ensure that the supplied string is either valid timecode or integer.
    Parameters:
        value (string/int): The text to be analyzed
    Returns:
        The text as either a string or an integer based on the appearance of the ':' in the string.
    Raises:
        ValueError: If the value cannot be converted to integer (for beats and ticks) or isn't a string (for timecodes)
    """
    if isinstance(value, float):  # To catch case when an input is float and it's not timecode
        raise ValueError("Input must be a string for timecodes or an integer for beats and ticks. Floats are not "
                         "accepted.")
    try:
        # Presence of ":" indicates this should be a timecode, so keep it as string
        if ":" in value:
            return value
        # Otherwise, try to convert to an integer for beats and ticks
        else:
            return int(value)
    except (ValueError, TypeError) as e:
        raise ValueError("Input must be a string for timecodes or an integer for beats and ticks") from e


def ticks_to_seconds(input_value, bpm, ticks_per_beat):
    return input_value / ticks_per_beat / bpm * SPM


def beats_to_seconds(input_value, bpm):
    return input_value / bpm * SPM


def timecode_to_seconds(input_value):
    minutes, seconds = map(float, input_value.split(':'))
    return minutes * SPM + seconds


def seconds_to_frames(seconds, fps):
    return math.floor(seconds * fps)


def seconds_to_timecode(seconds, fps):
    return f"{math.floor(seconds)}:{math.floor(seconds % 1 * fps):02d}"


def convert_audio_to_video_timing(ref_format, target_format, input_value, bpm=None, fps=None,
                                  ticks_per_beat=TPB, do_print=False):
    """
    The main function of BPMtoFPS. Convert a form of audio timing (either MIDI ticks, beats, or timecode) to a video
    format (either video frames or timecode).
    Parameters:
        ref_format (string): The input of the function as either a number of ticks, beats, or timecode
        target_format (string): The output of the function as either a number of video frames or timecode
        input_value (string/int): The number of ticks or the timecode to be processed, based on the input provided
        bpm (float): The beats per minute
        fps (float): The frames per second
        ticks_per_beat (int): The number of ticks per beat
        do_print (bool): If true, print the result to the console
    Returns:
        The frame number at which the note occurs
    """
    def handle_ticks(value):
        if bpm is None:
            raise ValueError("bpm needed for 'ticks' conversion")
        return ticks_to_seconds(value, bpm, ticks_per_beat)

    def handle_beats(value):
        if bpm is None:
            raise ValueError("bpm needed for 'beats' conversion")
        return beats_to_seconds(value, bpm)

    def frames_handler(seconds):
        if fps is None:
            raise ValueError("fps needed for 'frames' conversion")
        return seconds_to_frames(seconds, fps)

    def timecode_handler(seconds):
        if fps is None:
            raise ValueError("fps needed for 'timecode' conversion")
        return seconds_to_timecode(seconds, fps)

    in_conversion_map = {
        'ticks': handle_ticks,
        'beats': handle_beats,
        'timecode': lambda value: timecode_to_seconds(value)
    }

    out_conversion_map = {
        'frames': frames_handler,
        'timecode': timecode_handler
    }

    try:
        seconds = in_conversion_map[ref_format](input_value)
        output = out_conversion_map[target_format](seconds)
    except Exception as err:
        raise ValueError(f"An error occurred during conversion: {err}")

    if do_print:
        print(output)

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert MIDI ticks or timecode to video frames or timecode')
    parser.add_argument('-i', '--input', type=str, required=True,
                        choices=["ticks", "beats", "timecode"], help='Input format')
    parser.add_argument('-o', '--output', type=str, required=True, choices=["frames", "timecode"], help='Output format')
    parser.add_argument('-iv', '--input_value', type=ticks_or_timecode, required=True,
                        help='Number of MIDI ticks, specific musical beat, or timecode in hh:mm:ss.sss format')
    parser.add_argument('-b', '--bpm', type=float, required=True, help='Beats per minute of the song')
    parser.add_argument('-f', '--fps', type=float, required=True, help='Frames per second of the video')
    parser.add_argument('-tpb', '--ticks_per_beat', type=int,
                        default=TPB, help='Number of ticks per beat (default is 480)')
    parser.add_argument('-p', '--print', action='store_true', help='Print the output to the console')
    args = parser.parse_args()

    convert_audio_to_video_timing(args.input, args.output, args.input_value, args.bpm, args.fps, args.ticks_per_beat,
                                  args.print)
