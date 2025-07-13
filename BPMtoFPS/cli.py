"""
Command-line interface for BPMtoFPS package.
"""

import argparse
import sys
from typing import Dict, Union

from .models import InputFormat, OutputFormat
from .constants import DEFAULT_TICKS_PER_BEAT
from .main import convert_time


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
    formatted_lines: list[str] = []
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


def main():
    """Main CLI entry point."""
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


if __name__ == '__main__':
    main()
