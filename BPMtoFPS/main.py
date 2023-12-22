import math
import argparse

TPB = 480  # Ticks per beat (resolution)
SPM = 60  # Seconds per minute


def ticks_or_timecode(string):
    if ":" in string:
        return string
    else:
        return int(string)


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


def convert_audio_to_video_timing(in_format, out_format, input_value, bpm, fps, ticks_per_beat=TPB, do_print=False):
    """
    Convert some form of audio timing (either MIDI ticks or timecode) to a video format (either video frames or
    timecode).
    Parameters:
        in_format (string): The input of the function as either a number of ticks or timecode
        out_format (string): The output of the function as either a number of video frames or timecode
        input_value (string/int): The number of ticks or the timecode to be processed, based on the input provided
        bpm (float): The beats per minute
        fps (float): The frames per second
        ticks_per_beat (int): The number of ticks per beat
        do_print (bool): If true, print the result to the console
    Returns:
        The frame number at which the note occurs
    """
    if in_format == 'ticks':
        seconds = ticks_to_seconds(input_value, bpm, ticks_per_beat)
    elif in_format == 'beats':
        seconds = beats_to_seconds(input_value, bpm)
    elif in_format == 'timecode':
        seconds = timecode_to_seconds(input_value)

    if out_format == 'frames':
        output = seconds_to_frames(seconds, fps)
    elif out_format == 'timecode':
        output = seconds_to_timecode(seconds, fps)

    if do_print:
        print(output)

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert MIDI ticks or timecode to video frames or timecode')
    parser.add_argument('-i', '--input', type=str, required=True, choices=["ticks", "beats", "timecode"], help='Input '
                                                                                                               'format')
    parser.add_argument('-o', '--output', type=str, required=True, choices=["frames", "timecode"], help='Output format')
    parser.add_argument('-iv', '--input_value', type=ticks_or_timecode, required=True, help='Number of MIDI ticks or '
                                                                                            'timecode in hh:mm:ss.mmm '
                                                                                            'format')
    parser.add_argument('-b', '--bpm', type=float, required=True, help='Beats per minute of the song')
    parser.add_argument('-f', '--fps', type=float, required=True, help='Frames per second of the video')
    parser.add_argument('-tpb', '--ticks_per_beat', type=int, default=TPB, help='Number of ticks per beat (default is '
                                                                                '480)')
    parser.add_argument('-p', '--print', action='store_true', default=False, help='Print the output to the console')
    args = parser.parse_args()

    convert_audio_to_video_timing(args.input, args.output, args.input_value, args.bpm, args.fps, args.ticks_per_beat,
                                  args.print)
