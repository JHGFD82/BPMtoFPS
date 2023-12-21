import math
import argparse

SPM = 60  # Seconds per minute
TPB = 480  # Ticks per beat


def ticks_or_timecode(string):
    if ":" in string:  # this is a very simple check for a timecode
        return string
    else:
        return int(string)


def main(in_format, out_format, tt, bpm, fps, ticks_per_beat):
    """
    This is the main function of the package and currently accommodates MIDI ticks to video frames, with ambitions to
    include other forms of audio to video conversions.

    Parameters:
        in_format (string): The input of the function as either a number of ticks or timecode
        out_format (string): The output of the function as either a number of video frames or timecode
        tt (string/int): The number of ticks or the timecode to be processed, based on the input provided
        bpm (float): The beats per minute
        fps (float): The frames per second
        ticks_per_beat (int): The number of ticks per beat

    Returns:
        The frame number at which the note occurs
    """
    result = 0
    if in_format == 'ticks':
        result = tt / ticks_per_beat / bpm * SPM
    elif in_format == 'timecode':
        result = int(tt.split(':')[0] * 60) + int(tt.split(':')[1])
    print(tt.split(':')[0])
    output = 0
    if out_format == 'frames':
        output = math.floor(result * fps)
    elif out_format == 'timecode':
        output = str(math.floor(result / SPM)) + ':' + str(math.floor(result % 1 * fps))
    print('The note occurs at the frame number:', output)
    return output


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert MIDI ticks or timecode to video frames or timecode')
    parser.add_argument('-i', '--input', type=str, required=True, choices=["ticks", "timecode"], help='Input format')
    parser.add_argument('-o', '--output', type=str, required=True, choices=["frames", "timecode"], help='Output format')
    parser.add_argument('-iv', '--input_value', type=ticks_or_timecode, required=True, help='Number of MIDI '
                                                                                                 'ticks or timecode '
                                                                                                 'in hh:mm:ss.mmm '
                                                                                                 'format')
    parser.add_argument('-b', '--bpm', type=float, required=True, help='Beats per minute of the song')
    parser.add_argument('-f', '--fps', type=float, required=True, help='Frames per second of the video')
    parser.add_argument('-tpb', '--ticks_per_beat', type=int, default=TPB, help='Number of ticks per beat (default is '
                                                                                '480)')
    args = parser.parse_args()

    main(args.input, args.output, args.input_value, args.bpm, args.fps, args.ticks_per_beat)
