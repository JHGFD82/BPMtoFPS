import math
import argparse

TPB = 480  # Ticks per beat (resolution)
SPM = 60  # Seconds per minute


def ticks_to_seconds(input_value, bpm, ticks_per_beat):
    return input_value / ticks_per_beat / bpm * SPM


def beats_to_seconds(input_value, bpm):
    return input_value / bpm * SPM


def timecode_to_seconds(input_value):
    minutes, seconds = map(float, input_value.split(':'))
    return minutes * SPM + seconds


def calculate_frame_count(seconds, fps):
    frame_count = seconds * fps
    whole_frames = math.floor(frame_count)
    fractional_frames = frame_count % 1

    if fractional_frames >= 0.75:
        whole_frames += 1

    return whole_frames


def seconds_to_frames(seconds, fps):
    return calculate_frame_count(seconds, fps)


def seconds_to_timecode(seconds, fps):
    whole_frames = calculate_frame_count(seconds, fps)
    whole_seconds = math.floor(seconds)
    frame_part = int(whole_frames - whole_seconds * fps)

    return f"{whole_seconds}:{frame_part:02d}"


def convert_time(ref_format, target_format, input_value, bpm=None, fps=None, ticks_per_beat=TPB, do_print=False):
    """
    The main function of BPMtoFPS. Convert a form of audio timing (either MIDI ticks, beats, or timecode) to a video
    format (either video frames or timecode).

    Required Parameters:
        ref_format (string): The input of the function as either a number of ticks, beats, or timecode
        target_format (string): The output of the function as either a number of video frames or timecode
        input_value (string/int): The number of ticks or the timecode to be processed, based on the input provided
        fps (float): The frames per second of the video project

    Optional Parameters:
        bpm (float): The beats per minute, not required if inputting timecode
        ticks_per_beat (int): The number of ticks per beat
        do_print (bool): If true, print the result to the console

    Returns:
        The frame number at which the note occurs
    """

    if isinstance(input_value, float):
        raise ValueError(
            "Input must be a string for timecodes or an integer for beats and ticks. Floats are not accepted.")

    if ":" in str(input_value):
        input_value = str(input_value)
    else:
        try:
            input_value = int(input_value)
        except ValueError:
            raise ValueError("Input must be a string for timecodes or an integer for beats and ticks.")

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
                        help='Number of MIDI ticks, specific musical beat, or timecode in hh:mm:ss.sss format')
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
